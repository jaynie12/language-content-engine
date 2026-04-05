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

### Infrastructure (Deployment Day 22+)
- **Backend:** Railway or Render
- **Frontend:** Vercel
- **Database:** Railway PostgreSQL
- **Cache/Queue:** Railway Redis or Upstash
- **Files:** S3 (for exports, later)

---

## Architecture

### API Endpoints (MVP)
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
  transcript (TEXT)
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

### Small Test Group (Myself + Teacher)
- **No user auth Day 1-7.** Add single-user mode first.
- **Day 14+:** Add basic auth (email-only for now, no password complexity).
- **Feedback loop:** Teacher reviews output → I adjust prompts → iterate.
- **Metrics:** Accuracy of CEFR assignment, vocabulary relevance, false positives in extraction.

### Prompt Engineering Rules (All Weeks)
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

---

## Milestones

### Week 1 (Days 1-7): Backend Pipeline
- [DONE] Day 1: Project scaffold, first commit
- [ ] Day 2: YouTube transcript extraction working (CLI test)
- [ ] Day 3: First Claude API call, CLAUDE.md written
- [ ] Day 4: CEFR analysis prompt, iterate 5 times
- [ ] Day 5: Vocabulary extraction + prompt design with Claude's help
- [ ] Day 6: Full pipeline end-to-end (transcript → Claude → CEFR + vocab + topics)
- [ ] Day 7: Code review, README updated, push clean version

### Week 2 (Days 8-14): Frontend + Database
- [ ] Day 8: Basic React form + submit button
- [ ] Day 9: Display results on page
- [ ] Day 10: PostgreSQL schema designed, migrations written
- [ ] Day 11: Full loop: paste URL → process → store → display
- [ ] Day 12: Save vocabulary to user list (backend)
- [ ] Day 13: Saved words page + display
- [ ] Day 14: Show to mentor, gather feedback, update CLAUDE.md

### Week 3 (Days 15-21): Polish + Agents
- [ ] Day 15: Anki export (CSV generation)
- [ ] Day 16: Speaking speed indicator (from transcript timing)
- [ ] Day 17: UI polish (clean, intentional design)
- [ ] Day 18: Video detail page (full layout)
- [ ] Day 19: Filter by CEFR level
- [ ] Day 20: Error handling (missing transcripts, API failures, edge cases)
- [ ] Day 21: Full code review, clean commit

### Week 4 (Days 22-30): Ship + Document
- [ ] Day 22: Deploy to Railway/Render
- [ ] Day 23: Fix production issues
- [ ] Day 24: Add monitoring & logging
- [ ] Day 25: API documentation
- [ ] Day 26: Demo video (2 min screen record)
- [ ] Day 27: Substack post
- [ ] Day 28: GitHub polish (readme, repo story)
- [ ] Day 29: Show 3 people, gather feedback
- [ ] Day 30: Reflect + plan May

---

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

---

## Prompting Strategy for the Month

### Days 1-3: Foundation
- Give Claude your full stack + MVP spec
- Ask it to scaffold folder structure, dependencies
- Let it suggest database schema, ask for refinement

### Days 4-6: Prompt Iteration
- Write the CEFR analysis prompt → test → iterate 5 times
- Each iteration: explain what's wrong, let Claude suggest fixes
- Document all 5 versions in a `prompts/` folder

### Days 7-14: Architecture Review
- Ask Claude to review your codebase for structure, error handling
- Ask it questions about your own code: "Why did you suggest X?"
- Practice accepting/rejecting suggestions thoughtfully

### Days 15-21: System-Level Thinking
- Use Claude to design features before coding (video detail page, filtering)
- Ask it: "What could break here?" (adversarial testing)
- Use RAG thinking: "How would I query this data efficiently?"

### Days 22-30: Production Thinking
- "Help me debug this deployment error"
- "What should I monitor in this system?"
- "How would a senior engineer review this architecture?"

---

## Success Criteria (April 30)

1. **Live URL** — App accessible on the internet
2. **Working pipeline** — Paste URL → get results → save → export
3. **GitHub story** — Repo is clean, readme explains the build
4. **Substack post** — Document what you built, why, what you learned
5. **Interview-ready** — Can explain prompt engineering, Cursor usage, agent concepts with examples from this project
6. **Cost-efficient** — Token costs tracked, wasteful patterns identified

---

## Constraints You Accepted

- **Budget:** Minimal token spend (caching, truncation, batching)
- **Users:** Just you + teacher (no scale needed)
- **Time:** 30 days, 90 min build + 50 min learn daily
- **Dependencies:** No third-party NLP libraries (use Claude for all language tasks)

---

## What to Ask Claude Going Forward

### Good prompts for this project:
- "Here's my codebase. Review my [service name] for error handling."
- "I'm about to build [feature]. What could go wrong? Think through failure modes first."
- "Scaffold the [service/component] given this schema and my CLAUDE.md context."
- "I have 5 prompt versions. Here they are. Why is #3 the best?"
- "Help me design the database schema for [feature]. Ask me clarifying questions first."

### Bad prompts (avoid):
- "Build the whole app" (too vague)
- "Write better code" (no context)
- "Why doesn't this work?" (without error message + code)

---

**Last updated:** 4th April 2026
**Next review:** 11th April 2025
