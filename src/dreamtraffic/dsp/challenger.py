"""Challenger DSP adapters — StackAdapt and Adelphic/Viant.

PRODUCTION NOTE: Thinner placeholder adapters for emerging DSPs.
These platforms offer differentiated targeting (contextual, household-level)
that complements the big-three DSP strategy.
"""

from __future__ import annotations

import uuid

from dreamtraffic.dsp.base import DSPAdapter, UploadResult


class StackAdaptAdapter(DSPAdapter):
    """StackAdapt — contextual targeting, household-level reach."""

    name = "stackadapt"

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
        asset_id = f"sa-asset-{uuid.uuid4().hex[:8]}"
        creative_id = f"sa-cr-{uuid.uuid4().hex[:8]}"

        return UploadResult(
            dsp=self.name,
            asset_id=asset_id,
            creative_id=creative_id,
            audit_status="pending",
            placement_type=placement_type,
            vast_url=vast_url,
            request_payload={
                "campaignName": campaign_name,
                "vastTag": vast_url,
                "contextualTargeting": True,
                "householdTargeting": True,
                "_simulated": True,
            },
            response_payload={
                "creativeId": creative_id,
                "status": "pending_review",
                "_simulated": True,
            },
            _simulated=True,
        )

    def check_audit_status(self, creative_id: str) -> str:
        return "pending"

    def get_supported_placements(self) -> list[str]:
        return ["olv"]


class AdelphicAdapter(DSPAdapter):
    """Adelphic/Viant — household ID graph targeting."""

    name = "adelphic"

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
        asset_id = f"adel-asset-{uuid.uuid4().hex[:8]}"
        creative_id = f"adel-cr-{uuid.uuid4().hex[:8]}"

        return UploadResult(
            dsp=self.name,
            asset_id=asset_id,
            creative_id=creative_id,
            audit_status="pending",
            placement_type=placement_type,
            vast_url=vast_url,
            request_payload={
                "campaignName": campaign_name,
                "vastTag": vast_url,
                "viantHouseholdId": True,
                "_simulated": True,
            },
            response_payload={
                "creativeId": creative_id,
                "status": "pending_review",
                "_simulated": True,
            },
            _simulated=True,
        )

    def check_audit_status(self, creative_id: str) -> str:
        return "pending"

    def get_supported_placements(self) -> list[str]:
        return ["olv"]
