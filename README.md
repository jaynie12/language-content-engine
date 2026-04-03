# Vocabulary learning Engine

**Summary: **
After obtaining a transcript from a Youtube Video, an LLM will analyse the text to extract 20 key words from the video. Users can save these words to a personalised list and export them into anki or CSV for continual learning. 

### Backend Stack:

- **Language:** Python 3.11+
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **Cache:** Redis
- **Queue:** Celery + Redis
- **AI:** OpenAI API or Anthropic Claude API
- **YouTube:** youtube-transcript-api, google-api-python-client

### Frontend Stack:

- **Framework:** React 18
- **Build:** Vite
- **Styling:** Tailwind CSS
- **State:** React Query
- **Routing:** React Router

### Infrastructure:

- **Backend Hosting:** Railway or Render
- **Frontend Hosting:** Vercel
- **Database:** Railway PostgreSQL
- **Redis:** Railway Redis or Upstash
- **File Storage:** S3
