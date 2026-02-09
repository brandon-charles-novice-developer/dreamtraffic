"""Tests for CLI commands."""

import pytest
from click.testing import CliRunner

from dreamtraffic.cli import cli


class TestCLI:
    def setup_method(self):
        self.runner = CliRunner()

    def test_init_db(self, test_db):
        # The test_db fixture already sets up the global connection
        result = self.runner.invoke(cli, ["init-db"])
        assert result.exit_code == 0

    def test_demo_command(self, test_db):
        result = self.runner.invoke(cli, ["demo"])
        assert result.exit_code == 0
        assert "Demo complete" in result.output

    def test_help(self):
        result = self.runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "DreamTraffic" in result.output

    def test_status_no_campaigns(self, test_db):
        # The fixture seeds a campaign, so we should see it
        result = self.runner.invoke(cli, ["status"])
        assert result.exit_code == 0
