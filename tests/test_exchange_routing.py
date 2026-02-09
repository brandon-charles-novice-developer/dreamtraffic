"""Tests for Bidswitch exchange routing and SSP models."""

import pytest

from dreamtraffic.exchange.bidswitch import BidswitchRouter
from dreamtraffic.exchange.ssp import SSPRegistry


class TestSSPRegistry:
    def test_get_magnite(self):
        ssp = SSPRegistry.get("magnite")
        assert ssp.name == "Magnite"
        assert ssp.take_rate_pct == 15.0

    def test_get_freewheel(self):
        ssp = SSPRegistry.get("freewheel")
        assert ssp.streaming_pod_support is True

    def test_unknown_ssp_raises(self):
        with pytest.raises(KeyError, match="Unknown SSP"):
            SSPRegistry.get("nonexistent")

    def test_list_all(self):
        all_ssps = SSPRegistry.list_all()
        assert len(all_ssps) == 4
        keys = {s.key for s in all_ssps}
        assert keys == {"magnite", "pubmatic", "index_exchange", "freewheel"}

    def test_simulate_bid_request(self):
        br = SSPRegistry.simulate_bid_request("magnite", "test-creative")
        assert "imp" in br
        assert br["imp"][0]["video"]["w"] == 1920
        assert br["_simulated"] is True

    def test_simulate_bid_response(self):
        resp = SSPRegistry.simulate_bid_response("magnite", "test-creative", "https://vast.example.com")
        assert "seatbid" in resp
        assert resp["seatbid"][0]["bid"][0]["price"] == 10.50

    def test_freewheel_has_pod_support(self):
        br = SSPRegistry.simulate_bid_request("freewheel", "test")
        assert br["imp"][0]["video"]["podid"] is not None

    def test_non_pod_ssp_no_podid(self):
        br = SSPRegistry.simulate_bid_request("pubmatic", "test")
        assert br["imp"][0]["video"]["podid"] is None


class TestBidswitchRouter:
    def setup_method(self):
        self.router = BidswitchRouter()

    def test_route_amazon(self):
        routes = self.router.route("amazon", "olv")
        assert len(routes) > 0
        ssps = {r.ssp for r in routes}
        assert "magnite" in ssps

    def test_route_ttd(self):
        routes = self.router.route("thetradedesk", "olv")
        assert len(routes) > 0

    def test_route_dv360(self):
        routes = self.router.route("dv360", "olv")
        assert len(routes) > 0

    def test_routes_sorted_by_score(self):
        routes = self.router.route("amazon", "olv")
        scores = [r.smartswitch_score for r in routes]
        assert scores == sorted(scores, reverse=True)

    def test_route_has_fee(self):
        routes = self.router.route("amazon", "olv")
        for r in routes:
            assert r.fee_pct > 0

    def test_challenger_routing(self):
        routes = self.router.route("stackadapt", "olv")
        assert len(routes) > 0
        for r in routes:
            assert r.fee_pct == 2.5  # challenger fee tier

    def test_supply_map(self):
        supply_map = self.router.get_supply_map()
        assert "amazon" in supply_map
        assert "magnite" in supply_map["amazon"]

    def test_all_routes_simulated(self):
        routes = self.router.route("amazon", "olv")
        for r in routes:
            assert r._simulated is True

    def test_stv_routing_filters(self):
        routes = self.router.route("amazon", "stv")
        for r in routes:
            ssp = SSPRegistry.get(r.ssp)
            assert "stv" in ssp.supported_formats
