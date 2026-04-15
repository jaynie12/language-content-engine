# System Architecture (MVP)

## 1. System Context
```mermaid
flowchart LR
  learner[LanguageLearner] --> frontend[ReactFrontend]
  frontend --> api[FastAPIBackend]
  api --> postgres[(PostgreSQL)]
  api --> redis[(Redis)]
  api --> worker[CeleryWorker]
  worker --> ytApi[YouTubeTranscriptAPI]
  worker --> aiApi[AnthropicClaudeAPI]
  worker --> postgres
```

## 2. Container/Component View
```mermaid
flowchart TB
  subgraph client [ClientLayer]
    ui[ReactUI]
  end

  subgraph app [ApplicationLayer]
    gateway[FastAPIEndpoints]
    auth[AuthAndPreferences]
    analysisOrchestrator[AnalysisOrchestrator]
    vocabService[VocabularyService]
  end

  subgraph asyncLayer [AsyncLayer]
    queue[CeleryQueue]
    jobWorker[CeleryWorkers]
  end

  subgraph dataLayer [DataLayer]
    db[(PostgreSQL)]
    cache[(Redis)]
  end

  subgraph externals [ExternalDependencies]
    youtube[YouTubeServices]
    claude[ClaudeModelAPI]
  end

  ui --> gateway
  gateway --> auth
  gateway --> analysisOrchestrator
  gateway --> vocabService
  analysisOrchestrator --> queue
  queue --> jobWorker
  jobWorker --> youtube
  jobWorker --> claude
  gateway --> db
  auth --> db
  vocabService --> db
  analysisOrchestrator --> db
  analysisOrchestrator --> cache
  jobWorker --> db
  jobWorker --> cache
```

## 3. Sequence: Async Transcript + Analysis Flow
```mermaid
sequenceDiagram
  participant User
  participant Frontend
  participant API
  participant Queue
  participant Worker
  participant YouTube
  participant Claude
  participant DB

  User->>Frontend: Submit video URL
  Frontend->>API: POST /api/analyze
  API->>DB: Upsert video record
  API->>Queue: Enqueue analysis job
  API-->>Frontend: 202 submitted + job_id
  Queue->>Worker: Deliver job
  Worker->>YouTube: Fetch transcript and metadata
  Worker->>Claude: Run CEFR/topics/vocabulary analysis
  Worker->>DB: Persist analysis results
  Worker->>DB: Mark job completed
  Frontend->>API: GET /api/analyze/{job_id}
  API-->>Frontend: completed + video_id
```

## 4. Sequence: Save Vocabulary and Export
```mermaid
sequenceDiagram
  participant User
  participant Frontend
  participant API
  participant DB

  User->>Frontend: Save vocabulary item
  Frontend->>API: POST /api/vocabulary/save
  API->>DB: Insert user_vocabulary
  API-->>Frontend: saved=true
  User->>Frontend: Export list
  Frontend->>API: POST /api/vocabulary/export
  API->>DB: Query saved items
  API-->>Frontend: downloadable file response
```

## 5. Architectural Principles
- API contract-first before implementation.
- Asynchronous processing for long-running transcript/AI operations.
- Data integrity through explicit constraints and idempotent writes.
- Observability and failure transparency across async boundaries.
- Feature traceability from requirements to components and tests.
