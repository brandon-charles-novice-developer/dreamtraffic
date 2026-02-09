"""Trafficking Manager agent — DSP upload, VAST generation, audit tracking."""

from __future__ import annotations

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AssistantMessage, TextBlock

from dreamtraffic.config import MODELS
from dreamtraffic.tools.server import create_dreamtraffic_server, TOOL_NAMES
from dreamtraffic.agents.definitions import TRAFFICKING_MANAGER_PROMPT


class TraffickingManagerAgent:
    """Handles creative trafficking across DSPs with VAST tag generation."""

    name = "trafficking_manager"
    model = MODELS["trafficking"]

    def __init__(self) -> None:
        self._server = create_dreamtraffic_server()

    async def run(self, creative_id: int, dsps: list[str] | None = None) -> str:
        """Traffic an approved creative to specified DSPs."""
        dsp_list = dsps or ["amazon", "thetradedesk", "dv360"]
        dsp_str = ", ".join(dsp_list)

        options = ClaudeAgentOptions(
            model=self.model,
            system_prompt=TRAFFICKING_MANAGER_PROMPT,
            mcp_servers={"dreamtraffic": self._server},
            allowed_tools=TOOL_NAMES,
        )

        messages: list[str] = []
        async with ClaudeSDKClient(options=options) as client:
            await client.query(
                f"Traffic creative ID {creative_id} to these DSPs: {dsp_str}. "
                f"First generate the VAST tag with all measurement vendors, "
                f"then upload to each DSP and report the results."
            )
            async for msg in client.receive_response():
                if isinstance(msg, AssistantMessage):
                    for block in msg.content:
                        if isinstance(block, TextBlock):
                            messages.append(block.text)

        return "\n".join(messages)
