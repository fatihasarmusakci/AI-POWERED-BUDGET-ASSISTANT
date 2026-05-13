import os

os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./.pytest_vibecheck.db")
os.environ.setdefault("SYNC_DATABASE_URL", "sqlite:///./.pytest_vibecheck.db")
os.environ.setdefault("CELERY_EAGER", "true")


def pytest_configure(config):  # noqa: ARG001
    try:
        os.remove(".pytest_vibecheck.db")
    except OSError:
        pass
