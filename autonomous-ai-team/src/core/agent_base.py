"""
Base Agent class for the Autonomous AI Team system.
All agents (Manager and Specialists) inherit from this base class.
"""

import anthropic
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
from datetime import datetime

from .config import settings
from .logger import get_logger
from .tools import tool_registry

logger = get_logger(__name__)


class AgentBase(ABC):
    """Base class for all AI agents."""

    def __init__(
        self,
        agent_id: str,
        model: str = None,
        temperature: float = None,
        max_tokens: int = None
    ):
        """
        Initialize an agent.

        Args:
            agent_id: Unique identifier for this agent
            model: Claude model to use (defaults to settings.default_model)
            temperature: Sampling temperature (defaults to settings.temperature)
            max_tokens: Max tokens to generate (defaults to settings.max_tokens)
        """
        self.agent_id = agent_id
        self.model = model or settings.default_model
        self.temperature = temperature or settings.temperature
        self.max_tokens = max_tokens or settings.max_tokens

        # Initialize Claude client
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

        # Conversation history
        self.conversation_history: List[Dict[str, Any]] = []

        logger.info("agent_initialized", agent_id=agent_id, model=self.model)

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """System prompt that defines the agent's role and behavior."""
        pass

    @property
    def available_tools(self) -> List[Dict[str, Any]]:
        """Tools available to this agent. Override in subclasses to customize."""
        return tool_registry.get_all_claude_tools()

    async def run(
        self,
        task: str,
        context: Optional[Dict[str, Any]] = None,
        max_iterations: int = 10
    ) -> Dict[str, Any]:
        """
        Run the agent on a task.

        Args:
            task: The task description or user message
            context: Additional context for the task
            max_iterations: Maximum number of tool use iterations

        Returns:
            Dict containing the result and metadata
        """
        logger.info(
            "agent_run_started",
            agent_id=self.agent_id,
            task=task[:100],
            has_context=bool(context)
        )

        start_time = datetime.utcnow()

        try:
            # Build initial message
            messages = [{"role": "user", "content": self._build_user_message(task, context)}]

            iteration = 0
            while iteration < max_iterations:
                iteration += 1
                logger.debug("agent_iteration", iteration=iteration, agent_id=self.agent_id)

                # Call Claude
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    system=self.system_prompt,
                    tools=self.available_tools,
                    messages=messages
                )

                # Store in conversation history
                self.conversation_history.append({
                    "role": "assistant",
                    "content": response.content,
                    "stop_reason": response.stop_reason,
                    "timestamp": datetime.utcnow().isoformat()
                })

                # Check stop reason
                if response.stop_reason == "end_turn":
                    # Agent is done
                    result = self._extract_result(response)
                    elapsed = (datetime.utcnow() - start_time).total_seconds()

                    logger.info(
                        "agent_run_completed",
                        agent_id=self.agent_id,
                        iterations=iteration,
                        elapsed_seconds=elapsed
                    )

                    return {
                        "success": True,
                        "agent_id": self.agent_id,
                        "result": result,
                        "iterations": iteration,
                        "elapsed_seconds": elapsed,
                        "usage": {
                            "input_tokens": response.usage.input_tokens,
                            "output_tokens": response.usage.output_tokens
                        }
                    }

                elif response.stop_reason == "tool_use":
                    # Agent wants to use tools
                    tool_results = await self._handle_tool_use(response)

                    # Add assistant message and tool results to conversation
                    messages.append({
                        "role": "assistant",
                        "content": response.content
                    })
                    messages.append({
                        "role": "user",
                        "content": tool_results
                    })

                else:
                    # Unexpected stop reason
                    logger.warning(
                        "unexpected_stop_reason",
                        stop_reason=response.stop_reason,
                        agent_id=self.agent_id
                    )
                    break

            # Max iterations reached
            logger.warning("max_iterations_reached", agent_id=self.agent_id)
            return {
                "success": False,
                "error": "Max iterations reached",
                "agent_id": self.agent_id,
                "iterations": iteration
            }

        except Exception as e:
            logger.error("agent_run_failed", agent_id=self.agent_id, error=str(e))
            return {
                "success": False,
                "error": str(e),
                "agent_id": self.agent_id
            }

    def _build_user_message(self, task: str, context: Optional[Dict[str, Any]]) -> str:
        """Build the initial user message with task and context."""
        message = task

        if context:
            message += "\n\n**Additional Context:**\n"
            for key, value in context.items():
                message += f"- **{key}**: {value}\n"

        return message

    async def _handle_tool_use(self, response: anthropic.types.Message) -> List[Dict[str, Any]]:
        """Handle tool use requests from Claude."""
        tool_results = []

        for content_block in response.content:
            if content_block.type == "tool_use":
                tool_name = content_block.name
                tool_input = content_block.input

                logger.info(
                    "tool_use_requested",
                    agent_id=self.agent_id,
                    tool_name=tool_name,
                    tool_input=tool_input
                )

                # Execute the tool
                result = await tool_registry.execute_tool(tool_name, **tool_input)

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": content_block.id,
                    "content": str(result)
                })

                logger.info(
                    "tool_use_completed",
                    agent_id=self.agent_id,
                    tool_name=tool_name,
                    success=result.get("success", False)
                )

        return tool_results

    def _extract_result(self, response: anthropic.types.Message) -> str:
        """Extract the text result from Claude's response."""
        result_parts = []

        for content_block in response.content:
            if content_block.type == "text":
                result_parts.append(content_block.text)

        return "\n".join(result_parts)

    def reset_conversation(self):
        """Reset the conversation history."""
        self.conversation_history = []
        logger.info("conversation_reset", agent_id=self.agent_id)


class SpecialistAgent(AgentBase):
    """Base class for specialist agents."""

    def __init__(
        self,
        agent_id: str,
        specialty: str,
        model: str = None,
        temperature: float = None,
        max_tokens: int = None
    ):
        """
        Initialize a specialist agent.

        Args:
            agent_id: Unique identifier
            specialty: Agent's domain of expertise
            model: Claude model to use
            temperature: Sampling temperature
            max_tokens: Max tokens to generate
        """
        super().__init__(agent_id, model, temperature, max_tokens)
        self.specialty = specialty

        logger.info(
            "specialist_agent_initialized",
            agent_id=agent_id,
            specialty=specialty
        )
