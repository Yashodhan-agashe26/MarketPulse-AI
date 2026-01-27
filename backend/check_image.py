import json

with open("moneycontrol_news.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for item in data:
    if "Kotak" in item.get("headline", ""):
        print(f"URL: {item.get('image_url')}")
        print(f"LINK: {item.get('link')}")
