"""Bidswitch exchange routing — T-Groups, SmartSwitch, DSP↔SSP matching.

PRODUCTION NOTE: Placeholder that models Bidswitch's routing logic.
Real integration involves Bidswitch's proprietary API for supply path
management, T-Group configuration, and SmartSwitch ML optimization.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field

from dreamtraffic.exchange.ssp import SSPRegistry


@dataclass
class RouteResult:
    """Result of exchange routing for a DSP→SSP path."""
    dsp: str
    ssp: str
    t_group: str
    smartswitch_score: float
    estimated_latency_ms: int
    estimated_win_rate: float
    fee_pct: float
    route_type: str  # "t_group" | "smartswitch" | "direct"
    _simulated: bool = True


@dataclass
class TGroup:
    """Bidswitch T-Group — explicit DSP targeting rules for supply."""
    name: str
    dsp: str
    allowed_ssps: list[str] = field(default_factory=list)
    blocked_ssps: list[str] = field(default_factory=list)
    geo_targets: list[str] = field(default_factory=lambda: ["US"])
    format_filter: list[str] = field(default_factory=lambda: ["olv", "stv"])
    min_bid_floor: float = 0.0


class BidswitchRouter:
    """Simulate Bidswitch exchange routing between DSPs and SSPs."""

    # Pre-configured T-Groups per DSP
    T_GROUPS: dict[str, TGroup] = {
        "amazon_premium": TGroup(
            name="amazon_premium",
            dsp="amazon",
            allowed_ssps=["magnite", "pubmatic", "index_exchange"],
            format_filter=["olv", "stv"],
            min_bid_floor=5.0,
        ),
        "ttd_open": TGroup(
            name="ttd_open",
            dsp="thetradedesk",
            allowed_ssps=["magnite", "pubmatic", "index_exchange"],
            format_filter=["olv", "stv"],
            min_bid_floor=3.0,
        ),
        "dv360_google": TGroup(
            name="dv360_google",
            dsp="dv360",
            allowed_ssps=["magnite", "pubmatic", "index_exchange"],
            format_filter=["olv", "stv"],
            min_bid_floor=4.0,
        ),
        "challenger_broad": TGroup(
            name="challenger_broad",
            dsp="challenger",
            allowed_ssps=["pubmatic", "magnite"],
            format_filter=["olv"],
            min_bid_floor=2.0,
        ),
    }

    # Bidswitch fee tiers
    BASE_FEE_PCT = 2.0
    PREMIUM_FEE_PCT = 1.5  # high-volume DSPs
    CHALLENGER_FEE_PCT = 2.5

    def route(self, dsp: str, placement_type: str = "olv") -> list[RouteResult]:
        """Route a DSP to eligible SSPs via T-Group filtering + SmartSwitch scoring.

        PRODUCTION NOTE: Real SmartSwitch uses ML models trained on historical
        win rates, latency, and fill rates to optimize routing in real-time.
        """
        # Find applicable T-Groups
        t_group = self._find_t_group(dsp)
        if t_group is None:
            # Fallback: route to all SSPs
            eligible_ssps = [s.key for s in SSPRegistry.list_all()]
        else:
            eligible_ssps = [
                s for s in t_group.allowed_ssps
                if s not in t_group.blocked_ssps
            ]

        # Filter by placement type
        available_ssps = []
        for ssp_key in eligible_ssps:
            ssp = SSPRegistry.get(ssp_key)
            if placement_type in ssp.supported_formats:
                available_ssps.append(ssp_key)

        # SmartSwitch scoring (simulated)
        results = []
        for ssp_key in available_ssps:
            score = self._smartswitch_score(dsp, ssp_key)
            fee = self._get_fee(dsp)
            results.append(RouteResult(
                dsp=dsp,
                ssp=ssp_key,
                t_group=t_group.name if t_group else "default",
                smartswitch_score=score,
                estimated_latency_ms=random.randint(60, 120),
                estimated_win_rate=round(random.uniform(0.08, 0.22), 3),
                fee_pct=fee,
                route_type="t_group" if t_group else "smartswitch",
                _simulated=True,
            ))

        # Sort by SmartSwitch score descending
        results.sort(key=lambda r: r.smartswitch_score, reverse=True)
        return results

    def get_supply_map(self) -> dict[str, list[str]]:
        """Get the full DSP→SSP routing map."""
        supply_map = {}
        for tg in self.T_GROUPS.values():
            supply_map[tg.dsp] = tg.allowed_ssps
        return supply_map

    def _find_t_group(self, dsp: str) -> TGroup | None:
        """Find the best T-Group for a DSP."""
        for tg in self.T_GROUPS.values():
            if tg.dsp == dsp:
                return tg
        # Check challenger
        if dsp in ("stackadapt", "adelphic"):
            return self.T_GROUPS.get("challenger_broad")
        return None

    def _smartswitch_score(self, dsp: str, ssp: str) -> float:
        """Simulate SmartSwitch ML scoring.

        PRODUCTION NOTE: Real scoring uses features like:
        - Historical win rate for this DSP↔SSP pair
        - Latency percentiles
        - Fill rate trends
        - Bid floor alignment
        - Format compatibility depth
        """
        # Deterministic-ish scoring based on known good pairings
        preferred = {
            ("amazon", "magnite"): 0.92,
            ("amazon", "pubmatic"): 0.88,
            ("amazon", "index_exchange"): 0.85,
            ("thetradedesk", "pubmatic"): 0.90,
            ("thetradedesk", "magnite"): 0.87,
            ("thetradedesk", "index_exchange"): 0.84,
            ("dv360", "freewheel"): 0.95,
            ("dv360", "magnite"): 0.88,
        }
        base = preferred.get((dsp, ssp), 0.75)
        # Add slight randomness for realism
        return round(base + random.uniform(-0.03, 0.03), 3)

    def _get_fee(self, dsp: str) -> float:
        """Get Bidswitch fee tier for a DSP."""
        if dsp in ("amazon", "thetradedesk", "dv360"):
            return self.PREMIUM_FEE_PCT
        return self.CHALLENGER_FEE_PCT
