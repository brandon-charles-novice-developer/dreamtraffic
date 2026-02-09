"""Abstract DSP adapter interface."""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass
class UploadResult:
    """Result of uploading a creative to a DSP."""
    dsp: str
    asset_id: str
    creative_id: str
    audit_status: str
    placement_type: str
    vast_url: str
    request_payload: dict
    response_payload: dict
    _simulated: bool = True

    def to_json(self) -> str:
        return json.dumps({
            "dsp": self.dsp,
            "asset_id": self.asset_id,
            "creative_id": self.creative_id,
            "audit_status": self.audit_status,
            "placement_type": self.placement_type,
            "vast_url": self.vast_url,
            "_simulated": self._simulated,
            "timestamp": datetime.utcnow().isoformat(),
        }, indent=2)


class DSPAdapter(ABC):
    """Base interface for all DSP integrations."""

    name: str = ""

    @abstractmethod
    def upload_creative(
        self,
        *,
        video_url: str,
        vast_url: str,
        duration_seconds: int,
        width: int,
        height: int,
        placement_type: str,
        campaign_name: str,
    ) -> UploadResult:
        """Upload a creative asset and create a creative object in the DSP."""
        ...

    @abstractmethod
    def check_audit_status(self, creative_id: str) -> str:
        """Check the audit/review status of a creative."""
        ...

    @abstractmethod
    def get_supported_placements(self) -> list[str]:
        """Return list of supported placement types."""
        ...
