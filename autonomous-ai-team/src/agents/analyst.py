"""
Analyst Agent - Market research, competitive analysis, and opportunity identification.
"""

from src.core.agent_base import SpecialistAgent
from src.core.prompts import PROMPTS


class AnalystAgent(SpecialistAgent):
    """
    The Analyst Agent specializes in:
    - Market research and sizing
    - Competitive analysis
    - Opportunity identification
    - Data-driven insights
    """

    def __init__(self, model: str = None):
        super().__init__(
            agent_id="analyst",
            specialty="market_research_and_analysis",
            model=model
        )

    @property
    def system_prompt(self) -> str:
        """Return the Analyst agent's system prompt."""
        return PROMPTS["analyst"]
