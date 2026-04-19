"""
Celery application bootstrap.
Phase 1: provides deterministic worker startup wiring.
"""

from celery import Celery
from config import settings


celery_app = Celery(
    "language_content_engine",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)
