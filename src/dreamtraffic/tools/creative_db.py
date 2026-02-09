"""@tool definitions for campaign and creative CRUD operations."""

from __future__ import annotations

import json
from typing import Any

from claude_agent_sdk import tool

from dreamtraffic.db.engine import execute, fetch_one, fetch_all


@tool(
    "create_campaign",
    "Create a new campaign with brief, audience, placements, and flight dates.",
    {
        "name": str,
        "advertiser": str,
        "objective": str,
        "audience": str,
        "placements": str,
        "budget": float,
        "flight_start": str,
        "flight_end": str,
        "brief": str,
    },
)
async def create_campaign(args: dict[str, Any]) -> dict[str, Any]:
    cursor = execute(
        """INSERT INTO campaigns (name, advertiser, objective, audience, placements,
           budget, flight_start, flight_end, brief)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            args["name"], args["advertiser"], args["objective"],
            args["audience"], args["placements"], args["budget"],
            args["flight_start"], args["flight_end"], args["brief"],
        ),
    )
    return {"content": [{"type": "text", "text": f"Campaign created with ID: {cursor.lastrowid}"}]}


@tool(
    "get_campaign",
    "Get campaign details by ID.",
    {"campaign_id": int},
)
async def get_campaign(args: dict[str, Any]) -> dict[str, Any]:
    row = fetch_one("SELECT * FROM campaigns WHERE id = ?", (args["campaign_id"],))
    if row is None:
        return {"content": [{"type": "text", "text": f"Campaign {args['campaign_id']} not found"}]}
    return {"content": [{"type": "text", "text": json.dumps(row, indent=2)}]}


@tool(
    "create_creative",
    "Create a creative record linked to a campaign.",
    {
        "campaign_id": int,
        "name": str,
        "prompt": str,
        "duration_seconds": int,
        "placement_type": str,
    },
)
async def create_creative(args: dict[str, Any]) -> dict[str, Any]:
    cursor = execute(
        """INSERT INTO creatives (campaign_id, name, prompt, duration_seconds, placement_type)
           VALUES (?, ?, ?, ?, ?)""",
        (
            args["campaign_id"], args["name"], args["prompt"],
            args["duration_seconds"], args["placement_type"],
        ),
    )
    return {"content": [{"type": "text", "text": f"Creative created with ID: {cursor.lastrowid}"}]}


@tool(
    "get_creative",
    "Get creative details by ID.",
    {"creative_id": int},
)
async def get_creative(args: dict[str, Any]) -> dict[str, Any]:
    row = fetch_one("SELECT * FROM creatives WHERE id = ?", (args["creative_id"],))
    if row is None:
        return {"content": [{"type": "text", "text": f"Creative {args['creative_id']} not found"}]}
    return {"content": [{"type": "text", "text": json.dumps(row, indent=2)}]}


@tool(
    "list_creatives",
    "List all creatives for a campaign.",
    {"campaign_id": int},
)
async def list_creatives(args: dict[str, Any]) -> dict[str, Any]:
    rows = fetch_all(
        "SELECT id, name, approval_status, placement_type, duration_seconds FROM creatives WHERE campaign_id = ?",
        (args["campaign_id"],),
    )
    return {"content": [{"type": "text", "text": json.dumps(rows, indent=2)}]}
