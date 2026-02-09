"""VAST 4.2 XML generator with InLine, Wrapper, and AdVerification support."""

from __future__ import annotations

import uuid
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString

from dreamtraffic.measurement.vendors import VendorConfig, VENDORS


class VastGenerator:
    """Generate VAST 4.2 XML with measurement vendor wrapping."""

    TRACKING_EVENTS = [
        "start", "firstQuartile", "midpoint", "thirdQuartile",
        "complete", "pause", "resume", "mute", "unmute",
        "fullscreen", "exitFullscreen", "skip",
    ]

    def __init__(self) -> None:
        self._cache_buster = "[CACHEBUSTING]"
        self._timestamp = "[TIMESTAMP]"

    def generate_inline(
        self,
        *,
        video_url: str,
        duration: str = "00:00:30",
        title: str = "DreamTraffic Creative",
        advertiser: str = "DreamTraffic Demo",
        vendors: list[str] | None = None,
        click_through: str = "https://lumalabs.ai",
        ad_id: str | None = None,
    ) -> str:
        """Generate a VAST 4.2 InLine tag with AdVerification elements."""
        ad_id = ad_id or f"dt-{uuid.uuid4().hex[:12]}"
        vendor_configs = self._resolve_vendors(vendors)

        vast = Element("VAST", version="4.2")
        ad = SubElement(vast, "Ad", id=ad_id)
        inline = SubElement(ad, "InLine")

        SubElement(inline, "AdSystem").text = "DreamTraffic"
        SubElement(inline, "AdTitle").text = title
        SubElement(inline, "Advertiser").text = advertiser

        impression = SubElement(inline, "Impression", id="dt-imp")
        impression.text = f"https://track.dreamtraffic.demo/impression?id={ad_id}&cb={self._cache_buster}"

        # AdVerification — OMID-compliant elements for each measurement vendor
        if vendor_configs:
            verifications = SubElement(inline, "AdVerifications")
            for vc in vendor_configs:
                self._add_verification(verifications, vc)

        # Creatives
        creatives = SubElement(inline, "Creatives")
        creative = SubElement(creatives, "Creative", id=f"creative-{ad_id}", adId=ad_id)
        linear = SubElement(creative, "Linear")
        SubElement(linear, "Duration").text = duration

        # MediaFiles
        media_files = SubElement(linear, "MediaFiles")
        mf = SubElement(
            media_files, "MediaFile",
            delivery="progressive",
            type="video/mp4",
            width="1920",
            height="1080",
            codec="H.264",
            bitrate="5000",
        )
        mf.text = video_url

        # TrackingEvents
        tracking_events = SubElement(linear, "TrackingEvents")
        for event in self.TRACKING_EVENTS:
            te = SubElement(tracking_events, "Tracking", event=event)
            te.text = (
                f"https://track.dreamtraffic.demo/{event}"
                f"?id={ad_id}&cb={self._cache_buster}&ts={self._timestamp}"
            )

        # VideoClicks
        video_clicks = SubElement(linear, "VideoClicks")
        ct = SubElement(video_clicks, "ClickThrough", id="dt-click")
        ct.text = click_through
        click_track = SubElement(video_clicks, "ClickTracking", id="dt-click-track")
        click_track.text = f"https://track.dreamtraffic.demo/click?id={ad_id}&cb={self._cache_buster}"

        return self._prettify(vast)

    def generate_wrapper(
        self,
        *,
        vast_ad_tag_uri: str,
        vendors: list[str] | None = None,
        ad_id: str | None = None,
    ) -> str:
        """Generate a VAST 4.2 Wrapper tag that references another VAST tag."""
        ad_id = ad_id or f"dt-wrapper-{uuid.uuid4().hex[:8]}"
        vendor_configs = self._resolve_vendors(vendors)

        vast = Element("VAST", version="4.2")
        ad = SubElement(vast, "Ad", id=ad_id)
        wrapper = SubElement(ad, "Wrapper")

        SubElement(wrapper, "AdSystem").text = "DreamTraffic Wrapper"

        tag_uri = SubElement(wrapper, "VASTAdTagURI")
        tag_uri.text = vast_ad_tag_uri

        impression = SubElement(wrapper, "Impression", id="dt-wrapper-imp")
        impression.text = f"https://track.dreamtraffic.demo/wrapper-impression?id={ad_id}&cb={self._cache_buster}"

        if vendor_configs:
            verifications = SubElement(wrapper, "AdVerifications")
            for vc in vendor_configs:
                self._add_verification(verifications, vc)

        # Wrapper tracking events
        creatives = SubElement(wrapper, "Creatives")
        creative = SubElement(creatives, "Creative")
        linear = SubElement(creative, "Linear")
        tracking_events = SubElement(linear, "TrackingEvents")
        for event in ["start", "firstQuartile", "midpoint", "thirdQuartile", "complete"]:
            te = SubElement(tracking_events, "Tracking", event=event)
            te.text = (
                f"https://track.dreamtraffic.demo/wrapper-{event}"
                f"?id={ad_id}&cb={self._cache_buster}"
            )

        return self._prettify(vast)

    def _add_verification(self, parent: Element, vendor: VendorConfig) -> None:
        """Add an OMID-compliant AdVerification element."""
        verification = SubElement(parent, "Verification", vendor=vendor.vendor_key)

        js_resource = SubElement(
            verification, "JavaScriptResource",
            apiFramework="omid",
            browserOptional="true",
        )
        js_resource.text = vendor.js_url

        tracking = SubElement(verification, "TrackingEvents")
        ve = SubElement(tracking, "Tracking", event="verificationNotExecuted")
        ve.text = (
            f"{vendor.verification_url}/verify-not-executed"
            f"?vendor={vendor.key}&reason=[REASON]"
        )

        vp = SubElement(verification, "VerificationParameters")
        vp.text = f'{{"partner":"{vendor.omid_partner}","vendorKey":"{vendor.vendor_key}"}}'

    def _resolve_vendors(self, vendor_keys: list[str] | None) -> list[VendorConfig]:
        """Resolve vendor keys to configs. Default: all vendors."""
        if vendor_keys is None:
            return list(VENDORS.values())
        return [VENDORS[k] for k in vendor_keys if k in VENDORS]

    def _prettify(self, elem: Element) -> str:
        """Pretty-print XML with proper indentation."""
        raw = tostring(elem, encoding="unicode", xml_declaration=False)
        dom = parseString(raw)
        pretty = dom.toprettyxml(indent="  ", encoding=None)
        # Remove the XML declaration that minidom adds
        lines = pretty.split("\n")
        if lines[0].startswith("<?xml"):
            lines = lines[1:]
        result = "\n".join(lines).strip()
        # Add xmlns to the VAST element for spec compliance
        result = result.replace(
            '<VAST version="4.2">',
            '<VAST version="4.2" xmlns="http://www.iab.com/VAST">',
        )
        return result
