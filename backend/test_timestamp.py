import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# Test timestamp extraction on a single article
test_url = "https://www.moneycontrol.com/news/business/markets/q3-results-impact-jsw-energy-godrej-consumer-products-shares-plunge-10-india-cements-up-5-13791944.html"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

print(f"Testing timestamp extraction for: {test_url}\n")

try:
    response = requests.get(test_url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    
    timestamp = None
    
    # Try JSON-LD
    print("Trying JSON-LD...")
    scripts = soup.find_all("script", type="application/ld+json")
    for script in scripts:
        if script.string:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict) and "datePublished" in data:
                    timestamp = data["datePublished"]
                    print(f"Found in JSON-LD: {timestamp}")
                    break
                elif isinstance(data, list):
                    for item in data:
                        if "datePublished" in item:
                            timestamp = item["datePublished"]
                            print(f"Found in JSON-LD list: {timestamp}")
                            break
            except:
                continue
    
    # Try meta tags
    if not timestamp:
        print("\nTrying meta tags...")
        meta_date = soup.find("meta", property="article:published_time")
        if meta_date:
            timestamp = meta_date.get("content")
            print(f"Found in meta tag: {timestamp}")
    
    # Try article body
    if not timestamp:
        print("\nTrying article body...")
        time_span = soup.find("span", class_="article_schedule")
        if time_span:
            timestamp = time_span.get_text(strip=True)
            print(f"Found in article body: {timestamp}")
    
    if timestamp:
        print(f"\n✓ Successfully extracted timestamp: {timestamp}")
        
        # Try to format it
        try:
            dt_obj = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            formatted = dt_obj.strftime("%d %b %Y, %I:%M %p")
            print(f"✓ Formatted timestamp: {formatted}")
        except Exception as e:
            print(f"✗ Error formatting: {e}")
    else:
        print("\n✗ Could not extract timestamp")
        
except Exception as e:
    print(f"Error: {e}")
