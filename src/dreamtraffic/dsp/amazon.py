"""Amazon DSP adapter — MCP-inspired, OLV/STV, Certified Supply Exchange.

PRODUCTION NOTE: This is a placeholder adapter that simulates Amazon DSP API
responses. In production, this would integrate with the Amazon Advertising API v3
and leverage the Amazon DSP MCP Server (launched Feb 2, 2026) for programmatic
creative management.

Key Amazon DSP concepts modeled:
- OLV (Online Video) vs. STV (Streaming TV) creative specs
- Certified Supply Exchange partners (Magnite, PubMatic, Index Exchange)
- Post-June 2025 reduced fee schedule (managed-service cut up to 20%)
- Amazon audience segments (in-market, lifestyle, purchase-based)
"""

from __future__ import annotations

import uuid

from dreamtraffic.dsp.base import DSPAdapter, UploadResult


class AmazonDSPAdapter(DSPAdapter):
    """Amazon DSP — most detailed adapter, mirrors MCP Server patterns."""

    name = "amazon"

    # Post-June 2025 fee schedule
    MANAGED_SERVICE_FEE = 0.12  # 12% (reduced from ~15%)
    SELF_SERVICE_FEE = 0.10  # 10%

    # Certified Supply Exchange partners
    CERTIFIED_SUPPLY = ["magnite", "pubmatic", "index_exchange"]

    # Amazon audience segment types
    AUDIENCE_SEGMENTS = {
        "in_market": "Users actively researching/purchasing in category",
        "lifestyle": "Users whose purchase history indicates affinity",
        "purchase_based": "Amazon first-party purchase signals",
        "custom": "Advertiser-provided audience data",
    }

    # Creative spec requirements
    SPECS = {
        "olv": {
            "max_duration": 30,
            "min_resolution": "640x360",
            "max_file_size_mb": 500,
            "formats": ["mp4", "webm"],
            "codec": "H.264",
            "audio": "AAC, 128kbps+",
        },
        "stv": {
            "max_duration": 30,
            "min_resolution": "1920x1080",
            "max_file_size_mb": 500,
            "formats": ["mp4"],
            "codec": "H.264 High Profile",
            "audio": "AAC, 192kbps+",
        },
    }

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
        """Simulate Amazon DSP creative upload.

        PRODUCTION NOTE: Real implementation would:
        1. POST to /v3/creatives/video with asset URL
        2. Receive assetId, submit for creative review
        3. Poll audit status via GET /v3/creatives/{creativeId}
        4. Associate with line items once approved
        """
        asset_id = f"amzn-asset-{uuid.uuid4().hex[:12]}"
        creative_id = f"amzn-cr-{uuid.uuid4().hex[:12]}"

        # Validate placement type
        if placement_type not in self.SPECS:
            placement_type = "olv"

        spec = self.SPECS[placement_type]

        request_payload = {
            "advertiserId": "AMZN_ADV_DEMO",
            "creativeType": "VIDEO",
            "placementType": placement_type.upper(),
            "videoAsset": {
                "url": video_url,
                "vastTagUrl": vast_url,
                "duration": duration_seconds,
                "width": width,
                "height": height,
                "codec": spec["codec"],
            },
            "campaignName": campaign_name,
            "certifiedSupplyExchange": self.CERTIFIED_SUPPLY,
            "feeSchedule": {
                "type": "managed_service",
                "rate": self.MANAGED_SERVICE_FEE,
                "effective_date": "2025-06-01",
                "note": "Post-June 2025 reduced rate",
            },
        }

        response_payload = {
            "assetId": asset_id,
            "creativeId": creative_id,
            "auditStatus": "pending",
            "placementType": placement_type.upper(),
            "estimatedReviewTime": "24-48 hours",
            "certifiedSupplyPartners": self.CERTIFIED_SUPPLY,
            "mcpServerCompatible": True,
            "_simulated": True,
            # PRODUCTION NOTE: Real response includes moderation flags,
            # category classifications, and supply eligibility details
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
        """Simulate audit status check.

        PRODUCTION NOTE: Real implementation polls GET /v3/creatives/{creativeId}
        and returns one of: pending, under_review, approved, rejected.
        """
        # Simulation: always return under_review for demo
        return "under_review"

    def get_supported_placements(self) -> list[str]:
        return ["olv", "stv"]
