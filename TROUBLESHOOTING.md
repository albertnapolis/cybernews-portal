# Troubleshooting Guide

## Common Issues and Solutions

### 1. Port 8000 Already in Use

**Error Message:**
```
ERROR: [Errno 10048] error while attempting to bind on address ('0.0.0.0', 8000):
only one usage of each socket address (protocol/network address/port) is normally permitted
```

**Solutions:**

#### Option A: Use the Management Script (Recommended)
```bash
cd cybersecurity-portal/backend
python manage_server.py restart
```

#### Option B: On Windows, Use Batch Files
```bash
cd cybersecurity-portal/backend
restart_server.bat
```

#### Option C: Manual Process Kill
1. Find the process using port 8000:
   ```bash
   # Windows
   netstat -ano | findstr :8000

   # Linux/Mac
   lsof -i :8000
   ```

2. Kill the process:
   ```bash
   # Windows (replace PID with actual process ID)
   taskkill //F //PID [PID]

   # Linux/Mac
   kill -9 [PID]
   ```

3. Start the server again:
   ```bash
   python simple_run.py
   ```

### 2. ModuleNotFoundError: No module named 'app'

**Error Message:**
```
ModuleNotFoundError: No module named 'app'
```

**Solution:**
Run the server from the backend directory using the provided scripts:
```bash
cd cybersecurity-portal/backend
python simple_run.py
# OR
python manage_server.py start
```

### 3. Feedparser Error

**Error Message:**
```
ERROR:app.services.feed_parser:Error extracting article data:
module 'feedparser' has no attribute '_parse_date'
```

**Solution:**
This has been fixed in the latest code. Make sure you're using the updated `feed_parser.py` file.

### 4. No News Articles Showing

**Solution:**
Manually trigger a feed refresh:
```bash
# Using curl
curl -X POST http://localhost:8000/api/v1/news/refresh

# Or using Python
python -c "import requests; print(requests.post('http://localhost:8000/api/v1/news/refresh').json())"
```

### 5. Frontend Cannot Connect to Backend

**Possible Causes:**
1. Backend not running
2. CORS not configured properly
3. Wrong API URL in frontend

**Solutions:**
1. Ensure backend is running:
   ```bash
   curl http://localhost:8000/health
   ```

2. Check frontend `.env` file:
   ```
   VITE_API_URL=http://localhost:8000/api/v1
   ```

3. Restart both servers:
   ```bash
   # Backend
   cd cybersecurity-portal/backend
   python manage_server.py restart

   # Frontend
   cd cybersecurity-portal/frontend
   npm run dev
   ```

### 6. Database Issues

**Solution:**
Delete the SQLite database and let it recreate:
```bash
cd cybersecurity-portal/backend
del cybernews.db  # Windows
rm cybernews.db   # Linux/Mac
python simple_run.py
```

### 7. Dependencies Not Installed

**Backend:**
```bash
cd cybersecurity-portal/backend
pip install -r requirements.txt
```

**Frontend:**
```bash
cd cybersecurity-portal/frontend
npm install
```

## Quick Health Check

Run this to verify everything is working:
```bash
cd cybersecurity-portal/backend
python test_api.py
```

Expected output:
```
[OK] Root endpoint is working
[OK] Health endpoint is working
[OK] News endpoint is working
[OK] Categories endpoint is working
[OK] Sources endpoint is working
```

## Server Management Commands

### Start Server
```bash
python manage_server.py start
# or
start_server.bat  # Windows
```

### Stop Server
```bash
python manage_server.py stop
# or
stop_server.bat  # Windows
```

### Restart Server
```bash
python manage_server.py restart
# or
restart_server.bat  # Windows
```

## Need More Help?

1. Check the server logs in the terminal where you started the backend
2. Enable debug mode by setting `DEBUG=True` in `.env`
3. Check browser console for frontend errors (F12)
4. Verify all dependencies are installed correctly