"""Measurement vendor configurations — IAS, MOAT, DoubleVerify."""

from __future__ import annotations

from dataclasses import dataclass

from dreamtraffic.config import MEASUREMENT_VENDORS


@dataclass
class VendorConfig:
    key: str
    name: str
    verification_url: str
    js_url: str
    cpm: float
    vendor_key: str = ""  # VAST AdVerification vendor attribute

    @property
    def omid_partner(self) -> str:
        return f"com.{self.key}"


VENDORS: dict[str, VendorConfig] = {
    "ias": VendorConfig(
        key="ias",
        name="Integral Ad Science",
        verification_url=MEASUREMENT_VENDORS["ias"]["verification_url"],
        js_url=MEASUREMENT_VENDORS["ias"]["js_url"],
        cpm=MEASUREMENT_VENDORS["ias"]["cpm"],
        vendor_key="ias-pub-291582",
    ),
    "moat": VendorConfig(
        key="moat",
        name="Moat by Oracle",
        verification_url=MEASUREMENT_VENDORS["moat"]["verification_url"],
        js_url=MEASUREMENT_VENDORS["moat"]["js_url"],
        cpm=MEASUREMENT_VENDORS["moat"]["cpm"],
        vendor_key="moat-dreamtraffic",
    ),
    "doubleverify": VendorConfig(
        key="doubleverify",
        name="DoubleVerify",
        verification_url=MEASUREMENT_VENDORS["doubleverify"]["verification_url"],
        js_url=MEASUREMENT_VENDORS["doubleverify"]["js_url"],
        cpm=MEASUREMENT_VENDORS["doubleverify"]["cpm"],
        vendor_key="dv-ctx-123456",
    ),
}


def get_vendor_config(vendor_key: str) -> VendorConfig:
    """Get a vendor config by key. Raises KeyError if not found."""
    if vendor_key not in VENDORS:
        raise KeyError(f"Unknown measurement vendor: {vendor_key}. Available: {list(VENDORS.keys())}")
    return VENDORS[vendor_key]
