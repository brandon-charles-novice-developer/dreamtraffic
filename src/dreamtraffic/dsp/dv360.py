"""DV360 v4 adapter — Google Display & Video 360.

PRODUCTION NOTE: Placeholder adapter simulating DV360 v4 API responses.
Real implementation uses a two-step upload (asset → creative object) via
the Display & Video 360 API v4 with Google OAuth2 credentials.
"""

from __future__ import annotations

import uuid

from dreamtraffic.dsp.base import DSPAdapter, UploadResult


class DV360Adapter(DSPAdapter):
    """Google DV360 — two-step upload, Google-preferred supply paths."""

    name = "dv360"

    FEE_PCT = 0.14  # ~14% platform fee

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
        """Simulate DV360 two-step creative upload.

        PRODUCTION NOTE: Real implementation would:
        1. POST asset to /v4/advertisers/{id}/assets with video file
        2. POST creative to /v4/advertisers/{id}/creatives with VAST tag + asset ref
        3. DV360 runs Google creative review (brand safety + policy)
        4. Associate with line item and insertion order
        """
        asset_id = f"dv360-asset-{uuid.uuid4().hex[:10]}"
        creative_id = f"dv360-cr-{uuid.uuid4().hex[:10]}"

        request_payload = {
            "advertiserId": "DV360_ADV_DEMO",
            "displayName": f"{campaign_name} - {placement_type.upper()}",
            "entityStatus": "ENTITY_STATUS_ACTIVE",
            "creativeType": "CREATIVE_TYPE_VIDEO",
            "assets": [{"asset": {"mediaId": asset_id}, "role": "ASSET_ROLE_MAIN"}],
            "vastTagUrl": vast_url,
            "dimensions": {"widthPixels": width, "heightPixels": height},
        }

        response_payload = {
            "creativeId": creative_id,
            "assetId": asset_id,
            "approvalStatus": {
                "status": "APPROVAL_STATUS_PENDING_REVIEW",
                "googleReview": True,
            },
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
