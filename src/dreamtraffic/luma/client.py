"""LumaClient — generate, poll, and download Dream Machine videos."""

from __future__ import annotations

import time
from pathlib import Path

import httpx
from lumaai import LumaAI

from dreamtraffic.config import LUMAAI_API_KEY, DATA_DIR


class LumaClient:
    """Wrapper around the Luma AI SDK for video generation."""

    def __init__(self, api_key: str | None = None) -> None:
        self._client = LumaAI(auth_token=api_key or LUMAAI_API_KEY)

    def generate(
        self,
        prompt: str,
        *,
        duration: str = "5s",
        resolution: str = "1080p",
        aspect_ratio: str = "16:9",
        model: str = "ray2",
        loop: bool = False,
    ) -> str:
        """Start a video generation and return the generation ID."""
        generation = self._client.generations.create(
            prompt=prompt,
            model=model,
            resolution=resolution,
            duration=duration,
            aspect_ratio=aspect_ratio,
            loop=loop,
        )
        return generation.id

    def poll(self, generation_id: str, *, timeout: int = 300, interval: int = 5) -> dict:
        """Poll until generation completes. Returns generation data."""
        deadline = time.time() + timeout
        while time.time() < deadline:
            gen = self._client.generations.get(id=generation_id)
            if gen.state == "completed":
                return {
                    "id": gen.id,
                    "state": gen.state,
                    "video_url": gen.assets.video if gen.assets else "",
                    "thumbnail_url": getattr(gen.assets, "thumbnail", "") if gen.assets else "",
                }
            if gen.state == "failed":
                reason = getattr(gen, "failure_reason", "unknown")
                raise RuntimeError(f"Luma generation {generation_id} failed: {reason}")
            time.sleep(interval)
        raise TimeoutError(f"Luma generation {generation_id} timed out after {timeout}s")

    def download(self, video_url: str, filename: str | None = None) -> Path:
        """Download a completed video to the data directory."""
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        fname = filename or video_url.split("/")[-1].split("?")[0]
        if not fname.endswith(".mp4"):
            fname += ".mp4"
        dest = DATA_DIR / fname
        with httpx.stream("GET", video_url) as resp:
            resp.raise_for_status()
            with open(dest, "wb") as f:
                for chunk in resp.iter_bytes(chunk_size=8192):
                    f.write(chunk)
        return dest

    def generate_and_wait(
        self,
        prompt: str,
        *,
        duration: str = "5s",
        resolution: str = "1080p",
        aspect_ratio: str = "16:9",
        model: str = "ray2",
        loop: bool = False,
        timeout: int = 300,
    ) -> dict:
        """Generate a video and wait for completion. Returns generation data with video_url."""
        gen_id = self.generate(
            prompt,
            duration=duration,
            resolution=resolution,
            aspect_ratio=aspect_ratio,
            model=model,
            loop=loop,
        )
        return self.poll(gen_id, timeout=timeout)
