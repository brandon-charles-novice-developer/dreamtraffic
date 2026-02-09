"""Configuration — env vars, model tiers, DSP endpoints."""

from __future__ import annotations

import os
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = Path(os.getenv("DREAMTRAFFIC_DB_PATH", str(DATA_DIR / "dreamtraffic.db")))

# API keys
LUMAAI_API_KEY = os.getenv("LUMAAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Claude model tiers
MODELS = {
    "director": "claude-sonnet-4-5-20250929",
    "compliance": "claude-haiku-4-5-20251001",
    "trafficking": "claude-sonnet-4-5-20250929",
    "analyst": "claude-haiku-4-5-20251001",
}

# DSP endpoint stubs (placeholder URLs — production would use real API endpoints)
DSP_ENDPOINTS = {
    "amazon": {
        "base_url": "https://advertising-api.amazon.com/v3",
        "regions": ["NA", "EU", "FE"],
    },
    "thetradedesk": {
        "base_url": "https://api.thetradedesk.com/v3",
    },
    "dv360": {
        "base_url": "https://displayvideo.googleapis.com/v4",
    },
    "stackadapt": {
        "base_url": "https://api.stackadapt.com/v2",
    },
    "adelphic": {
        "base_url": "https://api.adelphic.com/v1",
    },
}

# Luma generation defaults
LUMA_DEFAULTS = {
    "model": "ray2",
    "resolution": "1080p",
    "aspect_ratio": "16:9",
}

# Measurement vendor pixel base URLs
MEASUREMENT_VENDORS = {
    "ias": {
        "name": "Integral Ad Science",
        "verification_url": "https://pixel.adsafeprotected.com/services/pub",
        "js_url": "https://fw.adsafeprotected.com/rfw/dv/fwjsvid/st/291582/36966574.js",
        "cpm": 0.02,
    },
    "moat": {
        "name": "Moat by Oracle",
        "verification_url": "https://z.moatads.com/dreamtrafficpixel/moatvideo.js",
        "js_url": "https://z.moatads.com/dreamtrafficpixel/moatvideo.js",
        "cpm": 0.03,
    },
    "doubleverify": {
        "name": "DoubleVerify",
        "verification_url": "https://cdn.doubleverify.com/dvbs_src.js",
        "js_url": "https://cdn.doubleverify.com/dvbs_src.js",
        "cpm": 0.025,
    },
}
