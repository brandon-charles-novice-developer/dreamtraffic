"""SSP models — Magnite, PubMatic, Index Exchange, FreeWheel.

PRODUCTION NOTE: Placeholder models representing SSP capabilities and
OpenRTB 2.6 bid request/response shapes. Real integration would involve
direct SSP partnerships and header bidding configurations.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SSPConfig:
    """SSP platform configuration and capabilities."""
    key: str
    name: str
    take_rate_pct: float
    supported_formats: list[str] = field(default_factory=list)
    openrtb_version: str = "2.6"
    specialization: str = ""
    streaming_pod_support: bool = False
    header_bidding: bool = False
    notes: str = ""


class SSPRegistry:
    """Registry of SSP configurations."""

    SSPS: dict[str, SSPConfig] = {
        "magnite": SSPConfig(
            key="magnite",
            name="Magnite",
            take_rate_pct=15.0,
            supported_formats=["olv", "stv", "ctv"],
            specialization="Premium video, CTV programmatic guaranteed",
            streaming_pod_support=True,
            header_bidding=True,
            notes="Largest independent sell-side platform. Strong CTV inventory.",
        ),
        "pubmatic": SSPConfig(
            key="pubmatic",
            name="PubMatic",
            take_rate_pct=14.0,
            supported_formats=["olv", "stv"],
            specialization="Cloud infrastructure, OpenWrap header bidding",
            streaming_pod_support=False,
            header_bidding=True,
            notes="Cloud-native SSP. Strong in mobile + video.",
        ),
        "index_exchange": SSPConfig(
            key="index_exchange",
            name="Index Exchange",
            take_rate_pct=12.0,
            supported_formats=["olv", "stv"],
            specialization="Transparency, header bidding marketplace",
            streaming_pod_support=False,
            header_bidding=True,
            notes="Known for supply path transparency and exchange-level reporting.",
        ),
        "freewheel": SSPConfig(
            key="freewheel",
            name="FreeWheel (Comcast)",
            take_rate_pct=18.0,
            supported_formats=["stv", "ctv"],
            specialization="Premium streaming TV, ad pod management",
            streaming_pod_support=True,
            header_bidding=False,
            notes="Premium CTV/streaming supply. OpenRTB 2.6 pod bidding support.",
        ),
    }

    @classmethod
    def get(cls, key: str) -> SSPConfig:
        if key not in cls.SSPS:
            raise KeyError(f"Unknown SSP: {key}. Available: {list(cls.SSPS.keys())}")
        return cls.SSPS[key]

    @classmethod
    def list_all(cls) -> list[SSPConfig]:
        return list(cls.SSPS.values())

    @classmethod
    def simulate_bid_request(cls, ssp_key: str, creative_id: str) -> dict:
        """Simulate an OpenRTB 2.6 bid request from an SSP.

        PRODUCTION NOTE: Real bid requests come from the SSP to DSPs
        with impression opportunities. This simulates the shape.
        """
        ssp = cls.get(ssp_key)
        return {
            "id": f"br-{ssp_key}-{creative_id[:8]}",
            "imp": [{
                "id": "1",
                "video": {
                    "mimes": ["video/mp4"],
                    "protocols": [2, 5, 6],  # VAST 2.0, 3.0, 4.x
                    "w": 1920,
                    "h": 1080,
                    "linearity": 1,  # linear (in-stream)
                    "maxduration": 30,
                    "minduration": 5,
                    "podid": "pod-1" if ssp.streaming_pod_support else None,
                },
                "bidfloor": 8.00,
                "bidfloorcur": "USD",
            }],
            "site": {
                "domain": f"publisher.{ssp_key}.example.com",
                "cat": ["IAB1"],  # Arts & Entertainment
            },
            "device": {
                "ua": "Mozilla/5.0 (CTV)",
                "devicetype": 3,  # Connected TV
            },
            "openrtb_version": ssp.openrtb_version,
            "_simulated": True,
        }

    @classmethod
    def simulate_bid_response(cls, ssp_key: str, creative_id: str, vast_url: str) -> dict:
        """Simulate an OpenRTB 2.6 bid response.

        PRODUCTION NOTE: Real bid responses go from DSP to SSP
        with creative + bid price.
        """
        return {
            "id": f"bresp-{ssp_key}-{creative_id[:8]}",
            "seatbid": [{
                "bid": [{
                    "id": f"bid-{creative_id[:8]}",
                    "impid": "1",
                    "price": 10.50,
                    "adm": vast_url,
                    "crid": creative_id,
                    "w": 1920,
                    "h": 1080,
                }],
                "seat": "dreamtraffic",
            }],
            "cur": "USD",
            "_simulated": True,
        }
