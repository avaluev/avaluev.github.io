"""
System Builder Agent - Process documentation, automation workflows, scaling plans.
"""

from src.core.agent_base import SpecialistAgent
from src.core.prompts import PROMPTS


class SystemBuilderAgent(SpecialistAgent):
    """
    The System Builder Agent specializes in:
    - Process mapping and documentation
    - Automation workflow design
    - Standard Operating Procedures (SOPs)
    - Scaling playbooks
    - Operational excellence
    """

    def __init__(self, model: str = None):
        super().__init__(
            agent_id="system_builder",
            specialty="process_automation_and_scaling",
            model=model
        )

    @property
    def system_prompt(self) -> str:
        """Return the System Builder agent's system prompt."""
        return PROMPTS["system_builder"]
