"""Compliance Reviewer agent — validates creatives against IAB/DSP specs."""

from __future__ import annotations

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AssistantMessage, TextBlock

from dreamtraffic.config import MODELS
from dreamtraffic.tools.server import create_dreamtraffic_server, TOOL_NAMES
from dreamtraffic.agents.definitions import COMPLIANCE_REVIEWER_PROMPT


class ComplianceReviewerAgent:
    """Reviews creatives for compliance with DSP specs and measurement requirements."""

    name = "compliance_reviewer"
    model = MODELS["compliance"]

    def __init__(self) -> None:
        self._server = create_dreamtraffic_server()

    async def run(self, creative_id: int) -> str:
        """Review a creative and approve or request revision."""
        options = ClaudeAgentOptions(
            model=self.model,
            system_prompt=COMPLIANCE_REVIEWER_PROMPT,
            mcp_servers={"dreamtraffic": self._server},
            allowed_tools=TOOL_NAMES,
        )

        messages: list[str] = []
        async with ClaudeSDKClient(options=options) as client:
            await client.query(
                f"Review creative ID {creative_id} for compliance. "
                f"Check all DSP specs, measurement requirements, and format validation. "
                f"Approve or request revision with specific feedback."
            )
            async for msg in client.receive_response():
                if isinstance(msg, AssistantMessage):
                    for block in msg.content:
                        if isinstance(block, TextBlock):
                            messages.append(block.text)

        return "\n".join(messages)
