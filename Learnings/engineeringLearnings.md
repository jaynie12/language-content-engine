Learning Notes during phase 1:

Concepts used: 

BaseSettings multi-file env loading; 
Celery app bootstrap with centralized config.

Patterns worth learning: 

configuration layering (fallback env files)
separation of runtime bootstrap (celery_app.py) from task logic.

Advanced alternative: 
move to package-style imports (backend.config) plus pyproject.toml for cleaner root-level execution and tooling consistency.