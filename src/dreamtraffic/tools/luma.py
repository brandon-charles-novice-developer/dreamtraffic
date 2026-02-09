"""@tool definitions for Luma Dream Machine API operations."""

from __future__ import annotations

from typing import Any

from claude_agent_sdk import tool

from dreamtraffic.luma.client import LumaClient
from dreamtraffic.db import supabase_client


@tool(
    "generate_video",
    "Generate a video using Luma Dream Machine. Returns the generation ID for polling.",
    {"prompt": str, "duration": str, "resolution": str, "campaign_id": int},
)
async def generate_video(args: dict[str, Any]) -> dict[str, Any]:
    client = LumaClient()
    gen_id = client.generate(
        prompt=args["prompt"],
        duration=args.get("duration", "5s"),
        resolution=args.get("resolution", "1080p"),
    )
    # Store generation reference
    if args.get("campaign_id"):
        supabase_client.insert_creative(
            campaign_id=args["campaign_id"],
            name="",
            luma_generation_id=gen_id,
            prompt=args["prompt"],
            video_url="",
            duration_seconds=0,
            width=1920,
            height=1080,
            aspect_ratio="16:9",
            format="mp4",
            placement_type="olv",
            approval_status="draft",
            measurement_config="",
            vast_url="",
        )
    return {"content": [{"type": "text", "text": f"Generation started: {gen_id}"}]}


@tool(
    "poll_generation",
    "Poll a Luma generation for completion. Returns video URL when done.",
    {"generation_id": str, "creative_id": int},
)
async def poll_generation(args: dict[str, Any]) -> dict[str, Any]:
    client = LumaClient()
    result = client.poll(args["generation_id"])
    video_url = result.get("video_url", "")

    if args.get("creative_id") and video_url:
        supabase_client.update_creative(args["creative_id"], video_url=video_url)

    return {"content": [{"type": "text", "text": f"Generation complete. Video URL: {video_url}"}]}


@tool(
    "download_video",
    "Download a completed Luma video to local storage.",
    {"video_url": str, "filename": str},
)
async def download_video(args: dict[str, Any]) -> dict[str, Any]:
    client = LumaClient()
    path = client.download(args["video_url"], args.get("filename"))
    return {"content": [{"type": "text", "text": f"Downloaded to: {path}"}]}
