"""Tests for VAST 4.2 generation and measurement vendor wrapping."""

import xml.etree.ElementTree as ET

import pytest

from dreamtraffic.measurement.vast import VastGenerator
from dreamtraffic.measurement.vendors import get_vendor_config, VENDORS

# VAST 4.2 namespace
NS = {"v": "http://www.iab.com/VAST"}


class TestVendors:
    def test_get_ias(self):
        v = get_vendor_config("ias")
        assert v.name == "Integral Ad Science"
        assert v.cpm == 0.02

    def test_get_moat(self):
        v = get_vendor_config("moat")
        assert v.name == "Moat by Oracle"

    def test_get_doubleverify(self):
        v = get_vendor_config("doubleverify")
        assert v.name == "DoubleVerify"

    def test_unknown_vendor_raises(self):
        with pytest.raises(KeyError, match="Unknown measurement vendor"):
            get_vendor_config("nonexistent")

    def test_omid_partner(self):
        v = get_vendor_config("ias")
        assert v.omid_partner == "com.ias"

    def test_all_vendors_present(self):
        assert set(VENDORS.keys()) == {"ias", "moat", "doubleverify"}


class TestVastInline:
    def setup_method(self):
        self.gen = VastGenerator()
        self.xml = self.gen.generate_inline(
            video_url="https://cdn.example.com/video.mp4",
            duration="00:00:30",
            title="Test Ad",
            vendors=["ias", "moat", "doubleverify"],
        )

    def test_valid_xml(self):
        ET.fromstring(self.xml)

    def test_vast_version(self):
        root = ET.fromstring(self.xml)
        assert root.attrib["version"] == "4.2"

    def test_has_inline(self):
        root = ET.fromstring(self.xml)
        ad = root.find("v:Ad", NS)
        assert ad is not None
        inline = ad.find("v:InLine", NS)
        assert inline is not None

    def test_ad_system(self):
        root = ET.fromstring(self.xml)
        ad_system = root.find(".//v:AdSystem", NS)
        assert ad_system is not None
        assert ad_system.text == "DreamTraffic"

    def test_duration(self):
        root = ET.fromstring(self.xml)
        duration = root.find(".//v:Duration", NS)
        assert duration is not None
        assert duration.text == "00:00:30"

    def test_media_file(self):
        root = ET.fromstring(self.xml)
        mf = root.find(".//v:MediaFile", NS)
        assert mf is not None
        assert mf.text == "https://cdn.example.com/video.mp4"
        assert mf.attrib["type"] == "video/mp4"
        assert mf.attrib["width"] == "1920"

    def test_ad_verifications(self):
        root = ET.fromstring(self.xml)
        verifications = root.findall(".//v:Verification", NS)
        assert len(verifications) == 3

    def test_ias_verification(self):
        root = ET.fromstring(self.xml)
        verifications = root.findall(".//v:Verification", NS)
        vendors = [v.attrib.get("vendor", "") for v in verifications]
        assert "ias-pub-291582" in vendors

    def test_omid_api_framework(self):
        root = ET.fromstring(self.xml)
        js_resources = root.findall(".//v:JavaScriptResource", NS)
        for js in js_resources:
            assert js.attrib["apiFramework"] == "omid"

    def test_tracking_events(self):
        root = ET.fromstring(self.xml)
        events = root.findall(".//v:Tracking", NS)
        event_types = {e.attrib["event"] for e in events}
        required = {"start", "firstQuartile", "midpoint", "thirdQuartile", "complete"}
        assert required.issubset(event_types)

    def test_video_clicks(self):
        root = ET.fromstring(self.xml)
        click_through = root.find(".//v:ClickThrough", NS)
        assert click_through is not None
        assert "lumalabs.ai" in click_through.text

    def test_impression_tracking(self):
        root = ET.fromstring(self.xml)
        impression = root.find(".//v:Impression", NS)
        assert impression is not None
        assert "dreamtraffic.demo" in impression.text

    def test_no_vendors(self):
        xml = self.gen.generate_inline(
            video_url="https://cdn.example.com/video.mp4",
            duration="00:00:15",
            vendors=[],
        )
        root = ET.fromstring(xml)
        verifications = root.findall(".//v:Verification", NS)
        assert len(verifications) == 0

    def test_xmlns_present(self):
        assert 'xmlns="http://www.iab.com/VAST"' in self.xml


class TestVastWrapper:
    def test_wrapper_structure(self):
        gen = VastGenerator()
        xml = gen.generate_wrapper(
            vast_ad_tag_uri="https://vast.example.com/original",
            vendors=["ias"],
        )
        root = ET.fromstring(xml)
        wrapper = root.find(".//v:Wrapper", NS)
        assert wrapper is not None

    def test_wrapper_has_tag_uri(self):
        gen = VastGenerator()
        xml = gen.generate_wrapper(
            vast_ad_tag_uri="https://vast.example.com/original",
        )
        root = ET.fromstring(xml)
        uri = root.find(".//v:VASTAdTagURI", NS)
        assert uri is not None
        assert uri.text == "https://vast.example.com/original"

    def test_wrapper_tracking(self):
        gen = VastGenerator()
        xml = gen.generate_wrapper(
            vast_ad_tag_uri="https://vast.example.com/original",
        )
        root = ET.fromstring(xml)
        events = root.findall(".//v:Tracking", NS)
        assert len(events) > 0
