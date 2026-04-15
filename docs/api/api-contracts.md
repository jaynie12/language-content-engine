# API Contracts (MVP)

## 1. Conventions
- Base path: `/api`
- Content type: `application/json`
- Error envelope:

```json
{
  "error": {
    "code": "string_code",
    "message": "Human readable message",
    "details": {}
  }
}
```

## 2. Async Analysis Workflow
### Job States
- `submitted`: request accepted.
- `processing`: worker is running.
- `completed`: results persisted and available.
- `failed`: terminal failure with reason.

### State Rules
- Transition allowed: `submitted -> processing -> completed|failed`
- `failed` and `completed` are terminal.
- Retry creates a new job id, preserves source video linkage.

## 3. Endpoint Catalog

## 3.1 Submit Video Analysis
- **POST** `/api/analyze`
- **Maps**: `FR-001..FR-010`, `NFR-002`
- **Request**

```json
{
  "url": "https://www.youtube.com/watch?v=abc123def45"
}
```

- **202 Response**

```json
{
  "job_id": "job_01HQ...",
  "status": "submitted",
  "youtube_id": "abc123def45"
}
```

- **Errors**
  - `400 invalid_url`
  - `422 unsupported_input`
  - `503 dependency_unavailable`

## 3.2 Get Analysis Job Status
- **GET** `/api/analyze/{job_id}`
- **Maps**: `FR-004`, `NFR-001`
- **200 Response**

```json
{
  "job_id": "job_01HQ...",
  "status": "processing",
  "submitted_at": "2026-04-15T20:00:00Z",
  "updated_at": "2026-04-15T20:00:10Z",
  "failure_reason": null
}
```

- **Errors**
  - `404 job_not_found`

## 3.3 Get Video Detail (Analysis Result)
- **GET** `/api/videos/{video_id}`
- **Maps**: `FR-003`, `FR-005..FR-010`, `FR-019`
- **200 Response**

```json
{
  "video_id": 12,
  "youtube_id": "abc123def45",
  "title": "French Conversation Practice",
  "language": "fr",
  "cefr_level": "B1",
  "confidence": 0.81,
  "topics": ["voyage", "culture", "conversation"],
  "duration_seconds": 670,
  "views": 21000,
  "vocabulary": [
    {
      "id": 1,
      "word": "voyage",
      "translation": "travel",
      "cefr_level": "A2",
      "frequency": "common",
      "example_sentence": "Nous parlons de voyage en France."
    }
  ]
}
```

## 3.4 List Videos (Browse/Search/Filter)
- **GET** `/api/videos`
- **Maps**: `FR-017`, `FR-018`, `FR-020`
- **Query Params**
  - `q`, `language`, `cefr_min`, `cefr_max`, `topics[]`, `duration_band`, `speed_band`, `watched`, `page`, `page_size`
- **200 Response**

```json
{
  "items": [],
  "page": 1,
  "page_size": 20,
  "total": 0
}
```

## 3.5 Auth (Basic)
- **POST** `/api/auth/signup`
- **POST** `/api/auth/login`
- **Maps**: `FR-011`, `NFR-003`

## 3.6 User Preferences
- **GET** `/api/users/me/preferences`
- **PUT** `/api/users/me/preferences`
- **Maps**: `FR-012`

## 3.7 Save Vocabulary
- **POST** `/api/vocabulary/save`
- **Maps**: `FR-013`
- **Request**

```json
{
  "video_id": 12,
  "vocabulary_id": 1
}
```

## 3.8 List Saved Vocabulary
- **GET** `/api/vocabulary/saved`
- **Maps**: `FR-014`

## 3.9 Export Vocabulary
- **POST** `/api/vocabulary/export`
- **Maps**: `FR-015`
- **Request**

```json
{
  "format": "csv",
  "filters": {
    "cefr_max": "B2"
  }
}
```

## 3.10 Mark Video Watched
- **POST** `/api/videos/{video_id}/watched`
- **Maps**: `FR-016`

## 4. Error Code Registry
- `invalid_url`
- `job_not_found`
- `video_not_found`
- `validation_error`
- `unauthorized`
- `forbidden`
- `dependency_unavailable`
- `ai_output_invalid`
- `export_failed`

## 5. Contract Quality Checks
- Every endpoint includes requirement mapping.
- Every async endpoint defines status model and terminal states.
- Every write endpoint defines idempotency strategy.
