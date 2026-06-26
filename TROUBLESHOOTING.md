# Troubleshooting & Common Issues

## Issue #1: `AttributeError: 'Flask' object has no attribute 'before_first_request'`

### Problem
Flask 2.0+ removed the `@app.before_first_request` decorator as it was incompatible with asynchronous contexts.

### Error Message
```
AttributeError: 'Flask' object has no attribute 'before_first_request'. Did you mean: 'before_request'?
```

### Root Cause
The decorator was used in `app.py` but it's no longer available in modern Flask versions.

### Solution Applied ✅
Changed from:
```python
@app.before_first_request
def create_tables():
    with app.app_context():
        db.create_all()
```

To:
```python
@app.before_request
def create_tables():
    with app.app_context():
        db.create_all()
```

**Result**: App now starts successfully and database tables are created on demand.

---

## Issue #2: `SAWarning: Duplicate class names in declarative base`

### Problem
Flask-SQLAlchemy warning about duplicate `Service` class names.

### Error Message
```
SAWarning: This declarative base already contains a class with the same class name 
and module name as models.Service, and will be replaced in the string-lookup table.
```

### Root Cause
Multiple imports or reloading of the `Service` model during Flask's debug reload mode.

### Status
⚠️ **Non-critical warning** - App functions correctly. Occurs during Flask debug reload (when code changes are detected).

### How to Minimize
The warning appears only during development. In production with debug=False, it won't appear.

To suppress during development, add to `app.py`:
```python
import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
```

---

## Common Setup Issues & Solutions

### Issue: Import Error - No module named 'models'

**Cause**: Missing or incorrect imports  
**Solution**:
```bash
# Verify you're in the correct directory
cd d:\jharkhand_tourism_updated\New-folder

# Verify models.py exists
ls models.py

# Re-install dependencies
pip install -r requirements.txt
```

### Issue: ModuleNotFoundError - No module named 'flask'

**Cause**: Flask not installed  
**Solution**:
```bash
pip install Flask
pip install -r requirements.txt
```

### Issue: Anthropic API Key Error

**Error**: "API key not configured"  
**Cause**: ANTHROPIC_API_KEY not set  
**Solution**:
```bash
# Create .env file
cp .env.example .env

# Edit .env and add your key
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### Issue: Database File Permission Denied

**Cause**: database.db file locked by another process  
**Solution**:
```bash
# Stop Flask server (Ctrl+C)
# Close any other connections
# Restart Flask
python app.py
```

### Issue: Port 5000 Already in Use

**Cause**: Another application using port 5000  
**Solution - Option 1**: Stop the other application  
**Solution - Option 2**: Use different port
```bash
# Set PORT environment variable
set PORT=5001
python app.py
```

### Issue: Template Not Found Error

**Error**: `TemplateNotFound: index.html`  
**Cause**: Templates not in correct location  
**Solution**:
```bash
# Verify templates directory exists
ls templates/

# Verify all HTML files are present
ls templates/*.html
```

### Issue: CORS Errors in Browser Console

**Error**: `Access to XMLHttpRequest blocked by CORS policy`  
**Cause**: CORS not enabled or misconfigured  
**Verify**: In `app.py`, check:
```python
from flask_cors import CORS
CORS(app)  # This line must be present
```

---

## Testing Endpoints

### Test 1: Home Page
```bash
# Should return index.html
Invoke-WebRequest -Uri "http://127.0.0.1:5000/" -UseBasicParsing
```

### Test 2: Register User
```bash
$body = @{
    name = "Test User"
    email = "test@example.com"
    password = "Password123!"
    role = "tourist"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/register" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

### Test 3: Get Destinations
```bash
Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/destinations" `
    -UseBasicParsing
```

### Test 4: Check Session
```bash
Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/check-session" `
    -UseBasicParsing
```

---

## Debugging Tips

### Enable Verbose Logging
```python
# Add to app.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Database
```bash
# Verify database.db exists
ls -la database.db

# Inspect with sqlite3 (if installed)
sqlite3 database.db ".tables"
```

### Check Requirements
```bash
# List installed packages
pip list

# Verify all required packages
pip check
```

### Monitor Flask Server Output
Look for these indicators:
- ✅ "Running on http://127.0.0.1:5000" - Server started
- ⚠️ SAWarning - Non-critical (debug reload)
- ❌ Traceback - Python error occurred
- 🔄 "Restarting with stat" - Code changed, reloading

---

## Production Deployment Checklist

Before moving to production:

- [ ] Set `FLASK_ENV=production`
- [ ] Change `debug=False` in app.run()
- [ ] Use strong SECRET_KEY (not dev-key)
- [ ] Configure ANTHROPIC_API_KEY in secrets manager
- [ ] Use production WSGI server (Gunicorn, uWSGI)
- [ ] Set up SSL/HTTPS
- [ ] Configure logging to files
- [ ] Set up database backups
- [ ] Configure monitoring & alerts
- [ ] Load test the application
- [ ] Test all API endpoints
- [ ] Set up CI/CD pipeline
- [ ] Document deployment process

---

## Getting Help

If you encounter issues:

1. **Check this file** - Common issues listed above
2. **Check SETUP.md** - Detailed setup instructions
3. **Check API_GUIDE.md** - API endpoint documentation
4. **Check Flask logs** - Terminal output shows detailed errors
5. **Check browser console** - Frontend JavaScript errors

---

## Quick Recovery Steps

### If app won't start:
```bash
# 1. Stop the server (Ctrl+C)
# 2. Check for syntax errors
python -m py_compile app.py

# 3. Check imports
python -c "from app import app; print('OK')"

# 4. Reinstall dependencies
pip install --upgrade -r requirements.txt

# 5. Restart
python app.py
```

### If database is corrupted:
```bash
# Backup the database
cp database.db database.db.backup

# Delete corrupted database
rm database.db

# Restart Flask (will recreate)
python app.py
```

### If stuck in debug loop:
```bash
# 1. Stop Flask (Ctrl+C)
# 2. Check for syntax errors in modified files
# 3. Restart Flask
python app.py
```

---

## Performance Optimization

### For Production:
1. Use Gunicorn instead of Flask development server:
   ```bash
   gunicorn -w 4 -b 127.0.0.1:5000 app:app
   ```

2. Enable caching for static files
3. Use connection pooling for database
4. Enable gzip compression
5. Use CDN for static assets
6. Monitor with tools like Datadog/NewRelic

---

## Security Notes

✅ **Implemented**:
- Session-based authentication
- Password hashing with werkzeug
- CORS validation
- Role-based access control
- SQL injection protection (SQLAlchemy ORM)

⚠️ **For Production**:
- Enable HTTPS/SSL
- Use secure session cookies (HttpOnly, Secure flags)
- Implement rate limiting
- Add input validation & sanitization
- Use environment variables for secrets
- Enable CSRF protection
- Set security headers (CSP, X-Frame-Options, etc.)

---

## Contact & Support

For issues not covered here, check:
- **Flask Documentation**: https://flask.palletsprojects.com/
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org/
- **Anthropic API**: https://docs.anthropic.com/

**Last Updated**: May 14, 2026
