# CLAUDE.md — French Learning App System Context

## Project Overview
**Name:** French Learning App  
**Purpose:** Make YouTube French learning passive → active. Users paste a video URL, get AI-extracted vocabulary + difficulty analysis, save words, export to Anki/CSV for spaced repetition.  
**Stage:** MVP (Days 1-30 April)  
**User:** Solo learner (myself) + French teacher for feedback. Small test group.

---

## Stack (Locked for April)

### Backend
- **Language:** Python 3.11+
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **Cache:** Redis
- **Queue:** Celery + Redis (async tasks)
- **AI Client:** Anthropic Claude API (cost-optimized)
- **YouTube:** youtube-transcript-api, google-api-python-client

### Frontend
- **Framework:** React 18
- **Build:** Vite
- **Styling:** Tailwind CSS
- **State:** React Query (for server state sync)
- **Routing:** React Router v6

### Infrastructure for Deployment
- **Backend:** Railway or Render
- **Frontend:** Vercel
- **Database:** Railway PostgreSQL
- **Cache/Queue:** Railway Redis or Upstash
- **Files:** S3 (for exports, later
---

## Architecture

### API Endpoints
```
POST /api/analyze
  Input: { url: "https://youtube.com/..." }
  Output: { 
    video_id, 
    title, 
    cefr_level, 
    confidence,
    vocabulary: [{ word, translation, cefr, frequency, example_sentence }],
    topics: [string]
  }

GET /api/videos
  Output: List of analyzed videos (paginated)

POST /api/vocabulary/save
  Input: { video_id, word }
  Output: { saved: true, user_word_id }

GET /api/vocabulary/saved
  Output: List of user's saved words

POST /api/vocabulary/export
  Input: { format: "anki" | "csv" }
  Output: File download
```

### Data Model (PostgreSQL)
```
users
  id (PK)
  email
  created_at

videos
  id (PK)
  youtube_id (UNIQUE)
  title
  analyzed_at
  cefr_level
  confidence
  topics (JSONB array)

vocabulary_items
  id (PK)
  video_id (FK)
  word
  translation
  cefr_level
  frequency
  example_sentence
  created_at

user_vocabulary
  id (PK)
  user_id (FK)
  vocabulary_id (FK)
  saved_at
  in_anki (BOOLEAN)
```

---

## Constraints & Design Decisions

### Cost Optimization (Token Budget)
- **Problem:** Claude API costs scale with token usage. Transcripts are long.
- **Solution:**
  1. Cache transcripts in Redis (don't re-fetch)
  2. Only send transcript to Claude once per video
  3. Store CEFR + vocabulary results in DB (reuse analysis)
  4. Use Celery for async processing (don't block user)
  5. Batch requests when possible
- **Monitoring (Day 24):** Track tokens/cost per request, log to identify waste

### Small Test Group 
- **No user auth Day 1-7.** Add single-user mode first.
- **Day 14+:** Add basic auth (email-only for now, no password complexity).
- **Feedback loop:** Teacher reviews output → I adjust prompts → iterate.
- **Metrics:** Accuracy of CEFR assignment, vocabulary relevance, false positives in extraction.

### Prompt Engineering Rules 
1. **System prompt** = Define the role, constraints, output format
2. **User prompt** = The actual transcript + analysis task
3. **XML tags** = Wrap structured data (`<transcript>`, `<vocabulary>`, `<topics>`)
4. **Few-shot examples** = Include 2-3 examples of desired output
5. **Temperature:** 0.3 for vocabulary extraction (deterministic), 0.7 for topic inference
6. **Token limits:** Assume 200k context window for Sonnet; clip transcripts if >150k tokens
7. **Validation:** Parse JSON response, validate CEFR levels against known set (A1-C2), reject malformed output

---

## Coding Conventions

### Python (Backend)
- **Typing:** Every function has type hints
- **Error handling:** Custom exceptions for API errors, database errors, Claude errors
- **Logging:** Structured logging with context (user_id, video_id, tokens_used)
- **Async:** Use `async`/`await` for I/O (database, API calls, Redis)
- **Environment:** `.env` for secrets; `python-dotenv` to load
- **Testing:** Unit tests for prompt logic, integration tests for full pipeline (not Day 1, add Day 15+)

### React (Frontend)
- **Components:** Functional, hooks-based, one component per file
- **State:** React Query for server state, useState only for UI state (input fields, modals)
- **Styling:** Tailwind utility classes, no custom CSS initially
- **Errors:** Toast notifications for user feedback (use library like `sonner` or `react-hot-toast`)
- **API calls:** Wrapped in React Query `useQuery` / `useMutation` hooks

### Database Migrations
- **Day 10:** Design schema
- **Day 22+:** Add migration tool (Alembic for SQLAlchemy or raw SQL with version tracking)

## Key Files & Their Roles

```
french-learning-app/
├── backend/
│   ├── main.py                 # FastAPI app entry
│   ├── config.py               # Settings, env vars
│   ├── models.py               # SQLAlchemy ORM
│   ├── schemas.py              # Pydantic request/response
│   ├── database.py             # DB connection, session
│   ├── services/
│   │   ├── youtube_service.py  # Transcript fetching
│   │   ├── claude_service.py   # Claude API calls (prompts here)
│   │   └── vocabulary_service.py # Extraction logic
│   ├── routes/
│   │   ├── analyze.py          # POST /api/analyze
│   │   ├── vocabulary.py       # Vocabulary endpoints
│   │   └── videos.py           # Video history
│   ├── tasks/
│   │   └── celery_tasks.py     # Async processing
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── UrlInput.jsx
│   │   │   ├── Results.jsx
│   │   │   ├── VocabularyList.jsx
│   │   │   └── SavedWords.jsx
│   │   ├── hooks/
│   │   │   └── useAnalyze.js   # React Query hook
│   │   ├── services/
│   │   │   └── api.js          # Axios/fetch client
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   └── README.md
├── .gitignore
├── CLAUDE.md                   # THIS FILE
└── README.md                   # Project overview
```


## Constraints You Accepted

- **Budget:** Minimal token spend (caching, truncation, batching)
- **Users:** Just you + teacher (no scale needed)
- **Dependencies:** No third-party NLP libraries (use Claude for all language tasks)


**Last updated:** 4th April 2026
**Next review:** 11th April 2025
