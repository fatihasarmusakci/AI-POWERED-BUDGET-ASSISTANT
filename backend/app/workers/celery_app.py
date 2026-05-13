from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "vibecheck",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

celery_app.conf.update(
    task_always_eager=settings.celery_eager,
    task_eager_propagates=True,
)

import app.workers.tasks  # noqa: E402,F401
