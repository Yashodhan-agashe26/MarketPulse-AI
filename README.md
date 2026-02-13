MarketPulse AI
MarketPulseAI-main/
├── backend/
│   ├── main.py
│   ├── chatbot.py
│   ├── notification_manager.py
│   ├── email_service.py
│   ├── scraper.py
│   ├── sentiment.py
│   └── database.py
│
├── frontend/
│   ├── src/components
│   ├── src/pages
│   ├── src/context
│   └── public/
│
└── README.md

🏗️ System Architecture
Dynamic RAG Flow

Extract ticker → Check ChromaDB → Fetch financials if missing → Embed → Retrieve → Generate factual answer.

Component Overview

Frontend

React UI, polling every 5 seconds for updates.

Sends AI queries to backend.

Backend

FastAPI orchestration.

Endpoints:

/news

/market

/chat

/stock/{symbol}/financials

Scraper

BeautifulSoup + Requests.

Cached JSON news storage.

AI Engine

Local Ollama Llama 3.2

FinBERT sentiment

Notification System

APScheduler every 1 minute

Watchlist keyword matching → Gmail SMTP alert.

🛡️ Disclaimer

This project is for educational purposes only.
AI insights and sentiment analysis must not be treated as financial advice.
Always perform independent research before investing.

👨‍💻 Team

Prashant Gupta

Aniruddha Dawkhare

Yashodhan Agashe

Ayushi Punde

Rujali Nagbhidkar

Priyanka Mankar
