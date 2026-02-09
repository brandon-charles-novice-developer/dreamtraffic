"""Tests for Luma client — mocked (no real API calls in tests)."""

from unittest.mock import MagicMock, patch

import pytest

from dreamtraffic.luma.client import LumaClient


class TestLumaClient:
    @patch("dreamtraffic.luma.client.LumaAI")
    def test_generate_returns_id(self, mock_luma_class):
        mock_client = MagicMock()
        mock_luma_class.return_value = mock_client

        mock_gen = MagicMock()
        mock_gen.id = "gen-abc123"
        mock_client.generations.create.return_value = mock_gen

        client = LumaClient(api_key="test-key")
        gen_id = client.generate("test prompt")
        assert gen_id == "gen-abc123"

    @patch("dreamtraffic.luma.client.LumaAI")
    def test_poll_success(self, mock_luma_class):
        mock_client = MagicMock()
        mock_luma_class.return_value = mock_client

        mock_gen = MagicMock()
        mock_gen.id = "gen-abc123"
        mock_gen.state = "completed"
        mock_gen.assets.video = "https://cdn.luma.example/output.mp4"
        mock_gen.assets.thumbnail = "https://cdn.luma.example/thumb.jpg"
        mock_client.generations.get.return_value = mock_gen

        client = LumaClient(api_key="test-key")
        result = client.poll("gen-abc123")
        assert result["state"] == "completed"
        assert result["video_url"] == "https://cdn.luma.example/output.mp4"

    @patch("dreamtraffic.luma.client.LumaAI")
    def test_poll_failure(self, mock_luma_class):
        mock_client = MagicMock()
        mock_luma_class.return_value = mock_client

        mock_gen = MagicMock()
        mock_gen.state = "failed"
        mock_gen.failure_reason = "content policy violation"
        mock_client.generations.get.return_value = mock_gen

        client = LumaClient(api_key="test-key")
        with pytest.raises(RuntimeError, match="failed"):
            client.poll("gen-abc123")

    @patch("dreamtraffic.luma.client.LumaAI")
    def test_generate_passes_params(self, mock_luma_class):
        mock_client = MagicMock()
        mock_luma_class.return_value = mock_client

        mock_gen = MagicMock()
        mock_gen.id = "gen-123"
        mock_client.generations.create.return_value = mock_gen

        client = LumaClient(api_key="test-key")
        client.generate("test", duration="5s", resolution="1080p", aspect_ratio="16:9")

        mock_client.generations.create.assert_called_once_with(
            prompt="test",
            model="ray2",
            resolution="1080p",
            duration="5s",
            aspect_ratio="16:9",
            loop=False,
        )
