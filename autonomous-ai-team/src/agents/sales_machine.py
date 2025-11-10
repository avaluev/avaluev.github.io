"""
Sales Machine Agent - Sales copy generation, conversion optimization, offer design.
"""

from src.core.agent_base import SpecialistAgent
from src.core.prompts import PROMPTS


class SalesMachineAgent(SpecialistAgent):
    """
    The Sales Machine Agent specializes in:
    - High-converting sales copy
    - Irresistible offer design
    - Objection handling
    - Email sequences
    - Landing page optimization
    """

    def __init__(self, model: str = None):
        super().__init__(
            agent_id="sales_machine",
            specialty="sales_copy_and_conversion",
            model=model
        )

    @property
    def system_prompt(self) -> str:
        """Return the Sales Machine agent's system prompt."""
        return PROMPTS["sales_machine"]
