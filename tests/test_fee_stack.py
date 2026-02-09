"""Tests for fee stack calculator."""

import pytest

from dreamtraffic.measurement.fee_stack import FeeStackCalculator, FeeBreakdown


class TestFeeBreakdown:
    def test_total_supply_cost(self):
        fb = FeeBreakdown(
            dsp="amazon", exchange="bidswitch", ssp="magnite",
            luma_creative_cpm=0.005,
            dsp_fee_pct=12.0, exchange_fee_pct=2.0, ssp_fee_pct=15.0,
            measurement_cpm=0.02,
        )
        assert fb.total_supply_cost_pct == 29.0
        assert fb.publisher_net_pct == 71.0


class TestFeeStackCalculator:
    def test_luma_cpm(self):
        calc = FeeStackCalculator(luma_cost_per_video=0.50, impression_goal=100_000)
        assert calc.luma_cpm == pytest.approx(0.005)

    def test_calculate_path(self):
        calc = FeeStackCalculator()
        fb = calc.calculate_path(
            dsp_fee_pct=12.0, exchange_fee_pct=2.0, ssp_fee_pct=15.0,
            measurement_cpm=0.02, dsp="amazon", ssp="magnite",
        )
        assert fb.total_supply_cost_pct == 29.0
        assert fb.publisher_net_pct == 71.0

    def test_calculate_all_paths(self, test_db):
        calc = FeeStackCalculator()
        paths = calc.calculate_all_paths()
        assert len(paths) > 0
        for p in paths:
            assert p.total_supply_cost_pct > 0
            assert p.publisher_net_pct > 0

    def test_compare_dsps(self, test_db):
        calc = FeeStackCalculator()
        comparison = calc.compare_dsps()
        assert "amazon" in comparison
        assert "thetradedesk" in comparison
        # Amazon should have lower avg cost than TTD (post-June 2025 reduction)
        assert comparison["amazon"]["avg_dsp_fee"] < comparison["thetradedesk"]["avg_dsp_fee"]

    def test_format_breakdown(self):
        calc = FeeStackCalculator()
        fb = calc.calculate_path(
            dsp_fee_pct=12.0, exchange_fee_pct=2.0, ssp_fee_pct=15.0,
            measurement_cpm=0.02, dsp="amazon", exchange="bidswitch", ssp="magnite",
        )
        formatted = calc.format_breakdown(fb)
        assert "amazon" in formatted
        assert "magnite" in formatted
        assert "12.0%" in formatted
        assert "29.0%" in formatted

    def test_adsp_advantage(self, test_db):
        """Verify ADSP has lower fees than TTD — the strategic narrative."""
        calc = FeeStackCalculator()
        comparison = calc.compare_dsps()
        adsp = comparison["amazon"]
        ttd = comparison["thetradedesk"]
        savings = ttd["avg_total_supply_cost"] - adsp["avg_total_supply_cost"]
        assert savings > 0, "ADSP should have lower total supply cost than TTD"
