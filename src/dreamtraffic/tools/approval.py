"""@tool definitions for approval workflow operations."""

from __future__ import annotations

import json
from typing import Any

from claude_agent_sdk import tool

from dreamtraffic.approval.workflow import ApprovalWorkflow


_workflow = ApprovalWorkflow()


@tool(
    "submit_for_review",
    "Submit a creative for compliance review. Transitions from draft to pending_review.",
    {"creative_id": int},
)
async def submit_for_review(args: dict[str, Any]) -> dict[str, Any]:
    result = _workflow.submit_for_review(args["creative_id"])
    return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}


@tool(
    "approve_creative",
    "Approve a creative after compliance review.",
    {"creative_id": int, "notes": str},
)
async def approve_creative(args: dict[str, Any]) -> dict[str, Any]:
    result = _workflow.approve(args["creative_id"], notes=args.get("notes", ""))
    return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}


@tool(
    "request_revision",
    "Request revision on a creative with specific feedback.",
    {"creative_id": int, "notes": str},
)
async def request_revision(args: dict[str, Any]) -> dict[str, Any]:
    result = _workflow.request_revision(args["creative_id"], notes=args["notes"])
    return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}


@tool(
    "get_approval_status",
    "Get current approval status and valid next transitions for a creative.",
    {"creative_id": int},
)
async def get_approval_status(args: dict[str, Any]) -> dict[str, Any]:
    status = _workflow.get_status(args["creative_id"])
    valid = _workflow.get_valid_transitions(args["creative_id"])
    trail = _workflow.get_audit_trail(args["creative_id"])
    return {"content": [{"type": "text", "text": json.dumps({
        "creative_id": args["creative_id"],
        "current_status": status,
        "valid_transitions": valid,
        "audit_trail_count": len(trail),
    }, indent=2)}]}


@tool(
    "get_audit_trail",
    "Get the full approval audit trail for a creative.",
    {"creative_id": int},
)
async def get_audit_trail(args: dict[str, Any]) -> dict[str, Any]:
    trail = _workflow.get_audit_trail(args["creative_id"])
    return {"content": [{"type": "text", "text": json.dumps(trail, indent=2)}]}
