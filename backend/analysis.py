import json
import os
import time
from datetime import datetime, timedelta
import google.generativeai as genai
import yfinance as yf

# Load Env (or rely on system env)
# In production, use python-dotenv. Here we assume exported vars.
JSON_FILE = "moneycontrol_news.json"

def init_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY not found.")
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.5-flash')

def load_news():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_news(news_list):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(news_list, f, indent=4, ensure_ascii=False)

def extract_ticker(model, headline):
    prompt = f"""
    Analyze this news headline and return a JSON object with two fields:
    1. "ticker": The primary Indian stock market ticker (NSE/BSE) for the company mentioned. Suffix with .NS or .BO. If none, use null.
    2. "short_question": A very short, natural 3-6 word question a user would ask about this impact.
    
    Headline: "{headline}"
    
    Example Output: {{ "ticker": "TATAMOTORS.NS", "short_question": "Impact of Tata EV launch?" }}
    Example Output: {{ "ticker": null, "short_question": "Market sentiment today?" }}
    """
    try:
        response = model.generate_content(prompt)
        text = response.text.replace("```json", "").replace("```", "").strip()
        data = json.loads(text)
        return data
    except Exception as e:
        print(f"Gemini Error: {e}")
        return {"ticker": None, "short_question": None}

def calculate_impact(ticker_symbol, news_timestamp_str):
    try:
        # timestamp format: "YYYY-MM-DD HH:MM:SS"
        news_time = datetime.strptime(news_timestamp_str, "%Y-%m-%d %H:%M:%S")
        
        # If news is after market close (3:30 PM), look at next day
        if news_time.hour >= 15 and news_time.minute >= 30:
            start_date = news_time + timedelta(days=1)
        else:
            start_date = news_time

        end_date = start_date + timedelta(days=5) # Buffer for weekends/holidays

        ticker = yf.Ticker(ticker_symbol)
        hist = ticker.history(start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"))

        if hist.empty:
            return None

        # Take the first available trading day
        row = hist.iloc[0]
        open_price = row['Open']
        close_price = row['Close']
        
        if open_price == 0: return 0.0

        pct_change = ((close_price - open_price) / open_price) * 100
        return round(pct_change, 2)

    except Exception as e:
        print(f"yfinance Error for {ticker_symbol}: {e}")
        return None

def main():
    print("Initializing Analysis Engine...")
    model = init_gemini()
    if not model:
        return

    news_list = load_news()
    updated_count = 0

    print(f"Processing {len(news_list)} news items...")

    for item in news_list:
        # Skip if already analyzed
        if "ticker" in item and "actual_impact" in item:
            continue

        print(f"Analyzing: {item['headline'][:50]}...")
        
        # 1. Extract Ticker & Question
        result = extract_ticker(model, item['headline'])
        ticker = result.get('ticker')
        question = result.get('short_question')
        
        item['ticker'] = ticker
        item['suggested_question'] = question
        
        # 2. Calculate Impact if ticker found
        impact = None
        if ticker:
            print(f"  -> Found Ticker: {ticker} | Q: {question}")
            impact = calculate_impact(ticker, item['timestamp'])
            if impact is not None:
                print(f"  -> Impact: {impact}%")
            else:
                print("  -> No market data found for date.")
        else:
            print("  -> No specific ticker identified.")

        item['actual_impact'] = impact
        updated_count += 1
        
        # Rate limiting to be safe
        time.sleep(1) 

        # Save periodically
        if updated_count % 5 == 0:
            save_news(news_list)

    save_news(news_list)
    print(f"Analysis Complete. Updated {updated_count} items.")

if __name__ == "__main__":
    main()
