# Definition of Done (Strict, MVP)

## 1. Global DoD (Applies To Every Feature)
- Requirement IDs are linked (`FR-*`, `NFR-*`) and acceptance criteria are measurable.
- API contracts updated with request/response/error examples.
- Data model/migration impact documented before merge.
- Async behavior defined where applicable (status, retry, timeout, failure reason).
- Error handling includes user-safe message + internal structured log context.
- Tests added/updated (unit and integration/API contract level for affected scope).
- Security checks applied (input validation, auth checks, secret handling, password hashing).
- Observability updated (key logs, job states, failure metrics).
- User journey and traceability docs updated.

## 2. Feature Acceptance Criteria (Given/When/Then)

### Transcript + Metadata + Async
- **AC-FR-001**
  - Given a valid YouTube URL
  - When analysis is requested
  - Then system extracts and stores canonical `youtube_id`.
- **AC-FR-002**
  - Given a video with transcript
  - When transcript is fetched
  - Then transcript language is identified and stored.
- **AC-FR-003**
  - Given metadata fetch succeeds
  - When persistence runs
  - Then video metadata record is created/updated exactly once.
- **AC-FR-004**
  - Given analysis request is submitted
  - When API responds
  - Then API returns job id and processing continues asynchronously.

### AI Analysis
- **AC-FR-005/006**
  - Given transcript text
  - When CEFR analysis completes
  - Then CEFR is one of `A1..C2` and confidence is in `[0.0,1.0]`.
- **AC-FR-007**
  - Given transcript text
  - When topic extraction completes
  - Then 3-5 topic tags are stored.
- **AC-FR-008/009/010**
  - Given transcript text
  - When vocabulary extraction completes
  - Then 20-30 learnable entries are stored with required fields and stop-word filtering.

### User Interaction
- **AC-FR-011/012**
  - Given user registration/login flow
  - When credentials and preferences are submitted
  - Then account is authenticated and preferences are persisted.
- **AC-FR-013/014**
  - Given video vocabulary item
  - When user saves item
  - Then personal list shows complete saved entry details.
- **AC-FR-015**
  - Given saved vocabulary list
  - When export is requested
  - Then downloadable CSV/Anki-compatible output is generated.

### UI and Discovery
- **AC-FR-017**
  - Given browse page
  - When filters are applied
  - Then results reflect all selected criteria.
- **AC-FR-018**
  - Given search text
  - When search executes
  - Then title matches are returned and filtered by user level preferences.
- **AC-FR-019**
  - Given a selected video
  - When detail page loads
  - Then player, metadata, CEFR badge, topics, and vocabulary are shown.
- **AC-FR-020**
  - Given user preferences
  - When homepage recommendations load
  - Then recommendations align to selected level and interests.

## 3. Release Gates (Must Pass)
- `RG-001` No unresolved critical defects in MVP feature scope.
- `RG-002` DoD checklist completed for all changed features.
- `RG-003` Contract and schema docs are current and reviewed.
- `RG-004` Async failure paths tested (timeout, upstream failure, malformed AI output).
- `RG-005` Security baseline validated (auth, input validation, secret handling).
- `RG-006` Observability baseline validated (logs and job-state visibility).

## 4. Evidence Required Before Marking Done
- Linked pull request notes referencing `FR-*` and `AC-*`.
- Test results for impacted modules.
- Updated docs in requirements/API/data/UX/traceability.
- ADR entry if architectural behavior changed.
