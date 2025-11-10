"""
Growth Hacker Agent - Customer acquisition strategies, growth experiments, metrics tracking.
"""

from src.core.agent_base import SpecialistAgent
from src.core.prompts import PROMPTS


class GrowthHackerAgent(SpecialistAgent):
    """
    The Growth Hacker Agent specializes in:
    - Customer acquisition strategies
    - Growth experiment design
    - Viral loop mechanics
    - Metrics and KPI tracking
    - Rapid scaling tactics
    """

    def __init__(self, model: str = None):
        super().__init__(
            agent_id="growth_hacker",
            specialty="customer_acquisition_and_growth",
            model=model
        )

    @property
    def system_prompt(self) -> str:
        """Return the Growth Hacker agent's system prompt."""
        return PROMPTS["growth_hacker"]
