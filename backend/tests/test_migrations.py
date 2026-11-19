import os

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import text

from app.db import make_engine

pytestmark = [
    pytest.mark.db,
    pytest.mark.skipif("DATABASE_URL" not in os.environ, reason="DATABASE_URL not set"),
]

ALEMBIC_INI = os.path.join(os.path.dirname(__file__), "..", "alembic.ini")


def test_migrations_upgrade_and_downgrade_cleanly() -> None:
    cfg = Config(ALEMBIC_INI)
    command.upgrade(cfg, "head")
    command.downgrade(cfg, "base")
    command.upgrade(cfg, "head")


def test_pgvector_extension_enabled() -> None:
    cfg = Config(ALEMBIC_INI)
    command.upgrade(cfg, "head")
    engine = make_engine()
    try:
        with engine.connect() as conn:
            version = conn.execute(
                text("SELECT extversion FROM pg_extension WHERE extname = 'vector'")
            ).scalar()
    finally:
        engine.dispose()
    assert version is not None
