

# French Learning App   [WORK IN PROGRESS]

Making French learning active, not passive.

# Vocabulary learning Engine

**Summary: **
After obtaining a transcript from a Youtube Video, an LLM will analyse the text to extract 20 key words from the video. Users can save these words to a personalised list and export them into anki or CSV for continual learning. 

** Experiment**
First coding project that is AI-first.  This directory also includes my prompts to see how they evolve over time

## What It Does

Paste a French YouTube video URL. The app:
1. Extracts the transcript
2. Analyzes it with Claude AI to determine difficulty (CEFR A1-C2)
3. Extracts 20 key vocabulary words with translations, frequency, and example sentences
4. Lets you save words to a personal list
5. Exports your saved vocabulary to Anki or CSV for spaced repetition

**Why?** Watching French YouTube is great, but passive. Most learners don't extract value. This turns passive watching into active learning with minimal friction.

## Quick Start

### Backend
```bash
# From repo root
cd backend
python -m venv venv
source venv/bin/activate  # Windows PowerShell: venv\Scripts\Activate.ps1
pip install -r ../requirements.txt
cp .env.example .env       # Windows PowerShell: copy .env.example .env
python main.py
# In a second terminal (from backend/)
celery -A celery_app.celery_app worker --loglevel=info
```

Backend runs on `http://localhost:8000`

### Frontend 
```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`

## Stack

**Backend:** Python 3.11+ | FastAPI | PostgreSQL | Redis | Celery | Claude API  
**Frontend:** React 18 | Vite | Tailwind CSS | React Query  
**Deploy:** Railway/Render (backend) | Vercel (frontend)


## Learning Goals

This is a challenge to ship a  product while learning:
- Prompt engineering
- AI tool mastery 
- Building with AI 
- Shipping

See [CLAUDE.md](./CLAUDE.md) for the full technical spec and architecture.

## API Endpoints (MVP)

- `POST /api/analyze` — Analyze a YouTube video
- `GET /api/videos` — Get analyzed videos
- `POST /api/vocabulary/save` — Save a word
- `GET /api/vocabulary/saved` — Get saved words
- `POST /api/vocabulary/export` — Export to Anki/CSV

## Author

Built in April 2026 as a learning projoect
---

**See [backend/README.md](./backend/README.md) for backend setup details.**
