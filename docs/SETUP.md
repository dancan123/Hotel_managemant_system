# Installation & Setup Guide

## System Requirements

- **OS**: Windows, macOS, or Linux
- **Python**: 3.8 or higher
- **Browser**: Any modern browser (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
- **RAM**: Minimum 2GB
- **Storage**: 500MB free space

## Step-by-Step Installation

### 1. Backend Installation

#### Step 1.1: Navigate to Backend Directory

```bash
cd hotel_management_system/backend
```

#### Step 1.2: Create Virtual Environment (Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Step 1.3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
- Flask 2.3.0 - Web framework
- Flask-CORS 4.0.0 - Cross-origin resource sharing
- PyJWT 2.8.0 - JSON Web Token authentication
- Werkzeug 2.3.0 - WSGI utilities and password hashing
- openpyxl 3.1.2 - Excel file generation
- reportlab 4.0.4 - PDF file generation

#### Step 1.4: Verify Installation

```bash
pip list
```

You should see all required packages listed.

### 2. Database Setup

The database is automatically initialized when the backend starts for the first time.

#### Manual Database Creation (Optional)

```bash
python
```

```python
from app.utils.database import init_db, _create_sample_data
init_db(None)
_create_sample_data()
exit()
```

### 3. Starting the Backend Server

```bash
python run.py
```

**Expected output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

The backend server will be available at: **http://localhost:5000**

### 4. Frontend Setup

#### Step 4.1: Simple Method - Direct Browser Access

1. Navigate to `frontend/` folder
2. Open `index.html` directly in your browser
3. Update API URL if backend is on different port

#### Step 4.2: Local Web Server (Recommended)

**Using Python:**

```bash
cd frontend
python -m http.server 8000
```

Then navigate to: **http://localhost:8000**

**Using Node.js:**

```bash
cd frontend
npx http-server
```

### 5. Configuration

#### Backend Configuration

Edit `backend/app/__init__.py` to change configuration:

```python
app.config['DEBUG'] = True  # Set to False for production
```

#### Frontend API Configuration

Edit `frontend/js/api.js` to update API base URL:

```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

### 6. First-Time Setup

When you start the backend for the first time:

1. Database `hotel_management.db` is automatically created
2. Database schema is initialized
3. Sample data is loaded (demo users and rooms)

**Demo Credentials:**

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Admin |
| manager1 | manager123 | Manager |
| waiter1 | waiter123 | Employee |
| waiter2 | waiter123 | Employee |
| receptionist1 | recept123 | Employee |

## Verification Checklist

- [ ] Backend running on http://localhost:5000
- [ ] Database file exists: `backend/database/hotel_management.db`
- [ ] Frontend accessible via browser
- [ ] Can login with demo credentials
- [ ] Dashboard loads without errors
- [ ] Charts are visible on dashboard

## Troubleshooting

### Issue: "Port 5000 already in use"

**Solution:**

```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (Windows)
taskkill /PID [PID] /F

# Or use a different port in run.py:
app.run(port=5001)
```

### Issue: "ModuleNotFoundError: No module named 'flask'"

**Solution:**

```bash
# Ensure virtual environment is activated
# Then reinstall dependencies
pip install -r requirements.txt
```

### Issue: "No module named 'app'"

**Solution:**

Ensure you're running from the `backend/` directory:

```bash
cd hotel_management_system/backend
python run.py
```

### Issue: "CORS error - Cannot read from API"

**Solution:**

Check that:
1. Backend is running
2. API_BASE_URL in `frontend/js/api.js` is correct
3. CORS is enabled in Flask (already enabled by default)

### Issue: "Database locked" error

**Solution:**

```bash
# Delete the database and restart backend
rm backend/database/hotel_management.db
python backend/run.py
```

### Issue: Login fails with correct credentials

**Solution:**

1. Check backend server is running
2. Clear browser cache and localStorage:
   ```javascript
   localStorage.clear()
   ```
3. Restart backend and try again

## Production Deployment

### Security Hardening

1. **Change JWT Secret Key**

Edit `backend/app/utils/auth.py`:

```python
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-very-secure-random-key-here')
```

2. **Use Environment Variables**

```bash
# .env file
export FLASK_ENV=production
export SECRET_KEY=your-production-secret-key
```

3. **Disable Debug Mode**

```python
app.run(debug=False)
```

### Deployment Options

#### Option 1: Heroku

```bash
# Create Procfile
echo "web: python backend/run.py" > Procfile

# Deploy
git push heroku main
```

#### Option 2: AWS/Digital Ocean

1. Install Gunicorn: `pip install gunicorn`
2. Run: `gunicorn -w 4 app:app`
3. Setup reverse proxy with Nginx

#### Option 3: Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "backend/run.py"]
```

## Backup & Recovery

### Regular Database Backup

```bash
# Copy database file
cp backend/database/hotel_management.db backend/database/hotel_management.db.backup

# Or use SQLite command
sqlite3 backend/database/hotel_management.db ".backup backup.db"
```

### Restore from Backup

```bash
# Stop backend
cp backend/database/hotel_management.db.backup backend/database/hotel_management.db

# Restart backend
python backend/run.py
```

## Performance Optimization

### Enable Caching

Add to `backend/app/__init__.py`:

```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
```

### Use Production Server

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Monitoring

### View Logs

Backend logs are printed to console. For file logging:

```python
# Add to backend/run.py
import logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)
```

### Monitor Database

```bash
# Check database size
ls -lh backend/database/hotel_management.db

# Check table counts
sqlite3 backend/database/hotel_management.db "SELECT COUNT(*) FROM sales;"
```

## Support

For detailed API documentation: See `API_DOCUMENTATION.md`
For database structure: See `DATABASE_SCHEMA.md`
