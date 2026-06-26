# Jharkhand Tourism - Complete Setup Guide

## 📋 Prerequisites
- Python 3.8+
- pip (Python package manager)
- Anthropic API key (get from https://console.anthropic.com)

## 🚀 Quick Start (5 minutes)

### Step 1: Clone or Download the Project
```bash
cd d:\jharkhand_tourism_updated\New-folder
```

### Step 2: Create Virtual Environment (Optional but recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
pip install python-dotenv  # For environment variable management
```

### Step 4: Setup Environment Variables
1. Copy `.env.example` to `.env`:
```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

2. Edit `.env` file and add your Anthropic API key:
```
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
```

### Step 5: Run the Application
```bash
python app.py
```

The app will be available at: **http://127.0.0.1:5000**

---

## 📁 Project Structure

```
.
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
├── database.db            # SQLite database (auto-created)
├── README.md              # Project overview
├── SETUP.md               # This file
├── API_GUIDE.md           # API documentation
├── templates/
│   └── index.html         # Frontend HTML
├── static/                # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
└── logs/                  # Application logs
```

---

## 🔧 Configuration Options

Edit `.env` file to customize:

| Variable | Default | Description |
|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | Required | Your Anthropic API key |
| `FLASK_ENV` | development | development or production |
| `SECRET_KEY` | dev-key | Flask session secret (change in production) |
| `HOST` | 127.0.0.1 | Server host address |
| `PORT` | 5000 | Server port |
| `DATABASE_PATH` | database.db | Path to SQLite database |

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution:** Install dependencies: `pip install -r requirements.txt`

### Issue: "ANTHROPIC_API_KEY not set"
**Solution:** 
1. Check `.env` file exists in project root
2. Verify API key is set correctly in `.env`
3. Restart the app after setting the key

### Issue: "Address already in use" (Port 5000)
**Solution:** Change PORT in `.env` or use:
```bash
python app.py --port 8000
```

### Issue: Database errors
**Solution:** Delete `database.db` to reset, or check file permissions

---

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Anthropic API Docs](https://docs.anthropic.com/)
- [SQLite Docs](https://www.sqlite.org/docs.html)

---

## 💡 Tips for Developers

1. **Use virtual environment:** Keeps dependencies isolated
2. **Keep `.env` secure:** Never commit to git (added to .gitignore)
3. **Check logs:** Look for errors in console output
4. **Test API endpoints:** Use Postman or curl (see API_GUIDE.md)

---

## 🤝 Support

For issues or questions, check:
- `README.md` for project overview
- `API_GUIDE.md` for endpoint documentation
- Application console for error messages
