"""
Model Router - Intelligently route tasks to appropriate models (Sonnet vs Haiku).
Implements Phase 2 cost optimization through smart model selection.
"""

from enum import Enum
from typing import Dict, Any, Optional
from dataclasses import dataclass

from .logger import get_logger
from .config import settings

logger = get_logger(__name__)


class ModelTier(Enum):
    """Model tiers for different complexity levels."""
    HAIKU = "claude-3-5-haiku-20241022"  # Fast, cheap
    SONNET = "claude-sonnet-4-5"  # Balanced
    OPUS = "claude-3-opus-20240229"  # Powerful, expensive


@dataclass
class ModelPricing:
    """Pricing for a model."""
    model_id: str
    input_cost_per_1m: float
    output_cost_per_1m: float
    max_tokens: int
    context_window: int


# Model pricing database
MODEL_PRICING = {
    ModelTier.HAIKU: ModelPricing(
        model_id="claude-3-5-haiku-20241022",
        input_cost_per_1m=0.25,
        output_cost_per_1m=1.25,
        max_tokens=8192,
        context_window=200000
    ),
    ModelTier.SONNET: ModelPricing(
        model_id="claude-sonnet-4-5",
        input_cost_per_1m=3.00,
        output_cost_per_1m=15.00,
        max_tokens=8192,
        context_window=200000
    ),
    ModelTier.OPUS: ModelPricing(
        model_id="claude-3-opus-20240229",
        input_cost_per_1m=15.00,
        output_cost_per_1m=75.00,
        max_tokens=4096,
        context_window=200000
    )
}


class TaskComplexity(Enum):
    """Task complexity levels."""
    SIMPLE = "simple"  # Classification, extraction, summarization
    MEDIUM = "medium"  # Analysis, generation, reasoning
    COMPLEX = "complex"  # Multi-step reasoning, creative work


class ModelRouter:
    """
    Routes tasks to appropriate models based on complexity.

    Design Principles:
    - Lean: Use cheapest model that can do the job
    - Token Safety: Track costs per model
    - KISS: Simple rules-based routing
    """

    def __init__(self):
        """Initialize the model router."""
        self.routing_rules = self._init_routing_rules()
        logger.info("model_router_initialized")

    def _init_routing_rules(self) -> Dict[str, Any]:
        """Initialize routing rules."""
        return {
            # Simple tasks → Haiku (20x cheaper)
            TaskComplexity.SIMPLE: {
                "model": ModelTier.HAIKU,
                "max_tokens": 2048,
                "temperature": 0.3,
                "use_cases": [
                    "classification",
                    "extraction",
                    "summarization",
                    "validation",
                    "formatting",
                    "routing"
                ]
            },

            # Medium tasks → Sonnet (balanced)
            TaskComplexity.MEDIUM: {
                "model": ModelTier.SONNET,
                "max_tokens": 4096,
                "temperature": 0.7,
                "use_cases": [
                    "analysis",
                    "generation",
                    "reasoning",
                    "planning",
                    "research"
                ]
            },

            # Complex tasks → Sonnet (or Opus if needed)
            TaskComplexity.COMPLEX: {
                "model": ModelTier.SONNET,  # Still Sonnet, not Opus (cost)
                "max_tokens": 8192,
                "temperature": 0.8,
                "use_cases": [
                    "multi_step_reasoning",
                    "creative_work",
                    "complex_analysis",
                    "strategic_planning",
                    "orchestration"
                ]
            }
        }

    def route_task(
        self,
        task_description: str,
        agent_id: str,
        explicit_complexity: Optional[TaskComplexity] = None
    ) -> Dict[str, Any]:
        """
        Route a task to the appropriate model.

        Args:
            task_description: Description of the task
            agent_id: Agent requesting routing
            explicit_complexity: Override auto-detection

        Returns:
            Dict with model, max_tokens, temperature
        """
        # Determine complexity
        if explicit_complexity:
            complexity = explicit_complexity
        else:
            complexity = self._detect_complexity(task_description, agent_id)

        # Get routing config
        config = self.routing_rules[complexity]
        model_tier = config["model"]
        pricing = MODEL_PRICING[model_tier]

        logger.info(
            "task_routed",
            agent_id=agent_id,
            complexity=complexity.value,
            model=pricing.model_id,
            estimated_cost_savings=self._calculate_savings(complexity)
        )

        return {
            "model": pricing.model_id,
            "max_tokens": config["max_tokens"],
            "temperature": config["temperature"],
            "pricing": {
                "input_per_1m": pricing.input_cost_per_1m,
                "output_per_1m": pricing.output_cost_per_1m
            }
        }

    def _detect_complexity(
        self,
        task_description: str,
        agent_id: str
    ) -> TaskComplexity:
        """
        Detect task complexity from description.

        Args:
            task_description: The task to analyze
            agent_id: Agent ID (some agents always need Sonnet)

        Returns:
            TaskComplexity level
        """
        task_lower = task_description.lower()

        # Agents that always use Sonnet (creative/strategic work)
        sonnet_agents = ["sales_machine", "brand_builder", "growth_hacker"]
        if agent_id in sonnet_agents:
            return TaskComplexity.COMPLEX

        # Simple task indicators
        simple_indicators = [
            "classify",
            "extract",
            "summarize",
            "validate",
            "format",
            "parse",
            "check if",
            "is this",
            "yes or no",
            "list the",
            "count the"
        ]

        if any(indicator in task_lower for indicator in simple_indicators):
            return TaskComplexity.SIMPLE

        # Complex task indicators
        complex_indicators = [
            "analyze and recommend",
            "create a strategy",
            "design a",
            "write copy",
            "generate content",
            "plan a",
            "come up with",
            "brainstorm",
            "multiple steps",
            "comprehensive"
        ]

        if any(indicator in task_lower for indicator in complex_indicators):
            return TaskComplexity.COMPLEX

        # Default to medium
        return TaskComplexity.MEDIUM

    def _calculate_savings(self, complexity: TaskComplexity) -> float:
        """
        Calculate cost savings vs always using Sonnet.

        Args:
            complexity: Task complexity

        Returns:
            Percentage savings (0-100)
        """
        if complexity == TaskComplexity.SIMPLE:
            # Haiku is ~20x cheaper than Sonnet
            haiku = MODEL_PRICING[ModelTier.HAIKU]
            sonnet = MODEL_PRICING[ModelTier.SONNET]

            avg_haiku_cost = (haiku.input_cost_per_1m + haiku.output_cost_per_1m) / 2
            avg_sonnet_cost = (sonnet.input_cost_per_1m + sonnet.output_cost_per_1m) / 2

            savings = ((avg_sonnet_cost - avg_haiku_cost) / avg_sonnet_cost) * 100
            return round(savings, 1)

        return 0.0

    def get_model_for_agent(self, agent_id: str, task_type: str = "default") -> str:
        """
        Get recommended model for a specific agent and task type.

        Args:
            agent_id: Agent identifier
            task_type: Type of task (e.g., "research", "generation")

        Returns:
            Model ID string
        """
        # Agent-specific routing
        agent_routing = {
            "manager": {
                "routing": ModelTier.HAIKU,  # Just routing decisions
                "orchestration": ModelTier.SONNET  # Complex coordination
            },
            "analyst": {
                "research": ModelTier.SONNET,  # Needs good reasoning
                "summarization": ModelTier.HAIKU  # Simple task
            },
            "growth_hacker": {
                "default": ModelTier.SONNET  # Creative work
            },
            "sales_machine": {
                "default": ModelTier.SONNET  # Copywriting needs creativity
            },
            "system_builder": {
                "documentation": ModelTier.SONNET,
                "validation": ModelTier.HAIKU
            },
            "brand_builder": {
                "default": ModelTier.SONNET  # Content creation
            }
        }

        agent_config = agent_routing.get(agent_id, {})
        model_tier = agent_config.get(task_type, agent_config.get("default", ModelTier.SONNET))

        return MODEL_PRICING[model_tier].model_id

    def estimate_cost(
        self,
        input_tokens: int,
        output_tokens: int,
        model_tier: ModelTier
    ) -> float:
        """
        Estimate cost for a task.

        Args:
            input_tokens: Expected input tokens
            output_tokens: Expected output tokens
            model_tier: Model tier to use

        Returns:
            Estimated cost in USD
        """
        pricing = MODEL_PRICING[model_tier]

        input_cost = (input_tokens / 1_000_000) * pricing.input_cost_per_1m
        output_cost = (output_tokens / 1_000_000) * pricing.output_cost_per_1m

        return input_cost + output_cost

    def get_pricing_info(self) -> Dict[str, Any]:
        """
        Get pricing information for all models.

        Returns:
            Dict with model pricing details
        """
        return {
            tier.name.lower(): {
                "model_id": pricing.model_id,
                "input_per_1m_tokens": pricing.input_cost_per_1m,
                "output_per_1m_tokens": pricing.output_cost_per_1m,
                "max_tokens": pricing.max_tokens,
                "context_window": pricing.context_window,
                "use_case": self.routing_rules.get(
                    TaskComplexity.SIMPLE if tier == ModelTier.HAIKU else TaskComplexity.COMPLEX,
                    {}
                ).get("use_cases", [])
            }
            for tier, pricing in MODEL_PRICING.items()
        }


# Global model router instance
_model_router: Optional[ModelRouter] = None


def get_model_router() -> ModelRouter:
    """
    Get the global model router instance (singleton pattern).

    Returns:
        ModelRouter instance
    """
    global _model_router

    if _model_router is None:
        _model_router = ModelRouter()

    return _model_router
