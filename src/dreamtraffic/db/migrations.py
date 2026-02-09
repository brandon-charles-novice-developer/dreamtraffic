"""DDL + seed data — DSP specs, SSP configs, fee schedules, supply paths."""

from __future__ import annotations

from pathlib import Path

from dreamtraffic.db.engine import get_connection

DDL = """
CREATE TABLE IF NOT EXISTS campaigns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    advertiser TEXT NOT NULL DEFAULT '',
    objective TEXT NOT NULL DEFAULT '',
    audience TEXT NOT NULL DEFAULT '',
    placements TEXT NOT NULL DEFAULT '',
    budget REAL NOT NULL DEFAULT 0.0,
    flight_start TEXT NOT NULL DEFAULT '',
    flight_end TEXT NOT NULL DEFAULT '',
    brief TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS creatives (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id INTEGER NOT NULL REFERENCES campaigns(id),
    name TEXT NOT NULL DEFAULT '',
    luma_generation_id TEXT NOT NULL DEFAULT '',
    prompt TEXT NOT NULL DEFAULT '',
    video_url TEXT NOT NULL DEFAULT '',
    duration_seconds INTEGER NOT NULL DEFAULT 0,
    width INTEGER NOT NULL DEFAULT 1920,
    height INTEGER NOT NULL DEFAULT 1080,
    aspect_ratio TEXT NOT NULL DEFAULT '16:9',
    format TEXT NOT NULL DEFAULT 'mp4',
    placement_type TEXT NOT NULL DEFAULT 'olv',
    approval_status TEXT NOT NULL DEFAULT 'draft',
    measurement_config TEXT NOT NULL DEFAULT '',
    vast_url TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS approval_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    creative_id INTEGER NOT NULL REFERENCES creatives(id),
    from_status TEXT NOT NULL,
    to_status TEXT NOT NULL,
    reviewer TEXT NOT NULL DEFAULT '',
    notes TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS trafficking_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    creative_id INTEGER NOT NULL REFERENCES creatives(id),
    dsp TEXT NOT NULL,
    dsp_creative_id TEXT NOT NULL DEFAULT '',
    dsp_asset_id TEXT NOT NULL DEFAULT '',
    vast_url TEXT NOT NULL DEFAULT '',
    audit_status TEXT NOT NULL DEFAULT 'pending',
    placement_type TEXT NOT NULL DEFAULT 'olv',
    request_payload TEXT NOT NULL DEFAULT '',
    response_payload TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS supply_paths (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dsp TEXT NOT NULL,
    exchange TEXT NOT NULL DEFAULT '',
    ssp TEXT NOT NULL,
    dsp_fee_pct REAL NOT NULL DEFAULT 0.0,
    exchange_fee_pct REAL NOT NULL DEFAULT 0.0,
    ssp_fee_pct REAL NOT NULL DEFAULT 0.0,
    measurement_cpm REAL NOT NULL DEFAULT 0.0,
    estimated_win_rate REAL NOT NULL DEFAULT 0.0,
    avg_latency_ms INTEGER NOT NULL DEFAULT 0,
    notes TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS dsp_specs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dsp TEXT NOT NULL,
    placement_type TEXT NOT NULL,
    max_duration_seconds INTEGER NOT NULL DEFAULT 0,
    min_width INTEGER NOT NULL DEFAULT 0,
    min_height INTEGER NOT NULL DEFAULT 0,
    supported_formats TEXT NOT NULL DEFAULT '',
    requires_vast INTEGER NOT NULL DEFAULT 1,
    requires_mraid INTEGER NOT NULL DEFAULT 0,
    max_file_size_mb REAL NOT NULL DEFAULT 0.0,
    notes TEXT NOT NULL DEFAULT ''
);
"""

SEED_DSP_SPECS = [
    # Amazon DSP — OLV
    ("amazon", "olv", 30, 640, 360, "mp4,webm", 1, 0, 500.0,
     "Amazon OLV: 15s/30s, H.264, AAC audio, <=500MB"),
    ("amazon", "stv", 30, 1920, 1080, "mp4", 1, 0, 500.0,
     "Amazon STV: 15s/30s, 1080p min, H.264 High Profile"),
    # The Trade Desk
    ("thetradedesk", "olv", 60, 640, 360, "mp4,webm,mov", 1, 0, 400.0,
     "TTD: up to 60s, VAST 2.0-4.2, UID 2.0 targeting"),
    ("thetradedesk", "stv", 60, 1280, 720, "mp4", 1, 0, 400.0,
     "TTD STV: 720p min, VAST 4.x preferred"),
    # DV360
    ("dv360", "olv", 60, 640, 360, "mp4,webm", 1, 0, 1024.0,
     "DV360: two-step upload (asset → creative), VAST 4.1+"),
    ("dv360", "stv", 30, 1920, 1080, "mp4", 1, 0, 1024.0,
     "DV360 STV: 1080p, VAST 4.1+, Google verification"),
    # Challenger DSPs
    ("stackadapt", "olv", 30, 640, 360, "mp4", 1, 0, 200.0,
     "StackAdapt: contextual + household targeting, VAST 3.0+"),
    ("adelphic", "olv", 30, 640, 360, "mp4", 1, 0, 300.0,
     "Adelphic/Viant: household ID targeting, VAST 2.0+"),
]

SEED_SUPPLY_PATHS = [
    # Amazon DSP paths (post-June 2025 reduced fees)
    ("amazon", "bidswitch", "magnite", 12.0, 2.0, 15.0, 0.02, 0.18, 85,
     "ADSP primary: Certified Supply Exchange partner"),
    ("amazon", "bidswitch", "pubmatic", 12.0, 2.0, 14.0, 0.02, 0.15, 90,
     "ADSP + PubMatic cloud infra, OpenWrap"),
    ("amazon", "bidswitch", "index_exchange", 12.0, 2.0, 12.0, 0.02, 0.20, 75,
     "ADSP + Index: header bidding transparency"),
    ("amazon", "direct", "freewheel", 12.0, 0.0, 18.0, 0.02, 0.12, 95,
     "ADSP direct → FreeWheel for premium streaming pods"),
    # TTD paths
    ("thetradedesk", "bidswitch", "magnite", 15.0, 2.0, 15.0, 0.03, 0.16, 88,
     "TTD via Bidswitch to Magnite premium video"),
    ("thetradedesk", "bidswitch", "pubmatic", 15.0, 2.0, 14.0, 0.03, 0.14, 92,
     "TTD standard path"),
    ("thetradedesk", "bidswitch", "index_exchange", 15.0, 2.0, 12.0, 0.03, 0.19, 78,
     "TTD + Index header bidding"),
    # DV360 paths
    ("dv360", "bidswitch", "magnite", 14.0, 2.0, 15.0, 0.025, 0.15, 90,
     "DV360 to Magnite via Bidswitch"),
    ("dv360", "direct", "freewheel", 14.0, 0.0, 18.0, 0.025, 0.10, 98,
     "DV360 direct to FreeWheel, Google-preferred path"),
    # Challenger DSP paths
    ("stackadapt", "bidswitch", "pubmatic", 16.0, 2.5, 14.0, 0.02, 0.10, 100,
     "StackAdapt contextual path"),
    ("adelphic", "bidswitch", "magnite", 16.0, 2.5, 15.0, 0.02, 0.08, 105,
     "Adelphic/Viant household targeting path"),
]


def init_db(db_path: Path | None = None) -> None:
    """Create tables and insert seed data."""
    conn = get_connection(db_path)
    conn.executescript(DDL)

    # Seed DSP specs if empty
    count = conn.execute("SELECT COUNT(*) FROM dsp_specs").fetchone()[0]
    if count == 0:
        conn.executemany(
            """INSERT INTO dsp_specs
               (dsp, placement_type, max_duration_seconds, min_width, min_height,
                supported_formats, requires_vast, requires_mraid, max_file_size_mb, notes)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            SEED_DSP_SPECS,
        )

    # Seed supply paths if empty
    count = conn.execute("SELECT COUNT(*) FROM supply_paths").fetchone()[0]
    if count == 0:
        conn.executemany(
            """INSERT INTO supply_paths
               (dsp, exchange, ssp, dsp_fee_pct, exchange_fee_pct, ssp_fee_pct,
                measurement_cpm, estimated_win_rate, avg_latency_ms, notes)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            SEED_SUPPLY_PATHS,
        )

    conn.commit()
