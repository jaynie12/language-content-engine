# Requirements Traceability Matrix (MVP)

## 1. Feature Traceability
| Requirement | API Contract | Data Model | User Journey | Architecture Component |
|---|---|---|---|---|
| FR-001..FR-004 | `/api/analyze`, `/api/analyze/{job_id}` | `videos`, `analysis_jobs` | Analyze Video | FastAPI + Celery Worker |
| FR-005..FR-010 | `/api/videos/{video_id}` | `videos`, `vocabulary_items` | Analyze Video | AnalysisOrchestrator + AI integration |
| FR-011..FR-012 | `/api/auth/*`, `/api/users/me/preferences` | `users`, `user_preferences` | Onboarding | AuthAndPreferences |
| FR-013..FR-015 | `/api/vocabulary/*` | `user_vocabulary`, `vocabulary_items` | Save and Export | VocabularyService |
| FR-016 | `/api/videos/{video_id}/watched` | `user_video_status` | Browse and Watch | FastAPI + DB |
| FR-017..FR-020 | `/api/videos` | `videos`, `user_preferences`, `user_video_status` | Browse/Search/Recommend | React UI + Query APIs |

## 2. Non-Functional Traceability
| NFR | Enforced By | Evidence |
|---|---|---|
| NFR-001 Reliability | `analysis_jobs` state model + retry policy | Async job tests and failure-state logs |
| NFR-002 Performance | Async submit/acknowledge flow | 202 response latency checks |
| NFR-003 Security | Password hashing + validated auth flows | Auth tests + config validation |
| NFR-004 Observability | Structured logs with job/request IDs | Log examples and runbook notes |
| NFR-005 Data Quality | CEFR/confidence/vocab validation rules | Validation tests + schema constraints |
| NFR-006 Privacy | Minimal profile data and controlled exports | Data inventory review |

## 3. Documentation Traceability
- Requirements source: `docs/requirements/product-requirements-spec.md`
- DoD and release gates: `docs/quality/definition-of-done.md`
- API source of truth: `docs/api/api-contracts.md`
- Data source of truth: `docs/data/data-model.md`
- Journey source of truth: `docs/ux/user-journeys.md`
- Architecture source of truth: `docs/architecture/system-architecture.md`
