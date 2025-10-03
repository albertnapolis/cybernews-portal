# Cybersecurity News Portal

A full-stack web application for aggregating and displaying cybersecurity news from multiple trusted sources.

## Features

- **Real-time News Aggregation**: Automatically fetches news from multiple RSS feeds
- **Advanced Filtering**: Filter by severity, category, source, and time range
- **Search Functionality**: Full-text search across titles and descriptions
- **Severity Classification**: Automatic classification of news by severity (Critical, High, Medium, Low, Info)
- **Category Management**: Organize news into categories (Vulnerabilities, Data Breaches, Malware, etc.)
- **Responsive Design**: Mobile-friendly interface using Bootstrap
- **RESTful API**: Well-structured backend API with FastAPI

## Tech Stack

### Backend
- **Python 3.8+**
- **FastAPI** - Modern web framework
- **SQLAlchemy** - ORM for database management
- **SQLite** - Database (can be easily switched to PostgreSQL)
- **feedparser** - RSS feed parsing
- **BeautifulSoup4** - HTML content extraction

### Frontend
- **Vue.js 3** - Progressive JavaScript framework
- **Vite** - Build tool and dev server
- **Pinia** - State management
- **Vue Router** - Client-side routing
- **Bootstrap 5** - CSS framework
- **Axios** - HTTP client

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd cybersecurity-portal/backend
```

2. Create a virtual environment:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

5. Run the backend server:
```bash
# Using the management script (recommended)
python manage_server.py start    # Start server
python manage_server.py stop     # Stop server
python manage_server.py restart  # Restart server

# Simple run
python simple_run.py

# On Windows, use batch files:
start_server.bat    # Start server
stop_server.bat     # Stop server
restart_server.bat  # Restart server

# Or using uvicorn directly:
python -m uvicorn main:app --reload
```

**Note:** If you get "port already in use" error, use `python manage_server.py restart` or `restart_server.bat`

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd cybersecurity-portal/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file:
```bash
echo "VITE_API_URL=http://localhost:8000/api/v1" > .env
```

4. Run the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## API Endpoints

### News
- `GET /api/v1/news` - Get paginated news articles
- `GET /api/v1/news/{id}` - Get specific article
- `GET /api/v1/news/latest/critical` - Get critical severity news
- `GET /api/v1/news/trending` - Get trending news
- `POST /api/v1/news/refresh` - Manually refresh feeds

### Categories
- `GET /api/v1/categories` - Get all categories
- `GET /api/v1/categories/{id}` - Get specific category
- `GET /api/v1/categories/slug/{slug}` - Get category by slug

### Sources
- `GET /api/v1/sources` - Get all news sources
- `GET /api/v1/sources/{id}` - Get specific source
- `PUT /api/v1/sources/{id}/toggle` - Toggle source active status

## Usage

1. **Initial Data Load**: On first run, the application will initialize default RSS feed sources and categories.

2. **Refresh Feeds**: Click the "Refresh Feeds" button on the homepage to manually fetch latest news.

3. **Filtering**: Use the filter bar to narrow down news by:
   - Severity level (Critical, High, Medium, Low, Info)
   - Category (Vulnerabilities, Data Breaches, etc.)
   - News source
   - Time range (Last 24 hours, Last week, etc.)
   - Search keywords

4. **View Details**: Click on any news article to view full details and access the original source.

## RSS Feed Sources

The application aggregates news from:
- The Hacker News
- SecurityWeek
- Krebs on Security
- ThreatPost
- Dark Reading
- BleepingComputer
- CISA Alerts
- Zero Day Initiative

## Development

### Adding New RSS Sources

Edit `app/core/config.py` and add new sources to the `RSS_FEEDS` list:

```python
RSS_FEEDS = [
    {"name": "Source Name", "url": "https://example.com/feed", "category": "general"},
    # ... more sources
]
```

### Running Tests

Backend:
```bash
cd cybersecurity-portal/backend
pytest
```

Frontend:
```bash
cd cybersecurity-portal/frontend
npm run test
```

## Deployment

### Backend Deployment

1. Update `.env` with production settings
2. Use a production database (PostgreSQL recommended)
3. Deploy using Docker or a platform like Heroku/AWS

### Frontend Deployment

1. Build for production:
```bash
npm run build
```

2. Deploy the `dist` folder to:
   - Netlify
   - Vercel
   - AWS S3 + CloudFront
   - Any static hosting service

## Security Considerations

- All fetched content is sanitized to prevent XSS attacks
- API endpoints use proper validation
- CORS is configured for production domains
- Environment variables for sensitive configuration
- Rate limiting should be implemented for production

## License

MIT License

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.