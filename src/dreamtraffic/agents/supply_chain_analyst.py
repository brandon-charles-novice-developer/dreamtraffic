"""Supply Chain Analyst agent — fee stack analysis, supply path optimization."""

from __future__ import annotations

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AssistantMessage, TextBlock

from dreamtraffic.config import MODELS
from dreamtraffic.tools.server import create_dreamtraffic_server, TOOL_NAMES
from dreamtraffic.agents.definitions import SUPPLY_CHAIN_ANALYST_PROMPT


class SupplyChainAnalystAgent:
    """Analyzes supply paths and fee stacks across the programmatic chain."""

    name = "supply_chain_analyst"
    model = MODELS["analyst"]

    def __init__(self) -> None:
        self._server = create_dreamtraffic_server()

    async def run(self, creative_id: int | None = None) -> str:
        """Analyze supply chain for a creative or general fee comparison."""
        options = ClaudeAgentOptions(
            model=self.model,
            system_prompt=SUPPLY_CHAIN_ANALYST_PROMPT,
            mcp_servers={"dreamtraffic": self._server},
            allowed_tools=TOOL_NAMES,
        )

        if creative_id:
            query = (
                f"Analyze the supply chain for creative ID {creative_id}. "
                f"Route through Bidswitch, calculate fee stacks for all paths, "
                f"and recommend optimal supply paths. Highlight where Luma "
                f"creative generation costs fit in the ADSP fee advantage."
            )
        else:
            query = (
                "Perform a comprehensive supply chain analysis. "
                "Compare all DSP fee stacks, route through Bidswitch, "
                "and highlight the ADSP fee advantage for Luma AI creative generation. "
                "Show the full fee breakdown for each path."
            )

        messages: list[str] = []
        async with ClaudeSDKClient(options=options) as client:
            await client.query(query)
            async for msg in client.receive_response():
                if isinstance(msg, AssistantMessage):
                    for block in msg.content:
                        if isinstance(block, TextBlock):
                            messages.append(block.text)

        return "\n".join(messages)
