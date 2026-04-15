# MVP Feature Learning Plan

## Purpose
This is the single learning artifact for the project. Learning is only tracked when it directly supports implementation of active MVP features.

## How To Use This File
For each feature slice:
1. Link requirement IDs (`FR-*`).
2. Define build goal and implementation scope.
3. Capture architecture concepts applied in implementation.
4. Apply one Cursor rule, one skill, and one hook tied to the slice.
5. Record reflection outcomes and concrete project changes.
6. Mark strict DoD pass/fail for the slice.

## Slice Template
```markdown
### Slice X: <Feature Name>
- Requirements: FR-xxx, FR-yyy
- Build Goal:
- In-Scope Build Tasks:
- Architecture Concepts Applied:
- Cursor Rule Used:
- Cursor Skill Used:
- Cursor Hook Used:
- Reflection:
  - What worked:
  - What failed:
  - What changed in design:
- DoD Result: pass/fail
```

## Slice 1: Transcript + Metadata + Async Processing
- Requirements: `FR-001`, `FR-002`, `FR-003`, `FR-004`
- Build Goal: accept URL, fetch transcript/metadata, and process analysis asynchronously.
- In-Scope Build Tasks:
  - URL validation and canonical `youtube_id` extraction.
  - Metadata/transcript persistence fields.
  - Async job enqueue, status transitions, failure reason capture.
- Architecture Concepts Applied:
  - API accept-then-process pattern.
  - Queue/worker separation of concerns.
  - Idempotent persistence for repeated submissions.
- Cursor Rule Used: backend async/error-handling rule for `backend/**/*.py`.
- Cursor Skill Used: async API contract drafting skill.
- Cursor Hook Used: post-edit quality check hook for backend files.
- Reflection:
  - What worked: clear `submitted -> processing -> completed/failed` model.
  - What failed: dependency failures need normalized error mapping.
  - What changed in design: added explicit `analysis_jobs` entity.
- DoD Result: pending

## Slice 2: Analyze Content (CEFR, topics, vocabulary)
- Requirements: `FR-005`, `FR-006`, `FR-007`, `FR-008`, `FR-009`, `FR-010`
- Build Goal: produce validated CEFR/topic/vocabulary outputs from transcript.
- In-Scope Build Tasks:
  - CEFR with confidence validation.
  - Topic extraction and persistence.
  - Vocabulary extraction with quality constraints (20-30 useful words).
- Architecture Concepts Applied:
  - Structured AI output validation.
  - Domain constraints at API + data layers.
  - Retry/fail strategy for malformed model output.
- Cursor Rule Used: AI validation standards rule.
- Cursor Skill Used: AI-output acceptance criteria skill.
- Cursor Hook Used: notify when analysis logic changes without docs updates.
- Reflection:
  - What worked:
  - What failed:
  - What changed in design:
- DoD Result: pending

## Slice 3: User Interaction (account, saved list, export, watched)
- Requirements: `FR-011`, `FR-012`, `FR-013`, `FR-014`, `FR-015`, `FR-016`
- Build Goal: support account basics, preference storage, saved vocabulary workflows, and watched state.
- In-Scope Build Tasks:
  - Signup/login and preference endpoints.
  - Save/list vocabulary and export format support.
  - Watched state persistence.
- Architecture Concepts Applied:
  - Ownership and access boundaries on user data.
  - Relational integrity for save/watch associations.
  - Export pipeline reliability and format correctness.
- Cursor Rule Used: user-data integrity and traceability rule.
- Cursor Skill Used: user-story to acceptance criteria skill.
- Cursor Hook Used: migration-impact review hook.
- Reflection:
  - What worked:
  - What failed:
  - What changed in design:
- DoD Result: pending

## Slice 4: Browse, Search, Detail, Personalization
- Requirements: `FR-017`, `FR-018`, `FR-019`, `FR-020`
- Build Goal: deliver searchable/filterable browse and preference-aligned recommendations.
- In-Scope Build Tasks:
  - Filter/search query behavior.
  - Video detail integration.
  - Recommendation filtering by level/interests.
- Architecture Concepts Applied:
  - Query design with indexed filtering.
  - Frontend state boundaries for server state vs UI state.
  - Contract alignment between frontend expectations and API response models.
- Cursor Rule Used: docs/journey update rule for filter/contract changes.
- Cursor Skill Used: journey-to-endpoint mapping skill.
- Cursor Hook Used: schema/route change documentation reminder hook.
- Reflection:
  - What worked:
  - What failed:
  - What changed in design:
- DoD Result: pending

## Reflection and ADR Review Loop (Used For Every Slice)
1. End each implementation slice by completing its reflection section in this file.
2. If reflection identifies architecture-impacting change, create/update one ADR in `docs/architecture/adr/`.
3. Link ADR id back to the slice entry.
4. Update relevant docs (`requirements`, `api`, `data`, `ux`, `traceability`) in the same change set.
5. Re-run strict DoD checks and set final pass/fail.

### Reflection Questions (Mandatory)
- Which architectural pattern was used and why?
- Which requirement or acceptance criterion was hardest to satisfy?
- What failure mode was discovered during implementation?
- What concrete design change was made because of this learning?
