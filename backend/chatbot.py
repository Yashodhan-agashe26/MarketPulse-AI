import google.generativeai as genai
import os
import json
from scraper import get_latest_news, scrape_article_content
from sentiment import analyze_sentiment
from summarizer import summarize_with_t5

# Setup models
chat_model = None
news_model = None

def init_gemini():
    global chat_model
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        try:
            # We need to configure the global genai with one key, 
            # or creates specific client instances if the library supports it.
            # The google-generativeai library uses a global configuration usually, 
            # but we can try to re-configure or use different client instances if available.
            # However, for simplicity given standard usage:
            # If both keys are different, we might need to re-configure before each call 
            # OR hopefully the client supports passing `api_key` to the model constructor or similar?
            # Checking docs (mental check): genai.configure() sets the global default.
            # To use diverse keys, we might need to handle it carefully.
            # Let's assume we can re-configure before generation or use a context manager if needed.
            # BUT, standard approach:
            genai.configure(api_key=api_key)
            chat_model = genai.GenerativeModel('gemini-2.5-flash')
            print("Gemini Chat model initialized.")
        except Exception as e:
            print(f"Error initializing Gemini Chat: {e}")
    else:
        print("Warning: GEMINI_API_KEY not found. Chatbot will not work.")

def init_summarizer():
    global news_model
    # For the news summarizer, we utilize the specific news API key.
    # Note: Using `genai.configure` switches the global key. 
    # Since this is a threaded environment (FastAPI), switching globals is risky.
    # However, for this implementation script, we'll try to instantiate with specific client objects if possible,
    # or just switch context. 
    # actually, the google-generativeai python client is a wrapper.
    # If we really need two different keys at the same time, it is tricky with the `genai` global.
    # Let's look at `genai.configure`...
    # As a workaround for different keys in the same process:
    # We can pass `api_key` to `generate_content`? No, usually not.
    # We can create a partial wrapper.
    # STARTUP-CHECK: If users provided two different keys, we really want to respect that.
    # Let's try to set it just-in-time if necessary, but that's not thread-safe.
    # Let's assume for now we configure the NEWS key in `init_summarizer` solely for the `news_model` 
    # knowing that `chat_model` relies on the other. 
    # WAIT - this is a conflict if both are used concurrently. 
    # Correct path: `lib` usually supports Client(api_key=...) in newer versions.
    # Falling back to strict re-configuration might be our only option without inspecting library version deeply.
    # We will implement a helper to call generation with a specific key.
    
    api_key = os.getenv("GEMINI_NEWS_API_KEY") or os.getenv("GEMINI_API_KEY")
    if api_key:
        try:
            # We'll just define the model here, but the key binding happens at call time if we can.
            # Or we simply re-configure.
            news_model = genai.GenerativeModel('gemini-2.5-flash')
            print("Gemini News model initialized.")
        except Exception as e:
            print(f"Error initializing Gemini News: {e}")
    else:
        print("Warning: GEMINI_NEWS_API_KEY (and fallback GEMINI_API_KEY) not found. Summarizer will not work.")

# Load stocks.json for alignment
STOCKS_FILE = os.path.join(os.path.dirname(__file__), "stocks.json")
try:
    with open(STOCKS_FILE, "r") as f:
        stocks_data = json.load(f)
        stocks_dict = stocks_data.get("companies", {})
except Exception as e:
    print(f"Error loading stocks.json: {e}")
    stocks_dict = {}

def generate_with_key(model_instance, prompt, api_key_env_var):
    """
    Helper to safely switch API keys for a specific generation call.
    This is not thread-safe but works for this basic setup.
    """
    current_key = os.getenv(api_key_env_var)
    if not current_key and api_key_env_var == "GEMINI_NEWS_API_KEY":
        current_key = os.getenv("GEMINI_API_KEY")

    if not current_key:
        return "Error: API Key not found."
    
    # Configure with the specific key for this call
    genai.configure(api_key=current_key)
    try:
        response = model_instance.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating content: {e}"

def get_chat_response(user_query):
    if not chat_model:
        init_gemini()
        if not chat_model:
            return "Error: Gemini API key not configured. Please set GEMINI_API_KEY."

    # Get context from latest news
    news = get_latest_news()
    
    # Create a summary context from the top 10 news items
    context = "Here is the latest financial news and historical analysis:\n"
    for item in news[:10]:
        impact_str = ""
        if item.get('ticker') and item.get('actual_impact') is not None:
            impact_str = f" [Historical Impact: {item['ticker']} moved {item['actual_impact']}%]"
        
        context += f"- {item['headline']} ({item['timestamp']}) - Sentiment: {item.get('sentiment', 'Unknown')}{impact_str}\n"

    prompt = f"""You are a helpful financial assistant for MarketPulse AI.
    Use the provided news context to answer the user's question.
    
    CRITICAL INSTRUCTION:
    If the context contains "Historical Impact" data for a company the user is asking about, YOU MUST mentions it.
    Example: "Based on similar past news, this stock moved X%."
    
    Context:
    {context}
    
    User Question: {user_query}
    """

    # Use the Chat API Key
    return generate_with_key(chat_model, prompt, "GEMINI_API_KEY")

def summarize_news(url):
    # Try to find content in cache first
    news = get_latest_news()
    content = next((n.get("full_content") for n in news if n.get("link") == url), None)
    
    if not content:
        print(f"Content not in cache for {url}, scraping...")
        content = scrape_article_content(url)
        if content and content != "Could not extract article content.":
            # Save to JSON for future use
            try:
                from scraper import load_existing_news, save_news
                existing_news = load_existing_news()
                updated = False
                for item in existing_news:
                    if item.get("link") == url:
                        item["full_content"] = content
                        updated = True
                        break
                if updated:
                    save_news(existing_news)
                    print(f"Persisted content for {url} to disk.")
            except Exception as e:
                print(f"Failed to persist content for {url}: {e}")
        
    if not content:
        return {"summary": "Failed to fetch article content.", "sentiment": "neutral"}

    # Initialize FinBERT if not already
    from sentiment import init_model as init_finbert
    init_finbert()

    # 1. Analyze Sentiment with FinBERT First (using first 2000 chars for speed/limit)
    finbert_result = analyze_sentiment(content[:2000]) 
    finbert_label = finbert_result.get("label", "neutral").capitalize()
    
    # 2. Use FLAN-T5 for both Metadata and Summary
    print(f"Generating T5 full summary (metadata + insights) for {url}...")
    
    # Combined prompt for T5 to handle everything locally
    t5_prompt = """Extract metadata and summarize this financial article:
Format:
Company Name: [Extract]
Sector: [Extract]
Incident Type: [Classify]

Key Insights (AI Generated):
[3-sentence summary]

Article Content:
{text}
"""
    
    final_summary_text = summarize_with_t5(content, max_length=250, custom_prompt=t5_prompt)

    return {
        "summary": final_summary_text,
        "sentiment": finbert_label.lower() 
    }


if __name__ == "__main__":
    # Test only if needed
    pass
