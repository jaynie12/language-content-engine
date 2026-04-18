# User Journeys (MVP)
## Journey 1: First-Time User Onboarding
1. User signs up with email/password.
2. User logs in and sets target language, current level, interests.
3. Home feed loads with recommendation videos from preferences.
4. User pastes first YouTube URL to start analysis.


### Success Criteria
- User reaches first analysis submission in under 2 minutes.
- Preferences persist and affect recommendation/filter defaults.


## Journey 2: Analyze Video End-to-End
1. User submits YouTube URL.
2. System validates URL and creates async analysis job.
3. User sees processing status and can refresh/poll.
4. On completion, detail page shows CEFR, confidence, topics, vocabulary.
5. User saves useful words from detail page.

### Exception Paths
- **E1 Invalid URL**: show validation error immediately; no job created.
- **E2 Transcript missing**: job fails with recoverable message and reason code.
- **E3 AI malformed output**: system retries once, then marks failed with diagnostic code.
- **E4 Dependency timeout**: job transitions to failed; user sees retry option.


## Journey 3: Save and Export Vocabulary
1. User selects vocabulary item in detail view.
2. User saves item to personal list.
3. User opens Saved Words page and filters by CEFR or date.
4. User exports list to CSV or Anki-compatible format.


### Success Criteria
- Duplicate saves are prevented cleanly.
- Export contains source video and context sentence per row.


## Journey 4: Browse, Search, and Watch Tracking
1. User opens browse page.
2. User applies filters (language, level, topic, duration, speed).
3. User performs text search on title.
4. User opens result detail and marks video as watched.
5. Future browse/recommendation experience reflects watched state.

### Exception Paths
- Empty result set returns explanatory empty-state UI.
- Unknown topic filter values are rejected at API layer.

## Journey 5: Personalized Recommendation Loop
1. User has preferences + watched history.

### Success Criteria
- Recommendation list stays aligned to selected level/interests.
- User can always access full browse mode if recommendation pool is small.
