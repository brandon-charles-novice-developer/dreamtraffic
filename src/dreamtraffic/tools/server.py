"""Assemble all tools into an MCP server for the Agent SDK."""

from __future__ import annotations

from claude_agent_sdk import create_sdk_mcp_server

from dreamtraffic.tools.luma import generate_video, poll_generation, download_video
from dreamtraffic.tools.creative_db import (
    create_campaign, get_campaign, create_creative, get_creative, list_creatives,
)
from dreamtraffic.tools.approval import (
    submit_for_review, approve_creative, request_revision,
    get_approval_status, get_audit_trail,
)
from dreamtraffic.tools.trafficking import (
    traffic_creative, traffic_all_dsps, check_dsp_audit, get_trafficking_summary,
)
from dreamtraffic.tools.supply_chain import (
    route_exchange, get_supply_map, list_ssps, analyze_fee_stack, simulate_bid,
)
from dreamtraffic.tools.measurement import (
    generate_vast_tag, generate_vast_wrapper,
    list_measurement_vendors, calculate_measurement_cost,
)

ALL_TOOLS = [
    # Luma
    generate_video,
    poll_generation,
    download_video,
    # Creative DB
    create_campaign,
    get_campaign,
    create_creative,
    get_creative,
    list_creatives,
    # Approval
    submit_for_review,
    approve_creative,
    request_revision,
    get_approval_status,
    get_audit_trail,
    # Trafficking
    traffic_creative,
    traffic_all_dsps,
    check_dsp_audit,
    get_trafficking_summary,
    # Supply Chain
    route_exchange,
    get_supply_map,
    list_ssps,
    analyze_fee_stack,
    simulate_bid,
    # Measurement
    generate_vast_tag,
    generate_vast_wrapper,
    list_measurement_vendors,
    calculate_measurement_cost,
]

TOOL_NAMES = [f"mcp__dreamtraffic__{t.__name__}" for t in ALL_TOOLS]


def create_dreamtraffic_server():
    """Create the DreamTraffic MCP server with all tools registered."""
    return create_sdk_mcp_server(
        name="dreamtraffic",
        version="0.1.0",
        tools=ALL_TOOLS,
    )
