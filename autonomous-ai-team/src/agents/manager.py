"""
Manager Agent - Orchestrates the team of specialist agents.
This is the central coordinator that routes tasks and manages the workflow.
"""

from typing import Dict, Any, List
import json

from src.core.agent_base import AgentBase
from src.core.prompts import PROMPTS
from src.core.logger import get_logger

# Import specialist agents
from .analyst import AnalystAgent
from .growth_hacker import GrowthHackerAgent
from .sales_machine import SalesMachineAgent
from .system_builder import SystemBuilderAgent
from .brand_builder import BrandBuilderAgent

logger = get_logger(__name__)


class ManagerAgent(AgentBase):
    """
    The Manager Agent coordinates all specialist agents.
    It analyzes requests, routes to appropriate specialists, and synthesizes results.
    """

    def __init__(self, model: str = None):
        super().__init__(
            agent_id="manager",
            model=model,
            temperature=0.7
        )

        # Initialize specialist agents
        self.specialist_agents = {
            "analyst": AnalystAgent(model=model),
            "growth_hacker": GrowthHackerAgent(model=model),
            "sales_machine": SalesMachineAgent(model=model),
            "system_builder": SystemBuilderAgent(model=model),
            "brand_builder": BrandBuilderAgent(model=model)
        }

        logger.info(
            "manager_agent_initialized",
            specialist_count=len(self.specialist_agents)
        )

    @property
    def system_prompt(self) -> str:
        """Return the Manager agent's system prompt."""
        return PROMPTS["manager"]

    @property
    def available_tools(self) -> List[Dict[str, Any]]:
        """
        Manager agent has access to specialist agents as tools,
        plus the standard tools.
        """
        # Start with standard tools
        tools = super().available_tools

        # Add specialist agent tools
        specialist_tools = [
            {
                "name": "call_analyst_agent",
                "description": (
                    "Call the Analyst Agent for market research, competitive analysis, "
                    "and opportunity identification. Use this when you need data-driven insights, "
                    "market sizing, competitor intelligence, or to identify growth opportunities."
                ),
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "task": {
                            "type": "string",
                            "description": "The specific task or question for the Analyst"
                        },
                        "context": {
                            "type": "object",
                            "description": "Additional context (product info, target market, etc.)"
                        }
                    },
                    "required": ["task"]
                }
            },
            {
                "name": "call_growth_hacker_agent",
                "description": (
                    "Call the Growth Hacker Agent for customer acquisition strategies, "
                    "growth experiments, and scaling tactics. Use this when you need growth "
                    "strategies, experiment designs, viral mechanics, or rapid scaling plans."
                ),
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "task": {
                            "type": "string",
                            "description": "The specific task or question for the Growth Hacker"
                        },
                        "context": {
                            "type": "object",
                            "description": "Additional context (current metrics, goals, resources, etc.)"
                        }
                    },
                    "required": ["task"]
                }
            },
            {
                "name": "call_sales_machine_agent",
                "description": (
                    "Call the Sales Machine Agent for sales copy, conversion optimization, "
                    "and offer design. Use this when you need landing pages, email sequences, "
                    "objection handling, or persuasive sales assets."
                ),
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "task": {
                            "type": "string",
                            "description": "The specific task or question for the Sales Machine"
                        },
                        "context": {
                            "type": "object",
                            "description": "Additional context (product, audience, objections, etc.)"
                        }
                    },
                    "required": ["task"]
                }
            },
            {
                "name": "call_system_builder_agent",
                "description": (
                    "Call the System Builder Agent for process documentation, automation "
                    "workflows, and scaling playbooks. Use this when you need SOPs, "
                    "process maps, automation designs, or operational systems."
                ),
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "task": {
                            "type": "string",
                            "description": "The specific task or question for the System Builder"
                        },
                        "context": {
                            "type": "object",
                            "description": "Additional context (current processes, pain points, etc.)"
                        }
                    },
                    "required": ["task"]
                }
            },
            {
                "name": "call_brand_builder_agent",
                "description": (
                    "Call the Brand Builder Agent for content creation, thought leadership, "
                    "and audience engagement. Use this when you need blog posts, social content, "
                    "SEO strategy, or authority-building content."
                ),
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "task": {
                            "type": "string",
                            "description": "The specific task or question for the Brand Builder"
                        },
                        "context": {
                            "type": "object",
                            "description": "Additional context (brand voice, audience, topics, etc.)"
                        }
                    },
                    "required": ["task"]
                }
            },
            {
                "name": "request_human_approval",
                "description": (
                    "Request human approval for high-stakes decisions like financial commitments "
                    ">$1,000, major strategy pivots, or legal matters. Returns approval status."
                ),
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "decision": {
                            "type": "string",
                            "description": "The decision that needs approval"
                        },
                        "rationale": {
                            "type": "string",
                            "description": "Why this decision is recommended"
                        },
                        "risk_level": {
                            "type": "string",
                            "enum": ["low", "medium", "high"],
                            "description": "Risk level of this decision"
                        }
                    },
                    "required": ["decision", "rationale"]
                }
            }
        ]

        return tools + specialist_tools

    async def _handle_tool_use(self, response) -> List[Dict[str, Any]]:
        """
        Override tool handling to intercept specialist agent calls.
        """
        tool_results = []

        for content_block in response.content:
            if content_block.type == "tool_use":
                tool_name = content_block.name
                tool_input = content_block.input

                logger.info(
                    "manager_tool_use",
                    tool_name=tool_name,
                    tool_input=tool_input
                )

                # Check if this is a specialist agent call
                if tool_name.startswith("call_") and tool_name.endswith("_agent"):
                    agent_id = tool_name.replace("call_", "").replace("_agent", "")
                    result = await self._call_specialist_agent(
                        agent_id,
                        tool_input.get("task"),
                        tool_input.get("context")
                    )
                elif tool_name == "request_human_approval":
                    result = await self._request_human_approval(tool_input)
                else:
                    # Standard tool - use parent implementation
                    from src.core.tools import tool_registry
                    result = await tool_registry.execute_tool(tool_name, **tool_input)

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": content_block.id,
                    "content": json.dumps(result, indent=2)
                })

        return tool_results

    async def _call_specialist_agent(
        self,
        agent_id: str,
        task: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Call a specialist agent and return its result."""
        logger.info("calling_specialist_agent", agent_id=agent_id, task=task[:100])

        agent = self.specialist_agents.get(agent_id)
        if not agent:
            return {
                "success": False,
                "error": f"Unknown specialist agent: {agent_id}"
            }

        try:
            result = await agent.run(task=task, context=context)
            logger.info(
                "specialist_agent_completed",
                agent_id=agent_id,
                success=result.get("success")
            )
            return result
        except Exception as e:
            logger.error(
                "specialist_agent_failed",
                agent_id=agent_id,
                error=str(e)
            )
            return {
                "success": False,
                "agent_id": agent_id,
                "error": str(e)
            }

    async def _request_human_approval(self, approval_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Request human approval for a decision.
        In production, this would integrate with a notification system.
        For now, it logs and auto-approves based on settings.
        """
        from src.core.config import settings

        decision = approval_request.get("decision")
        rationale = approval_request.get("rationale")
        risk_level = approval_request.get("risk_level", "medium")

        logger.warning(
            "human_approval_requested",
            decision=decision,
            risk_level=risk_level
        )

        # In production, this would send a notification and wait for approval
        # For now, auto-approve based on settings
        auto_approve = settings.is_development

        if auto_approve:
            logger.info("auto_approving_in_development")
            return {
                "approved": True,
                "message": "Auto-approved in development mode",
                "decision": decision
            }
        else:
            return {
                "approved": False,
                "message": "Human approval required (not implemented yet)",
                "decision": decision,
                "action_required": "Implement human approval workflow"
            }
