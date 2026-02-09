"""@tool definitions for exchange routing, SSP mapping, and fee analysis."""

from __future__ import annotations

import json
from typing import Any

from claude_agent_sdk import tool

from dreamtraffic.exchange.bidswitch import BidswitchRouter
from dreamtraffic.exchange.ssp import SSPRegistry
from dreamtraffic.measurement.fee_stack import FeeStackCalculator


@tool(
    "route_exchange",
    "Route a DSP through Bidswitch to eligible SSPs. Returns scored routes.",
    {"dsp": str, "placement_type": str},
)
async def route_exchange(args: dict[str, Any]) -> dict[str, Any]:
    router = BidswitchRouter()
    routes = router.route(args["dsp"], args.get("placement_type", "olv"))
    route_data = [
        {
            "ssp": r.ssp,
            "t_group": r.t_group,
            "smartswitch_score": r.smartswitch_score,
            "estimated_latency_ms": r.estimated_latency_ms,
            "estimated_win_rate": r.estimated_win_rate,
            "fee_pct": r.fee_pct,
            "_simulated": r._simulated,
        }
        for r in routes
    ]
    return {"content": [{"type": "text", "text": json.dumps(route_data, indent=2)}]}


@tool(
    "get_supply_map",
    "Get the full DSP to SSP routing map via Bidswitch.",
    {},
)
async def get_supply_map(args: dict[str, Any]) -> dict[str, Any]:
    router = BidswitchRouter()
    supply_map = router.get_supply_map()
    return {"content": [{"type": "text", "text": json.dumps(supply_map, indent=2)}]}


@tool(
    "list_ssps",
    "List all SSP configurations with capabilities.",
    {},
)
async def list_ssps(args: dict[str, Any]) -> dict[str, Any]:
    ssps = SSPRegistry.list_all()
    data = [
        {
            "key": s.key,
            "name": s.name,
            "take_rate_pct": s.take_rate_pct,
            "formats": s.supported_formats,
            "specialization": s.specialization,
            "streaming_pods": s.streaming_pod_support,
            "header_bidding": s.header_bidding,
        }
        for s in ssps
    ]
    return {"content": [{"type": "text", "text": json.dumps(data, indent=2)}]}


@tool(
    "analyze_fee_stack",
    "Calculate and compare fee stacks across all supply paths.",
    {"base_cpm": float},
)
async def analyze_fee_stack(args: dict[str, Any]) -> dict[str, Any]:
    calc = FeeStackCalculator()
    comparison = calc.compare_dsps()
    return {"content": [{"type": "text", "text": json.dumps(comparison, indent=2)}]}


@tool(
    "simulate_bid",
    "Simulate an OpenRTB 2.6 bid request/response for a specific SSP.",
    {"ssp": str, "creative_id": str},
)
async def simulate_bid(args: dict[str, Any]) -> dict[str, Any]:
    bid_request = SSPRegistry.simulate_bid_request(args["ssp"], args["creative_id"])
    bid_response = SSPRegistry.simulate_bid_response(
        args["ssp"], args["creative_id"], f"https://vast.dreamtraffic.demo/{args['creative_id']}"
    )
    return {"content": [{"type": "text", "text": json.dumps({
        "bid_request": bid_request,
        "bid_response": bid_response,
    }, indent=2)}]}
