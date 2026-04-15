# Product Requirements Specification (MVP)

## 1. Purpose
Build an MVP that turns passive YouTube language watching into active vocabulary learning through transcript ingestion, AI analysis, and personalized study workflows.

## 2. Scope
### In Scope
- Ingest YouTube video transcript and metadata.
- Detect spoken language and persist core video data.
- Run asynchronous AI analysis for CEFR level, topics, and key vocabulary.
- Support basic user accounts and preferences.
- Provide saved vocabulary list, watched status, and CSV/Anki export.
- Provide browse/search/filter/detail UI behaviors.

### Out of Scope (MVP)
- Social features (sharing, comments, groups).
- Native mobile app.
- Advanced recommendation ML beyond rule-based filtering.
- Multi-tenant enterprise controls.

## 3. Personas
- **P1 Solo Learner**: wants to quickly extract useful vocabulary from videos.
- **P2 Tutor Reviewer**: validates whether CEFR and vocabulary outputs are acceptable.

## 4. Product Objectives
- Reduce friction from video URL to learnable vocabulary list.
- Produce consistent CEFR/topic/vocabulary outputs with confidence scoring.
- Keep processing resilient and asynchronous.
- Make all major feature behavior testable via explicit acceptance criteria.

## 5. Assumptions and Constraints
- Stack: FastAPI, PostgreSQL, Redis, Celery, React, Anthropic API.
- Budget-sensitive AI usage with caching and reuse.
- MVP timeline prioritizes correctness and traceability over breadth.

## 6. Functional Requirements (MVP)

### Transcript and Metadata
- **FR-001**: System accepts a valid YouTube URL and extracts a normalized `youtube_id`.
- **FR-002**: System retrieves transcript text for supported languages and detects transcript language.
- **FR-003**: System stores video metadata (title, source identifiers, language) in database.
- **FR-004**: Transcript/analysis processing executes asynchronously via job pipeline.

### Content Analysis
- **FR-005**: System determines CEFR level (A1-C2) using transcript analysis.
- **FR-006**: System stores model confidence score for CEFR decision in range 0.0-1.0.
- **FR-007**: System identifies CEFR level and 3-5 topical tags for the video and stores this in the video meta data table
- **FR-008**: System extracts 20-30 key vocabulary items from transcript.
- **FR-009**: Each vocabulary item includes translation, frequency and an example sentence. If its a noun, store the feminine and plural versions of the word.
- **FR-010**: Extraction excludes low-learning-value stop words (articles/pronouns unless pedagogically required).

### User Interaction
- **FR-011**: User can sign up/login with email and password.
- **FR-012**: User can set and update target language, current CEFR level, and interests.
- **FR-013**: User can save vocabulary item to personal list from video context.
- **FR-014**: System shows saved list with word, translation, source video, context sentence, date saved.
- **FR-015**: User can export saved vocabulary to CSV; Anki-compatible export supported in MVP.

### UI and Discovery
- **FR-017**: Browse supports filters for language, CEFR level, topic, duration, speaking speed.
- **FR-018**: Search supports text search over video titles with level-preference-aware filtering.
- **FR-019**: Video detail page shows player, metadata, difficulty badge, topics, vocabulary list.
- **FR-020**: Homepage recommendations are filtered by user level and interests.

## 7. Non-Functional Requirements
- **NFR-001 Reliability**: Failed async jobs move to explicit failed state with reason.
- **NFR-002 Performance**: Analyze request acknowledges quickly (<2s) and returns job id.
- **NFR-003 Security**: Passwords are hashed; secrets stored in environment only.
- **NFR-004 Observability**: Structured logs include request id/job id and external dependency failures.
- **NFR-005 Data Quality**: CEFR enum, confidence range, and vocabulary cardinality are validated.
- **NFR-006 Privacy**: Only necessary user/profile data is stored for MVP.

## 8. Acceptance Boundary
MVP is complete when FR-001 to FR-020 meet acceptance criteria and strict Definition of Done checks in `docs/quality/definition-of-done.md`.
