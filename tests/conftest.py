"""Shared test fixtures — temporary database for isolation."""

from __future__ import annotations

import pytest

import dreamtraffic.db.engine as engine
from dreamtraffic.db.migrations import init_db


@pytest.fixture(autouse=True)
def test_db(tmp_path):
    """Create a fresh database for each test, set as the global connection."""
    db_path = tmp_path / "test.db"

    # Initialize with seed data — this creates tables + seeds
    init_db(db_path)

    # Get the connection created by init_db and set it as the global
    conn = engine.get_connection(db_path)
    engine._connection = conn

    # Seed a demo campaign + creative for tests that need them
    conn.execute(
        """INSERT INTO campaigns (id, name, advertiser, objective, audience,
           placements, budget, flight_start, flight_end, brief)
           VALUES (1, 'Test Campaign', 'Test Advertiser', 'awareness',
           'test audience', 'olv,stv', 100000, '2026-03-01', '2026-04-30',
           'Test campaign brief')"""
    )
    conn.execute(
        """INSERT INTO creatives (id, campaign_id, name, prompt, video_url,
           duration_seconds, width, height, placement_type, approval_status,
           vast_url, luma_generation_id)
           VALUES (1, 1, 'Test Creative', 'A test video prompt',
           'https://cdn.luma.example/test.mp4', 30, 1920, 1080, 'olv', 'draft',
           '', 'gen-test-001')"""
    )
    conn.commit()

    yield db_path

    engine._connection = None
    conn.close()
