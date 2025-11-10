"""
Token Manager - Token counting, budget tracking, and cost optimization.
Implements the Token Safety principle.
"""

import tiktoken
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from collections import defaultdict

from .logger import get_logger
from .config import settings

logger = get_logger(__name__)


@dataclass
class TokenUsage:
    """Track token usage for a single operation."""
    input_tokens: int
    output_tokens: int
    model: str
    timestamp: datetime = field(default_factory=datetime.utcnow)

    @property
    def total_tokens(self) -> int:
        """Total tokens used."""
        return self.input_tokens + self.output_tokens

    def calculate_cost(self, input_cost_per_1k: float, output_cost_per_1k: float) -> float:
        """
        Calculate cost in USD.

        Args:
            input_cost_per_1k: Cost per 1K input tokens
            output_cost_per_1k: Cost per 1K output tokens

        Returns:
            Total cost in USD
        """
        input_cost = (self.input_tokens / 1000) * input_cost_per_1k
        output_cost = (self.output_tokens / 1000) * output_cost_per_1k
        return input_cost + output_cost


class TokenManager:
    """
    Manages token counting, budget tracking, and cost optimization.

    Design Principles:
    - Token Safety: Track every token, prevent budget overruns
    - Lean: Minimal overhead, fast operations
    - DRY: Centralized token logic
    """

    # Claude Sonnet 4.5 pricing (per 1K tokens)
    DEFAULT_INPUT_COST = 0.003
    DEFAULT_OUTPUT_COST = 0.015

    def __init__(self, daily_budget: float = None):
        """
        Initialize token manager.

        Args:
            daily_budget: Daily budget in USD (default from settings)
        """
        self.daily_budget = daily_budget or settings.max_cost_per_day

        # Track usage by agent and date
        self.usage_by_agent: Dict[str, list] = defaultdict(list)
        self.usage_by_date: Dict[str, list] = defaultdict(list)

        # Pricing for different models
        self.model_pricing = {
            "claude-sonnet-4-5": {
                "input": self.DEFAULT_INPUT_COST,
                "output": self.DEFAULT_OUTPUT_COST
            },
            "claude-sonnet-3-5": {
                "input": 0.003,
                "output": 0.015
            },
            "claude-haiku": {
                "input": 0.00025,
                "output": 0.00125
            }
        }

        # Initialize tokenizer (for estimation before API calls)
        try:
            self.tokenizer = tiktoken.encoding_for_model("gpt-4")  # Similar to Claude
        except Exception as e:
            logger.warning("tokenizer_init_failed", error=str(e))
            self.tokenizer = None

        logger.info("token_manager_initialized", daily_budget=self.daily_budget)

    def estimate_tokens(self, text: str) -> int:
        """
        Estimate token count for text.

        Uses tiktoken for estimation. Not exact for Claude but close enough
        for budget management.

        Args:
            text: Text to estimate

        Returns:
            Estimated token count
        """
        if not self.tokenizer:
            # Fallback: rough estimate (1 token ≈ 4 characters)
            return len(text) // 4

        try:
            return len(self.tokenizer.encode(text))
        except Exception as e:
            logger.error("token_estimation_failed", error=str(e))
            return len(text) // 4

    def record_usage(
        self,
        agent_id: str,
        input_tokens: int,
        output_tokens: int,
        model: str = "claude-sonnet-4-5"
    ) -> TokenUsage:
        """
        Record token usage for an agent.

        Args:
            agent_id: Agent identifier
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            model: Model used

        Returns:
            TokenUsage object with cost calculation
        """
        usage = TokenUsage(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            model=model
        )

        # Get pricing for model
        pricing = self.model_pricing.get(model, {
            "input": self.DEFAULT_INPUT_COST,
            "output": self.DEFAULT_OUTPUT_COST
        })

        cost = usage.calculate_cost(pricing["input"], pricing["output"])

        # Store usage
        today = datetime.utcnow().date().isoformat()
        self.usage_by_agent[agent_id].append(usage)
        self.usage_by_date[today].append(usage)

        logger.info(
            "token_usage_recorded",
            agent_id=agent_id,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=usage.total_tokens,
            cost_usd=round(cost, 4)
        )

        return usage

    def get_daily_usage(self, date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get token usage for a specific date.

        Args:
            date: Date in YYYY-MM-DD format (default: today)

        Returns:
            Dictionary with usage statistics
        """
        if date is None:
            date = datetime.utcnow().date().isoformat()

        usages = self.usage_by_date.get(date, [])

        if not usages:
            return {
                "date": date,
                "total_tokens": 0,
                "input_tokens": 0,
                "output_tokens": 0,
                "total_cost_usd": 0.0,
                "call_count": 0
            }

        total_input = sum(u.input_tokens for u in usages)
        total_output = sum(u.output_tokens for u in usages)

        # Calculate cost
        total_cost = 0.0
        for usage in usages:
            pricing = self.model_pricing.get(usage.model, {
                "input": self.DEFAULT_INPUT_COST,
                "output": self.DEFAULT_OUTPUT_COST
            })
            total_cost += usage.calculate_cost(pricing["input"], pricing["output"])

        return {
            "date": date,
            "total_tokens": total_input + total_output,
            "input_tokens": total_input,
            "output_tokens": total_output,
            "total_cost_usd": round(total_cost, 2),
            "call_count": len(usages),
            "budget_remaining_usd": round(self.daily_budget - total_cost, 2),
            "budget_used_percentage": round((total_cost / self.daily_budget) * 100, 1)
        }

    def get_agent_usage(self, agent_id: str) -> Dict[str, Any]:
        """
        Get usage statistics for a specific agent.

        Args:
            agent_id: Agent identifier

        Returns:
            Dictionary with usage statistics
        """
        usages = self.usage_by_agent.get(agent_id, [])

        if not usages:
            return {
                "agent_id": agent_id,
                "total_tokens": 0,
                "total_cost_usd": 0.0,
                "call_count": 0
            }

        total_input = sum(u.input_tokens for u in usages)
        total_output = sum(u.output_tokens for u in usages)

        total_cost = 0.0
        for usage in usages:
            pricing = self.model_pricing.get(usage.model, {
                "input": self.DEFAULT_INPUT_COST,
                "output": self.DEFAULT_OUTPUT_COST
            })
            total_cost += usage.calculate_cost(pricing["input"], pricing["output"])

        return {
            "agent_id": agent_id,
            "total_tokens": total_input + total_output,
            "input_tokens": total_input,
            "output_tokens": total_output,
            "total_cost_usd": round(total_cost, 2),
            "call_count": len(usages),
            "avg_tokens_per_call": round((total_input + total_output) / len(usages), 0)
        }

    def check_budget_available(self) -> bool:
        """
        Check if we're within daily budget.

        Returns:
            True if budget is available, False if exceeded
        """
        usage = self.get_daily_usage()
        remaining = usage["budget_remaining_usd"]

        if remaining < 0:
            logger.warning(
                "daily_budget_exceeded",
                spent=usage["total_cost_usd"],
                budget=self.daily_budget,
                overage=abs(remaining)
            )
            return False

        # Warning at 80% budget used
        if usage["budget_used_percentage"] >= 80:
            logger.warning(
                "budget_warning",
                percentage=usage["budget_used_percentage"],
                remaining=remaining
            )

        return True

    def estimate_call_cost(
        self,
        input_text: str,
        expected_output_tokens: int = 1000,
        model: str = "claude-sonnet-4-5"
    ) -> float:
        """
        Estimate cost of an API call before making it.

        Args:
            input_text: Input text to send
            expected_output_tokens: Expected output tokens
            model: Model to use

        Returns:
            Estimated cost in USD
        """
        input_tokens = self.estimate_tokens(input_text)

        pricing = self.model_pricing.get(model, {
            "input": self.DEFAULT_INPUT_COST,
            "output": self.DEFAULT_OUTPUT_COST
        })

        input_cost = (input_tokens / 1000) * pricing["input"]
        output_cost = (expected_output_tokens / 1000) * pricing["output"]

        return input_cost + output_cost

    def should_allow_call(
        self,
        input_text: str,
        expected_output_tokens: int = 1000,
        model: str = "claude-sonnet-4-5"
    ) -> tuple[bool, str]:
        """
        Determine if an API call should be allowed based on budget.

        Args:
            input_text: Input text
            expected_output_tokens: Expected output tokens
            model: Model to use

        Returns:
            Tuple of (should_allow, reason)
        """
        # Check daily budget
        if not self.check_budget_available():
            return False, "Daily budget exceeded"

        # Estimate cost
        estimated_cost = self.estimate_call_cost(
            input_text,
            expected_output_tokens,
            model
        )

        # Check if this call would exceed remaining budget
        usage = self.get_daily_usage()
        remaining = usage["budget_remaining_usd"]

        if estimated_cost > remaining:
            return False, f"Call would exceed remaining budget (${remaining:.2f})"

        return True, "Budget available"

    def get_cost_optimization_suggestions(self) -> list:
        """
        Get suggestions for optimizing costs.

        Returns:
            List of optimization suggestions
        """
        suggestions = []

        # Analyze agent usage
        for agent_id in self.usage_by_agent:
            usage = self.get_agent_usage(agent_id)

            # High token usage per call
            if usage["avg_tokens_per_call"] > 5000:
                suggestions.append({
                    "agent": agent_id,
                    "issue": "high_tokens_per_call",
                    "recommendation": "Consider breaking down tasks into smaller chunks",
                    "avg_tokens": usage["avg_tokens_per_call"]
                })

        # Check daily spending
        daily_usage = self.get_daily_usage()
        if daily_usage["budget_used_percentage"] > 50:
            suggestions.append({
                "agent": "system",
                "issue": "high_daily_spend",
                "recommendation": "Review agent prompts for efficiency, consider caching",
                "percentage": daily_usage["budget_used_percentage"]
            })

        return suggestions

    def get_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive usage summary.

        Returns:
            Dictionary with all usage stats
        """
        daily_usage = self.get_daily_usage()

        agent_summaries = {}
        for agent_id in self.usage_by_agent:
            agent_summaries[agent_id] = self.get_agent_usage(agent_id)

        return {
            "daily_usage": daily_usage,
            "agent_usage": agent_summaries,
            "optimization_suggestions": self.get_cost_optimization_suggestions()
        }


# Global token manager instance
_token_manager: Optional[TokenManager] = None


def get_token_manager() -> TokenManager:
    """
    Get the global token manager instance (singleton pattern).

    Returns:
        TokenManager instance
    """
    global _token_manager

    if _token_manager is None:
        _token_manager = TokenManager()

    return _token_manager
