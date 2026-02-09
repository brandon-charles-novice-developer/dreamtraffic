"""Creative Director agent — campaign brief to Luma-optimized video prompts."""

from __future__ import annotations

import asyncio

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AssistantMessage, TextBlock

from dreamtraffic.config import MODELS
from dreamtraffic.tools.server import create_dreamtraffic_server, TOOL_NAMES
from dreamtraffic.agents.definitions import CREATIVE_DIRECTOR_PROMPT


class CreativeDirectorAgent:
    """Orchestrates creative generation from campaign brief to Luma video."""

    name = "creative_director"
    model = MODELS["director"]

    def __init__(self) -> None:
        self._server = create_dreamtraffic_server()

    async def run(self, brief: str) -> str:
        """Generate creatives from a campaign brief. Returns summary."""
        options = ClaudeAgentOptions(
            model=self.model,
            system_prompt=CREATIVE_DIRECTOR_PROMPT,
            mcp_servers={"dreamtraffic": self._server},
            allowed_tools=TOOL_NAMES,
        )

        messages: list[str] = []
        async with ClaudeSDKClient(options=options) as client:
            await client.query(
                f"Given this campaign brief, generate placement-optimized video creatives "
                f"using Luma Dream Machine:\n\n{brief}"
            )
            async for msg in client.receive_response():
                if isinstance(msg, AssistantMessage):
                    for block in msg.content:
                        if isinstance(block, TextBlock):
                            messages.append(block.text)

        return "\n".join(messages)
