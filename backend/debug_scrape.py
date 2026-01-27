import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

url = "https://www.moneycontrol.com/news/business/companies/kotak-mahindra-bank-long-term-story-13790821.html"

try:
    print(f"Fetching {url}...")
    res = requests.get(url, headers=HEADERS, timeout=10)
    print(f"Status: {res.status_code}")
    
    soup = BeautifulSoup(res.text, "html.parser")
    
    og_image = soup.find("meta", property="og:image")
    print(f"OG Image: {og_image}")
    
    twitter_image = soup.find("meta", property="twitter:image") # some sites use name="twitter:image"
    print(f"Twitter Image (prop): {twitter_image}")
    
    twitter_image_name = soup.find("meta", attrs={"name": "twitter:image"})
    print(f"Twitter Image (name): {twitter_image_name}")
    
    # Try finding the main article image
    # Moneycontrol often uses class="artti_img" or similar
    article_img_div = soup.find("div", class_="article_image")
    if article_img_div:
        img = article_img_div.find("img")
        print(f"Article Image Div: {img}")
        
except Exception as e:
    print(f"Error: {e}")
