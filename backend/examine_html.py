import requests
from bs4 import BeautifulSoup

url = "https://www.moneycontrol.com/news/business/markets/q3-results-impact-jsw-energy-godrej-consumer-products-shares-plunge-10-india-cements-up-5-13791944.html"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

response = requests.get(url, headers=HEADERS, timeout=10)
soup = BeautifulSoup(response.text, "html.parser")

# Save a portion of the HTML to examine
with open("moneycontrol_sample.html", "w", encoding="utf-8") as f:
    # Get the article header area
    article_header = soup.find("div", class_="article_box")
    if article_header:
        f.write(str(article_header)[:5000])  # First 5000 chars
    else:
        f.write(str(soup)[:10000])  # First 10000 chars of full page

print("HTML sample saved to moneycontrol_sample.html")

# Also search for any time-related elements
print("\n=== Searching for time-related elements ===")
time_elements = soup.find_all(["time", "span", "div"], class_=lambda x: x and ("time" in x.lower() or "date" in x.lower() or "publish" in x.lower() or "schedule" in x.lower()))
for elem in time_elements[:10]:
    print(f"\nTag: {elem.name}, Class: {elem.get('class')}")
    print(f"Text: {elem.get_text(strip=True)[:100]}")
    print(f"Datetime attr: {elem.get('datetime')}")
