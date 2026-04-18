# Data Model (Canonical, MVP)

![Data Model](language-content-engine\docs\data\Feature Flag - Page 3.png)

## 1. Model Overview
Core entities:
- `users`
- `user_preferences`
- `videos`
- `analysis_jobs`
- `vocabulary_items`
- `user_vocabulary`
- `user_video_status`


## 3. Entities and Constraints

## 3.1 `users`
- `id` PK
- `email` VARCHAR(255) UNIQUE NOT NULL
- `password_hash` TEXT NOT NULL
- `created_at` TIMESTAMP NOT NULL default now
- `updated_at` TIMESTAMP NOT NULL default now

## 3.2 `user_preferences`
- `id` PK
- `user_id` FK -> users.id UNIQUE NOT NULL
- `target_language` VARCHAR(10) NOT NULL
- `current_level` VARCHAR(3) NOT NULL CHECK in (`A1`,`A2`,`B1`,`B2`,`C1`,`C2`)
- `interests` JSONB NOT NULL default `[]`
- `updated_at` TIMESTAMP NOT NULL

## 3.3 `videos`
- `id` PK
- `youtube_id` VARCHAR(20) UNIQUE NOT NULL
- `title` VARCHAR(500) NOT NULL
- `cefr_level` VARCHAR(3) NULL CHECK CEFR enum
- `confidence` FLOAT NULL CHECK (`confidence >= 0 AND confidence <= 1`)
- `topics` JSONB NOT NULL default `[]`
- `analyzed_at` TIMESTAMP NULL
- `created_at` TIMESTAMP NOT NULL
- `updated_at` TIMESTAMP NOT NULL

## 3.4 `analysis_jobs`
- `id` PK
- `job_id` VARCHAR(40) UNIQUE NOT NULL
- `video_id` FK -> videos.id NOT NULL
- `status` VARCHAR(20) NOT NULL CHECK in (`submitted`,`processing`,`completed`,`failed`)
- `retry_count` INTEGER NOT NULL default 0
- `failure_reason` TEXT NULL
- `submitted_at` TIMESTAMP NOT NULL
- `started_at` TIMESTAMP NULL
- `completed_at` TIMESTAMP NULL

## 3.5 `vocabulary_items`
- `id` PK
- `video_id` FK -> videos.id NOT NULL
- `word` VARCHAR(255) NOT NULL
- `translation` VARCHAR(255) NOT NULL
- `cefr_level` VARCHAR(3) NOT NULL CHECK CEFR enum
- `frequency` VARCHAR(20) NOT NULL CHECK in (`once`,`common`,`very common`)
- `example_sentence` TEXT NOT NULL
- `created_at` TIMESTAMP NOT NULL
- UNIQUE (`video_id`, `word`, `example_sentence`)

## 3.6 `user_vocabulary`
- `id` PK
- `user_id` FK -> users.id NOT NULL
- `vocabulary_id` FK -> vocabulary_items.id NOT NULL
- `saved_at` TIMESTAMP NOT NULL
- UNIQUE (`user_id`, `vocabulary_id`)

## 3.7 `user_video_status`
- `id` PK
- `user_id` FK -> users.id NOT NULL
- `video_id` FK -> videos.id NOT NULL
- `watched` BOOLEAN NOT NULL default false
- `watched_at` TIMESTAMP NULL
- UNIQUE (`user_id`, `video_id`)
