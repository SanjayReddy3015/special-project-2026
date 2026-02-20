# 🌾 WikiKisan Backend API

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Framework-FastAPI-009688)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**WikiKisan** is a robust, AI-powered agricultural backend designed to empower farmers with real-time community insights, market data, and expert advice. Built with high-performance Python and MongoDB, it serves as the intelligence layer for the WikiKisan ecosystem.

---

## 🚀 Features

* **Farmer's Community:** A multilingual forum (English, Hindi, Telugu) for crop-specific discussions and problem-solving.
* **AI Farming Advisor:** Integrated with Google Gemini 2.0 Flash to provide expert agricultural guidance.
* **Real-time Weather Analysis:** Contextual farming advice based on live weather data (e.g., pesticide safety alerts).
* **Mandi Price Tracker:** Fetches real-time market data to help farmers find the best prices for their produce.
* **Advanced Middleware:** Built-in performance monitoring, global error handling, and structured logging.

---

## 📁 Project Structure

```text
wikikisan-backend/
├── app/
│   ├── api/             # Route handlers (Community, Weather, Market)
│   ├── core/            # Configuration and security logic
│   ├── models/          # Data schemas (Pydantic/MongoDB)
│   ├── services/        # Business logic (AI Advisor, Translation)
│   ├── database.py      # Async MongoDB connection pool
│   └── main.py          # Application entry point
├── scripts/             # Data seeding and automation scripts
├── .env                 # Environment variables (Private)
└── requirements.txt     # Dependency list
