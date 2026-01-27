import time
from dotenv import load_dotenv
load_dotenv()
from chatbot import summarize_news, init_summarizer
import chatbot

# Mock scrape_article_content
test_content = """
Reliance Industries Limited (RIL), led by Mukesh Ambani, announced its quarterly results today in Mumbai. 
The company reported a 15% increase in net profit, driven by strong performance in its O2C and retail segments. 
Analysts say the stock is likely to see a positive reaction in tomorrow's trading session. 
Meanwhile, the energy sector is seeing significant interest from global investors as oil prices stabilize. 
Reliance has also been expanding its green energy footprint in Gujarat.
"""
chatbot.scrape_article_content = lambda url: test_content

def benchmark():
    print("Pre-initializing (if not already)...")
    start_init = time.time()
    init_summarizer()
    end_init = time.time()
    print(f"Initialization took: {end_init - start_init:.2f}s")
    
    print("\nStarting summary generation benchmark (3 runs)...")
    for i in range(1, 4):
        start = time.time()
        result = summarize_news("http://mock-url.com")
        end = time.time()
        print(f"Run {i}: {end - start:.2f}s")
        if i == 1:
            print("-" * 40)
            print("SAMPLE OUTPUT:")
            if isinstance(result, dict):
                print(f"Sentiment: {result.get('sentiment')}")
                print(result.get('summary'))
            else:
                print(result)
            print("-" * 40)

if __name__ == "__main__":
    benchmark()
