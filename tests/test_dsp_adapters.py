"""Tests for DSP adapters — Amazon, TTD, DV360, challengers."""

import pytest

from dreamtraffic.dsp import get_adapter
from dreamtraffic.dsp.amazon import AmazonDSPAdapter
from dreamtraffic.dsp.thetradedesk import TTDAdapter
from dreamtraffic.dsp.dv360 import DV360Adapter
from dreamtraffic.dsp.challenger import StackAdaptAdapter, AdelphicAdapter


UPLOAD_KWARGS = {
    "video_url": "https://cdn.luma.example/test.mp4",
    "vast_url": "https://vast.dreamtraffic.demo/inline/1",
    "duration_seconds": 30,
    "width": 1920,
    "height": 1080,
    "placement_type": "olv",
    "campaign_name": "Test Campaign",
}


class TestAdapterFactory:
    def test_get_amazon(self):
        adapter = get_adapter("amazon")
        assert isinstance(adapter, AmazonDSPAdapter)

    def test_get_ttd(self):
        adapter = get_adapter("thetradedesk")
        assert isinstance(adapter, TTDAdapter)

    def test_get_dv360(self):
        adapter = get_adapter("dv360")
        assert isinstance(adapter, DV360Adapter)

    def test_get_stackadapt(self):
        adapter = get_adapter("stackadapt")
        assert isinstance(adapter, StackAdaptAdapter)

    def test_get_adelphic(self):
        adapter = get_adapter("adelphic")
        assert isinstance(adapter, AdelphicAdapter)

    def test_unknown_raises(self):
        with pytest.raises(ValueError, match="Unknown DSP"):
            get_adapter("nonexistent")


class TestAmazonDSP:
    def test_upload_creative(self):
        adapter = AmazonDSPAdapter()
        result = adapter.upload_creative(**UPLOAD_KWARGS)
        assert result.dsp == "amazon"
        assert result.asset_id.startswith("amzn-asset-")
        assert result.creative_id.startswith("amzn-cr-")
        assert result.audit_status == "pending"
        assert result._simulated is True

    def test_upload_stv(self):
        kwargs = {**UPLOAD_KWARGS, "placement_type": "stv"}
        result = AmazonDSPAdapter().upload_creative(**kwargs)
        assert result.placement_type == "stv"

    def test_request_payload_structure(self):
        result = AmazonDSPAdapter().upload_creative(**UPLOAD_KWARGS)
        payload = result.request_payload
        assert "certifiedSupplyExchange" in payload
        assert "feeSchedule" in payload
        assert payload["feeSchedule"]["rate"] == 0.12

    def test_check_audit(self):
        assert AmazonDSPAdapter().check_audit_status("any-id") == "under_review"

    def test_supported_placements(self):
        assert AmazonDSPAdapter().get_supported_placements() == ["olv", "stv"]


class TestTTD:
    def test_upload_creative(self):
        result = TTDAdapter().upload_creative(**UPLOAD_KWARGS)
        assert result.dsp == "thetradedesk"
        assert result.request_payload["Uid2Enabled"] is True

    def test_supported_placements(self):
        assert TTDAdapter().get_supported_placements() == ["olv", "stv"]


class TestDV360:
    def test_upload_creative(self):
        result = DV360Adapter().upload_creative(**UPLOAD_KWARGS)
        assert result.dsp == "dv360"
        assert "creativeType" in result.request_payload

    def test_response_has_google_review(self):
        result = DV360Adapter().upload_creative(**UPLOAD_KWARGS)
        assert result.response_payload["approvalStatus"]["googleReview"] is True


class TestChallengers:
    def test_stackadapt(self):
        result = StackAdaptAdapter().upload_creative(**UPLOAD_KWARGS)
        assert result.dsp == "stackadapt"
        assert result.request_payload["contextualTargeting"] is True

    def test_adelphic(self):
        result = AdelphicAdapter().upload_creative(**UPLOAD_KWARGS)
        assert result.dsp == "adelphic"
        assert result.request_payload["viantHouseholdId"] is True

    def test_challenger_olv_only(self):
        assert StackAdaptAdapter().get_supported_placements() == ["olv"]
        assert AdelphicAdapter().get_supported_placements() == ["olv"]
