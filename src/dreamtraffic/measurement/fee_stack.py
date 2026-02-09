"""Full supply chain fee calculator — creative gen through publisher net."""

from __future__ import annotations

from dataclasses import dataclass

from dreamtraffic.db import fetch_all


@dataclass
class FeeBreakdown:
    """Fee breakdown for a single supply path."""
    dsp: str
    exchange: str
    ssp: str
    # Fee percentages
    luma_creative_cpm: float  # amortized cost per 1000 impressions
    dsp_fee_pct: float
    exchange_fee_pct: float
    ssp_fee_pct: float
    measurement_cpm: float  # total measurement vendor CPM
    # Calculated
    total_supply_cost_pct: float = 0.0
    publisher_net_pct: float = 0.0
    effective_cpm_on_10: float = 0.0  # cost breakdown on a $10 CPM
    notes: str = ""

    def __post_init__(self) -> None:
        self.total_supply_cost_pct = self.dsp_fee_pct + self.exchange_fee_pct + self.ssp_fee_pct
        self.publisher_net_pct = 100.0 - self.total_supply_cost_pct


class FeeStackCalculator:
    """Calculate fee stacks across supply paths."""

    # Luma creative generation cost assumptions
    LUMA_COST_PER_VIDEO = 0.50  # estimated per 5s generation
    DEFAULT_IMPRESSION_GOAL = 100_000  # amortize over this many impressions

    def __init__(
        self,
        luma_cost_per_video: float | None = None,
        impression_goal: int | None = None,
    ) -> None:
        self.luma_cost = luma_cost_per_video or self.LUMA_COST_PER_VIDEO
        self.impression_goal = impression_goal or self.DEFAULT_IMPRESSION_GOAL

    @property
    def luma_cpm(self) -> float:
        """Luma creative generation cost amortized as CPM."""
        return (self.luma_cost / self.impression_goal) * 1000

    def calculate_path(
        self,
        dsp_fee_pct: float,
        exchange_fee_pct: float,
        ssp_fee_pct: float,
        measurement_cpm: float,
        *,
        dsp: str = "",
        exchange: str = "",
        ssp: str = "",
        notes: str = "",
    ) -> FeeBreakdown:
        """Calculate fee breakdown for a single supply path."""
        return FeeBreakdown(
            dsp=dsp,
            exchange=exchange,
            ssp=ssp,
            luma_creative_cpm=round(self.luma_cpm, 4),
            dsp_fee_pct=dsp_fee_pct,
            exchange_fee_pct=exchange_fee_pct,
            ssp_fee_pct=ssp_fee_pct,
            measurement_cpm=measurement_cpm,
            notes=notes,
        )

    def calculate_all_paths(self) -> list[FeeBreakdown]:
        """Calculate fee breakdowns for all supply paths in the database."""
        paths = fetch_all("SELECT * FROM supply_paths ORDER BY dsp, ssp")
        results = []
        for p in paths:
            fb = self.calculate_path(
                dsp_fee_pct=p["dsp_fee_pct"],
                exchange_fee_pct=p["exchange_fee_pct"],
                ssp_fee_pct=p["ssp_fee_pct"],
                measurement_cpm=p["measurement_cpm"],
                dsp=p["dsp"],
                exchange=p["exchange"],
                ssp=p["ssp"],
                notes=p["notes"],
            )
            results.append(fb)
        return results

    def compare_dsps(self) -> dict[str, dict]:
        """Compare average fee stacks by DSP. Returns dict keyed by DSP name."""
        all_paths = self.calculate_all_paths()
        dsp_groups: dict[str, list[FeeBreakdown]] = {}
        for fb in all_paths:
            dsp_groups.setdefault(fb.dsp, []).append(fb)

        comparison = {}
        for dsp, breakdowns in sorted(dsp_groups.items()):
            n = len(breakdowns)
            comparison[dsp] = {
                "path_count": n,
                "avg_dsp_fee": round(sum(b.dsp_fee_pct for b in breakdowns) / n, 2),
                "avg_total_supply_cost": round(sum(b.total_supply_cost_pct for b in breakdowns) / n, 2),
                "avg_publisher_net": round(sum(b.publisher_net_pct for b in breakdowns) / n, 2),
                "avg_measurement_cpm": round(sum(b.measurement_cpm for b in breakdowns) / n, 4),
                "luma_creative_cpm": round(self.luma_cpm, 4),
                "paths": [
                    {
                        "exchange": b.exchange,
                        "ssp": b.ssp,
                        "total_cost_pct": b.total_supply_cost_pct,
                        "publisher_net_pct": b.publisher_net_pct,
                    }
                    for b in breakdowns
                ],
            }

        return comparison

    def format_breakdown(self, fb: FeeBreakdown, base_cpm: float = 10.0) -> str:
        """Format a fee breakdown as a readable string."""
        lines = [
            f"Supply Path: {fb.dsp} → {fb.exchange or 'direct'} → {fb.ssp}",
            f"{'─' * 50}",
            f"  Luma Creative Gen    ${fb.luma_creative_cpm:.4f}/CPM (amortized)",
            f"  DSP Fee              {fb.dsp_fee_pct:.1f}%  (${base_cpm * fb.dsp_fee_pct / 100:.2f})",
            f"  Exchange Fee         {fb.exchange_fee_pct:.1f}%  (${base_cpm * fb.exchange_fee_pct / 100:.2f})",
            f"  SSP Fee              {fb.ssp_fee_pct:.1f}%  (${base_cpm * fb.ssp_fee_pct / 100:.2f})",
            f"  Measurement          ${fb.measurement_cpm:.3f}/CPM",
            f"{'─' * 50}",
            f"  Total Supply Cost    {fb.total_supply_cost_pct:.1f}% + measurement",
            f"  Publisher Net        {fb.publisher_net_pct:.1f}%  (${base_cpm * fb.publisher_net_pct / 100:.2f})",
        ]
        if fb.notes:
            lines.append(f"  Note: {fb.notes}")
        return "\n".join(lines)
