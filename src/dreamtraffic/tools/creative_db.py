"""@tool definitions for campaign and creative CRUD operations."""

from __future__ import annotations

import json
from typing import Any

from claude_agent_sdk import tool

from dreamtraffic.db import supabase_client


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
    result = supabase_client.insert_campaign(
        args["name"], args["advertiser"], args["objective"],
        args["audience"], args["placements"], args["budget"],
        args["flight_start"], args["flight_end"], args["brief"],
    )
    return {"content": [{"type": "text", "text": f"Campaign created with ID: {result['id']}"}]}


@tool(
    "get_campaign",
    "Get campaign details by ID.",
    {"campaign_id": int},
)
async def get_campaign(args: dict[str, Any]) -> dict[str, Any]:
    row = supabase_client.get_campaign(args["campaign_id"])
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
    result = supabase_client.insert_creative(
        campaign_id=args["campaign_id"],
        name=args["name"],
        luma_generation_id="",
        prompt=args["prompt"],
        video_url="",
        duration_seconds=args["duration_seconds"],
        width=1920,
        height=1080,
        aspect_ratio="16:9",
        format="mp4",
        placement_type=args["placement_type"],
        approval_status="draft",
        measurement_config="",
        vast_url="",
    )
    return {"content": [{"type": "text", "text": f"Creative created with ID: {result['id']}"}]}


@tool(
    "get_creative",
    "Get creative details by ID.",
    {"creative_id": int},
)
async def get_creative(args: dict[str, Any]) -> dict[str, Any]:
    row = supabase_client.get_creative(args["creative_id"])
    if row is None:
        return {"content": [{"type": "text", "text": f"Creative {args['creative_id']} not found"}]}
    return {"content": [{"type": "text", "text": json.dumps(row, indent=2)}]}


@tool(
    "list_creatives",
    "List all creatives for a campaign.",
    {"campaign_id": int},
)
async def list_creatives(args: dict[str, Any]) -> dict[str, Any]:
    rows = supabase_client.get_creatives(campaign_id=args["campaign_id"])
    filtered = [
        {
            "id": r.get("id"),
            "name": r.get("name"),
            "approval_status": r.get("approval_status"),
            "placement_type": r.get("placement_type"),
            "duration_seconds": r.get("duration_seconds"),
        }
        for r in rows
    ]
    return {"content": [{"type": "text", "text": json.dumps(filtered, indent=2)}]}
