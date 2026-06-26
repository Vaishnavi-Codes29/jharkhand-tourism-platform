# Jharkhand Tourism - Setup Guide

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set your Anthropic API key (REQUIRED for chatbot)

**Option A — Environment variable (recommended):**
```bash
# Linux/Mac
export ANTHROPIC_API_KEY=sk-ant-your-key-here
python app.py

# Windows
set ANTHROPIC_API_KEY=sk-ant-your-key-here
python app.py
```

**Option B — Edit app.py directly:**
Open `app.py` and replace line:
```python
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "your-anthropic-api-key-here")
```
with:
```python
ANTHROPIC_API_KEY = "sk-ant-your-actual-key-here"
```

Get your API key at: https://console.anthropic.com

### 3. Run the server
```bash
python app.py
```

### 4. Open in browser
Visit: http://localhost:5000

---

## Admin Login
- Email: admin@jharkhand.gov.in
- Password: Admin@123#

## Demo Tourist Login
- Email: priya@gmail.com
- Password: Priya@123

## Demo Provider Login
- Email: raju@gmail.com
- Password: Raju@123!

---

## Features
- AI chatbot powered by Claude (via `/chat` backend endpoint)
- Admin can see all provider requests, tourist bookings, approve/reject providers
- Tourist dashboard with bookings, trip planner, marketplace
- Provider dashboard with listings and booking management
- Session-based authentication with SQLite database
