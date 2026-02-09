"""Dataclass models for all database entities."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ApprovalStatus(str, Enum):
    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    REVISION_REQUESTED = "revision_requested"
    APPROVED = "approved"
    TRAFFICKED = "trafficked"
    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"


class AuditStatus(str, Enum):
    PENDING = "pending"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    ACTIVE = "active"


class PlacementType(str, Enum):
    OLV = "olv"  # Online video (display)
    STV = "stv"  # Streaming TV (CTV)
    PREROLL = "preroll"


@dataclass
class Campaign:
    id: int | None = None
    name: str = ""
    advertiser: str = ""
    objective: str = ""
    audience: str = ""
    placements: str = ""  # comma-separated PlacementType values
    budget: float = 0.0
    flight_start: str = ""
    flight_end: str = ""
    brief: str = ""
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class Creative:
    id: int | None = None
    campaign_id: int = 0
    name: str = ""
    luma_generation_id: str = ""
    prompt: str = ""
    video_url: str = ""
    duration_seconds: int = 0
    width: int = 1920
    height: int = 1080
    aspect_ratio: str = "16:9"
    format: str = "mp4"
    placement_type: str = "olv"
    approval_status: str = ApprovalStatus.DRAFT.value
    measurement_config: str = ""  # JSON string of vendor configs
    vast_url: str = ""
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class ApprovalEvent:
    id: int | None = None
    creative_id: int = 0
    from_status: str = ""
    to_status: str = ""
    reviewer: str = ""
    notes: str = ""
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class TraffickingRecord:
    id: int | None = None
    creative_id: int = 0
    dsp: str = ""
    dsp_creative_id: str = ""
    dsp_asset_id: str = ""
    vast_url: str = ""
    audit_status: str = AuditStatus.PENDING.value
    placement_type: str = "olv"
    request_payload: str = ""  # JSON
    response_payload: str = ""  # JSON
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class SupplyPath:
    id: int | None = None
    dsp: str = ""
    exchange: str = ""
    ssp: str = ""
    dsp_fee_pct: float = 0.0
    exchange_fee_pct: float = 0.0
    ssp_fee_pct: float = 0.0
    measurement_cpm: float = 0.0
    estimated_win_rate: float = 0.0
    avg_latency_ms: int = 0
    notes: str = ""


@dataclass
class DSPSpec:
    id: int | None = None
    dsp: str = ""
    placement_type: str = ""
    max_duration_seconds: int = 0
    min_width: int = 0
    min_height: int = 0
    supported_formats: str = ""  # comma-separated
    requires_vast: bool = True
    requires_mraid: bool = False
    max_file_size_mb: float = 0.0
    notes: str = ""
