# French Learning App — Backend

FastAPI backend for French YouTube analysis. Extracts transcripts, analyzes with Claude, extracts vocabulary.

## Quick Start

### 1. Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy .env template and add your API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 2. Database Setup (PostgreSQL)

```bash
# Install PostgreSQL locally or use Railway/Render for remote

# Create database
createdb french_app_db

# Or update .env with your database URL if using remote
DATABASE_URL=postgresql://user:password@localhost:5432/french_app_db
```

For development without PostgreSQL, you can use SQLite:
```
DATABASE_URL=sqlite:///./french_app.db
```

### 3. Redis Setup (for caching and Celery)

```bash
# Install Redis locally or use Upstash/Railway for remote

# Start Redis (local)
redis-server

# Or update .env with remote URL
REDIS_URL=redis://localhost:6379/0
```

### 4. Run the App

```bash
# Development server
python main.py

# Or with uvicorn directly
uvicorn main:app --reload

# Server runs on http://localhost:8000
```

Visit `http://localhost:8000/docs` for interactive API documentation.

---

## Project Structure

```
backend/
├── main.py                  # FastAPI app entry point
├── config.py               # Settings from .env
├── database.py             # SQLAlchemy setup
├── models.py               # ORM models (User, Video, Vocabulary)
├── schemas.py              # Pydantic request/response models
├── services/
│   ├── youtube_service.py  # Fetch YouTube transcripts
│   ├── claude_service.py   # Claude API calls (prompts)
│   └── vocabulary_service.py # Extraction logic (Day 5)
├── routes/
│   ├── analyze.py          # POST /api/analyze
│   ├── vocabulary.py       # Vocabulary endpoints
│   └── videos.py           # Video history
├── tasks/
│   └── celery_tasks.py     # Async job processing (Day 22+)
├── requirements.txt
├── .env.example
└── README.md
```

---

## API Endpoints (MVP)

### Analysis
- **POST** `/api/analyze` — Analyze a YouTube video
  ```json
  {
    "url": "https://www.youtube.com/watch?v=..."
  }
  ```
  Returns: `{ video_id, title, cefr_level, confidence, vocabulary: [...], topics: [...] }`

### Videos
- **GET** `/api/videos` — List analyzed videos (paginated)
- **GET** `/api/videos/{id}` — Get video details

### Vocabulary
- **POST** `/api/vocabulary/save` — Save word to user list
- **GET** `/api/vocabulary/saved` — Get user's saved words
- **POST** `/api/vocabulary/export` — Export to Anki or CSV

---

## Development

### Running Tests (Coming Day 15+)

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest -v
```

### Code Quality

```bash
# Format code
black . --line-length 100

# Linting
flake8 .

# Type checking
mypy .
```

---

## Environment Variables

See `.env.example`. Key ones:

- `ANTHROPIC_API_KEY` — Your Claude API key (required)
- `DATABASE_URL` — PostgreSQL connection string
- `REDIS_URL` — Redis connection string
- `YOUTUBE_API_KEY` — Optional, for extended metadata
- `DEBUG` — True for development
- `FRONTEND_URL` — CORS origin for React frontend
- `TRACK_TOKENS` — Log token usage (cost tracking)

---

## Cost Optimization

The app implements several strategies to minimize Claude API costs:

1. **Caching** — Store analyzed transcripts in DB, don't re-analyze
2. **Truncation** — Clip transcripts at reasonable length (context window efficiency)
3. **Batching** — Group requests when possible
4. **Token logging** — Track usage per request to identify waste
5. **Model selection** — Using Claude 3.5 Sonnet (better price/performance than Opus)

See `config.py` and `services/claude_service.py` for implementation.

---

## Database Schema (simplified)

```sql
users (id, email, created_at)
videos (id, user_id, youtube_id, title, transcript, cefr_level, confidence, topics, analyzed_at)
vocabulary_items (id, video_id, word, translation, cefr_level, frequency, example_sentence)
user_vocabulary (id, user_id, vocabulary_id, in_anki, saved_at)
```

Full schema in `models.py`.

---

## Deployment

See main project README for Railway/Render deployment steps.

---
