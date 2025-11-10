"""
Brand Builder Agent - Content creation, authority building, audience engagement.
"""

from src.core.agent_base import SpecialistAgent
from src.core.prompts import PROMPTS


class BrandBuilderAgent(SpecialistAgent):
    """
    The Brand Builder Agent specializes in:
    - Content strategy and creation
    - Thought leadership
    - SEO optimization
    - Social media content
    - Authority building
    """

    def __init__(self, model: str = None):
        super().__init__(
            agent_id="brand_builder",
            specialty="content_and_authority_building",
            model=model
        )

    @property
    def system_prompt(self) -> str:
        """Return the Brand Builder agent's system prompt."""
        return PROMPTS["brand_builder"]
