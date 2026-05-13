import asyncio
import os

from app.db.session import AsyncSessionLocal, init_db
from app.seed_bootstrap import seed_demo_if_empty, wipe_and_seed


async def _run(*, force: bool) -> None:
    await init_db()
    async with AsyncSessionLocal() as session:
        if force:
            await wipe_and_seed(session)
        else:
            await seed_demo_if_empty(session)


def main() -> None:
    force = os.environ.get("SEED_FORCE", "").lower() in {"1", "true", "yes"}
    asyncio.run(_run(force=force))


if __name__ == "__main__":
    main()
