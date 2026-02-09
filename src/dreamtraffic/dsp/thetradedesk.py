"""The Trade Desk v3 adapter.

PRODUCTION NOTE: Placeholder adapter simulating TTD v3 API responses.
Real implementation would use TTD's REST API with partner credentials,
support UID 2.0 targeting, and integrate with Kokai AI optimization.
"""

from __future__ import annotations

import uuid

from dreamtraffic.dsp.base import DSPAdapter, UploadResult


class TTDAdapter(DSPAdapter):
    """The Trade Desk — UID 2.0, Kokai AI, open internet focus."""

    name = "thetradedesk"

    FEE_PCT = 0.15  # ~15% platform fee

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
        """Simulate TTD creative upload.

        PRODUCTION NOTE: Real implementation would:
        1. POST to /v3/creative with VAST tag
        2. Associate with ad group via /v3/adgroup
        3. TTD performs internal creative audit
        4. Support UID 2.0 audience targeting
        """
        asset_id = f"ttd-asset-{uuid.uuid4().hex[:10]}"
        creative_id = f"ttd-cr-{uuid.uuid4().hex[:10]}"

        request_payload = {
            "AdvertiserId": "TTD_ADV_DEMO",
            "CreativeName": f"{campaign_name} - {placement_type.upper()}",
            "VastTagUrl": vast_url,
            "VideoAttributes": {
                "Duration": duration_seconds,
                "Width": width,
                "Height": height,
            },
            "Uid2Enabled": True,
            "KokaiOptimization": True,
        }

        response_payload = {
            "CreativeId": creative_id,
            "AssetId": asset_id,
            "AuditStatus": "pending",
            "Uid2Ready": True,
            "_simulated": True,
        }

        return UploadResult(
            dsp=self.name,
            asset_id=asset_id,
            creative_id=creative_id,
            audit_status="pending",
            placement_type=placement_type,
            vast_url=vast_url,
            request_payload=request_payload,
            response_payload=response_payload,
            _simulated=True,
        )

    def check_audit_status(self, creative_id: str) -> str:
        return "under_review"

    def get_supported_placements(self) -> list[str]:
        return ["olv", "stv"]
