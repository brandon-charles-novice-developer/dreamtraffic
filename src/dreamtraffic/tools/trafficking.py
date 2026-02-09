"""@tool definitions for DSP trafficking operations."""

from __future__ import annotations

import json
from typing import Any

from claude_agent_sdk import tool

from dreamtraffic.dsp import get_adapter
from dreamtraffic.db.engine import execute, fetch_one, fetch_all


@tool(
    "traffic_creative",
    "Upload a creative to a specific DSP. Requires the creative to be approved.",
    {"creative_id": int, "dsp": str},
)
async def traffic_creative(args: dict[str, Any]) -> dict[str, Any]:
    creative = fetch_one("SELECT * FROM creatives WHERE id = ?", (args["creative_id"],))
    if creative is None:
        return {"content": [{"type": "text", "text": f"Creative {args['creative_id']} not found"}]}

    if creative["approval_status"] != "approved":
        return {"content": [{"type": "text", "text": (
            f"Creative must be approved before trafficking. "
            f"Current status: {creative['approval_status']}"
        )}]}

    campaign = fetch_one("SELECT * FROM campaigns WHERE id = ?", (creative["campaign_id"],))
    campaign_name = campaign["name"] if campaign else "Unknown Campaign"

    adapter = get_adapter(args["dsp"])
    result = adapter.upload_creative(
        video_url=creative["video_url"],
        vast_url=creative["vast_url"],
        duration_seconds=creative["duration_seconds"],
        width=creative["width"],
        height=creative["height"],
        placement_type=creative["placement_type"],
        campaign_name=campaign_name,
    )

    # Record trafficking
    execute(
        """INSERT INTO trafficking_records
           (creative_id, dsp, dsp_creative_id, dsp_asset_id, vast_url,
            audit_status, placement_type, request_payload, response_payload)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            args["creative_id"], result.dsp, result.creative_id,
            result.asset_id, result.vast_url, result.audit_status,
            result.placement_type,
            json.dumps(result.request_payload),
            json.dumps(result.response_payload),
        ),
    )

    return {"content": [{"type": "text", "text": json.dumps({
        "dsp": result.dsp,
        "creative_id": result.creative_id,
        "asset_id": result.asset_id,
        "audit_status": result.audit_status,
        "_simulated": result._simulated,
    }, indent=2)}]}


@tool(
    "traffic_all_dsps",
    "Upload a creative to all specified DSPs at once.",
    {"creative_id": int, "dsps": str},
)
async def traffic_all_dsps(args: dict[str, Any]) -> dict[str, Any]:
    dsp_list = [d.strip() for d in args["dsps"].split(",")]
    results = []
    for dsp in dsp_list:
        # Re-use the single trafficking logic
        r = await traffic_creative({"creative_id": args["creative_id"], "dsp": dsp})
        results.append({"dsp": dsp, "result": r["content"][0]["text"]})
    return {"content": [{"type": "text", "text": json.dumps(results, indent=2)}]}


@tool(
    "check_dsp_audit",
    "Check the audit status of a creative on a specific DSP.",
    {"creative_id": int, "dsp": str},
)
async def check_dsp_audit(args: dict[str, Any]) -> dict[str, Any]:
    record = fetch_one(
        "SELECT * FROM trafficking_records WHERE creative_id = ? AND dsp = ?",
        (args["creative_id"], args["dsp"]),
    )
    if record is None:
        return {"content": [{"type": "text", "text": f"No trafficking record for creative {args['creative_id']} on {args['dsp']}"}]}

    adapter = get_adapter(args["dsp"])
    status = adapter.check_audit_status(record["dsp_creative_id"])

    return {"content": [{"type": "text", "text": json.dumps({
        "dsp": args["dsp"],
        "dsp_creative_id": record["dsp_creative_id"],
        "audit_status": status,
        "_simulated": True,
    }, indent=2)}]}


@tool(
    "get_trafficking_summary",
    "Get trafficking status across all DSPs for a creative.",
    {"creative_id": int},
)
async def get_trafficking_summary(args: dict[str, Any]) -> dict[str, Any]:
    records = fetch_all(
        "SELECT dsp, dsp_creative_id, audit_status, placement_type, created_at FROM trafficking_records WHERE creative_id = ?",
        (args["creative_id"],),
    )
    return {"content": [{"type": "text", "text": json.dumps(records, indent=2)}]}
