"""@tool definitions for measurement vendor config and VAST wrapping."""

from __future__ import annotations

import json
from typing import Any

from claude_agent_sdk import tool

from dreamtraffic.measurement.vendors import get_vendor_config, VENDORS
from dreamtraffic.measurement.vast import VastGenerator
from dreamtraffic.measurement.fee_stack import FeeStackCalculator
from dreamtraffic.db.engine import execute, fetch_one


@tool(
    "generate_vast_tag",
    "Generate a VAST 4.2 InLine tag with measurement vendor AdVerification elements.",
    {"creative_id": int, "vendors": str},
)
async def generate_vast_tag(args: dict[str, Any]) -> dict[str, Any]:
    creative = fetch_one("SELECT * FROM creatives WHERE id = ?", (args["creative_id"],))
    if creative is None:
        return {"content": [{"type": "text", "text": f"Creative {args['creative_id']} not found"}]}

    vendor_keys = [v.strip() for v in args.get("vendors", "ias,moat,doubleverify").split(",")]

    # Calculate duration string
    secs = creative["duration_seconds"]
    duration_str = f"00:00:{secs:02d}"

    generator = VastGenerator()
    vast_xml = generator.generate_inline(
        video_url=creative["video_url"],
        duration=duration_str,
        title=creative["name"] or "DreamTraffic Creative",
        vendors=vendor_keys,
    )

    # Store VAST URL reference and measurement config
    vast_url = f"https://vast.dreamtraffic.demo/inline/{args['creative_id']}"
    execute(
        "UPDATE creatives SET vast_url = ?, measurement_config = ? WHERE id = ?",
        (vast_url, json.dumps(vendor_keys), args["creative_id"]),
    )

    return {"content": [{"type": "text", "text": vast_xml}]}


@tool(
    "generate_vast_wrapper",
    "Generate a VAST 4.2 Wrapper tag that wraps an existing VAST tag with additional measurement.",
    {"vast_ad_tag_uri": str, "vendors": str},
)
async def generate_vast_wrapper(args: dict[str, Any]) -> dict[str, Any]:
    vendor_keys = [v.strip() for v in args.get("vendors", "ias,moat,doubleverify").split(",")]
    generator = VastGenerator()
    wrapper_xml = generator.generate_wrapper(
        vast_ad_tag_uri=args["vast_ad_tag_uri"],
        vendors=vendor_keys,
    )
    return {"content": [{"type": "text", "text": wrapper_xml}]}


@tool(
    "list_measurement_vendors",
    "List available measurement vendors and their CPMs.",
    {},
)
async def list_measurement_vendors(args: dict[str, Any]) -> dict[str, Any]:
    data = [
        {
            "key": v.key,
            "name": v.name,
            "cpm": v.cpm,
            "omid_partner": v.omid_partner,
        }
        for v in VENDORS.values()
    ]
    return {"content": [{"type": "text", "text": json.dumps(data, indent=2)}]}


@tool(
    "calculate_measurement_cost",
    "Calculate total measurement vendor cost for given impression volume.",
    {"vendors": str, "impressions": int},
)
async def calculate_measurement_cost(args: dict[str, Any]) -> dict[str, Any]:
    vendor_keys = [v.strip() for v in args["vendors"].split(",")]
    total_cpm = sum(VENDORS[k].cpm for k in vendor_keys if k in VENDORS)
    total_cost = (total_cpm / 1000) * args["impressions"]
    return {"content": [{"type": "text", "text": json.dumps({
        "vendors": vendor_keys,
        "total_cpm": total_cpm,
        "impressions": args["impressions"],
        "total_cost": round(total_cost, 2),
    }, indent=2)}]}
