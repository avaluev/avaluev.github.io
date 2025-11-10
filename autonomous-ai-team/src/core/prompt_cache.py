"""
Prompt Caching - Implement Anthropic's prompt caching for 90% cost reduction.
Phase 2 feature for major cost optimization.
"""

import anthropic
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

from .logger import get_logger
from .config import settings

logger = get_logger(__name__)


class PromptCache:
    """
    Manages Anthropic's prompt caching for cost optimization.

    Prompt caching allows you to cache parts of your prompt that don't change
    between requests, reducing costs by up to 90% and improving latency.

    Key Benefits:
    - 90% cost reduction on cached prompt tokens
    - 10x faster processing of cached content
    - 5-minute cache lifetime (enough for most workflows)

    Pricing:
    - Write (cache miss): $3.75 per 1M tokens (25% premium)
    - Read (cache hit): $0.30 per 1M tokens (90% discount!)
    """

    def __init__(self):
        """Initialize prompt cache manager."""
        self.cache_stats = {
            "hits": 0,
            "misses": 0,
            "savings_usd": 0.0
        }
        logger.info("prompt_cache_initialized")

    def create_cached_system_prompt(
        self,
        system_prompt: str,
        cache_enabled: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Create a system prompt with caching enabled.

        Args:
            system_prompt: The system prompt text
            cache_enabled: Whether to enable caching

        Returns:
            List of system content blocks with cache control
        """
        if not cache_enabled:
            return [{"type": "text", "text": system_prompt}]

        # Split prompt into cacheable and non-cacheable parts
        # Cache everything if prompt is long enough (>1024 tokens recommended)
        return [
            {
                "type": "text",
                "text": system_prompt,
                "cache_control": {"type": "ephemeral"}  # Cache for 5 minutes
            }
        ]

    def create_cached_messages(
        self,
        messages: List[Dict[str, Any]],
        cache_recent_turns: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Create messages with caching for conversation history.

        Caches recent conversation turns to speed up multi-turn interactions.

        Args:
            messages: List of message dicts
            cache_recent_turns: Number of recent turns to cache

        Returns:
            Messages with cache control markers
        """
        if len(messages) <= 1:
            return messages

        # Add cache control to recent assistant messages
        cached_messages = messages.copy()

        # Cache the last N conversation turns
        for i in range(len(cached_messages) - cache_recent_turns, len(cached_messages)):
            if i >= 0 and cached_messages[i]["role"] == "assistant":
                # Convert content to list format for cache control
                content = cached_messages[i]["content"]
                if isinstance(content, str):
                    cached_messages[i]["content"] = [
                        {
                            "type": "text",
                            "text": content,
                            "cache_control": {"type": "ephemeral"}
                        }
                    ]

        return cached_messages

    def create_message_with_caching(
        self,
        client: anthropic.Anthropic,
        model: str,
        system: str,
        messages: List[Dict[str, Any]],
        max_tokens: int = 4096,
        temperature: float = 0.7,
        tools: Optional[List[Dict[str, Any]]] = None,
        cache_system: bool = True,
        cache_tools: bool = True
    ) -> anthropic.types.Message:
        """
        Create a message with prompt caching enabled.

        Args:
            client: Anthropic client
            model: Model ID
            system: System prompt
            messages: Conversation messages
            max_tokens: Max tokens to generate
            temperature: Sampling temperature
            tools: Available tools
            cache_system: Whether to cache system prompt
            cache_tools: Whether to cache tools

        Returns:
            Message response with cache usage info
        """
        # Prepare cached system prompt
        if cache_system:
            system_blocks = self.create_cached_system_prompt(system)
        else:
            system_blocks = [{"type": "text", "text": system}]

        # Prepare cached tools
        if tools and cache_tools and len(tools) > 0:
            # Mark tools for caching (they rarely change)
            tools_with_cache = tools.copy()
            # Cache the last tool definition (Anthropic caches from end)
            if len(tools_with_cache) > 0:
                tools_with_cache[-1]["cache_control"] = {"type": "ephemeral"}
        else:
            tools_with_cache = tools

        # Create request
        request_params = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "system": system_blocks,
            "messages": messages
        }

        if tools_with_cache:
            request_params["tools"] = tools_with_cache

        # Make API call
        response = client.messages.create(**request_params)

        # Track cache usage
        self._record_cache_usage(response)

        return response

    def _record_cache_usage(self, response: anthropic.types.Message):
        """
        Record cache hit/miss statistics.

        Args:
            response: API response with usage info
        """
        usage = response.usage

        # Check for cache usage (Anthropic includes cache stats in usage)
        cache_creation_tokens = getattr(usage, "cache_creation_input_tokens", 0)
        cache_read_tokens = getattr(usage, "cache_read_input_tokens", 0)

        if cache_read_tokens > 0:
            self.cache_stats["hits"] += 1

            # Calculate savings
            # Cache read: $0.30/1M tokens
            # Regular read: $3.00/1M tokens
            # Savings: $2.70/1M tokens (90%)
            savings = (cache_read_tokens / 1_000_000) * 2.70
            self.cache_stats["savings_usd"] += savings

            logger.info(
                "cache_hit",
                cache_read_tokens=cache_read_tokens,
                savings_usd=round(savings, 4)
            )

        if cache_creation_tokens > 0:
            self.cache_stats["misses"] += 1

            logger.info(
                "cache_miss",
                cache_creation_tokens=cache_creation_tokens
            )

    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache performance statistics.

        Returns:
            Dict with cache hit rate and savings
        """
        total_requests = self.cache_stats["hits"] + self.cache_stats["misses"]

        if total_requests == 0:
            hit_rate = 0.0
        else:
            hit_rate = (self.cache_stats["hits"] / total_requests) * 100

        return {
            "total_requests": total_requests,
            "cache_hits": self.cache_stats["hits"],
            "cache_misses": self.cache_stats["misses"],
            "hit_rate_percentage": round(hit_rate, 1),
            "total_savings_usd": round(self.cache_stats["savings_usd"], 2),
            "estimated_monthly_savings": round(self.cache_stats["savings_usd"] * 30, 2)
        }

    def reset_stats(self):
        """Reset cache statistics."""
        self.cache_stats = {
            "hits": 0,
            "misses": 0,
            "savings_usd": 0.0
        }
        logger.info("cache_stats_reset")


class CacheStrategy:
    """
    Strategies for what to cache in different scenarios.

    Design Principles:
    - Lean: Cache what doesn't change
    - Token Safety: Track savings
    - KISS: Simple rules
    """

    @staticmethod
    def should_cache_system_prompt(prompt_length: int) -> bool:
        """
        Determine if system prompt should be cached.

        Anthropic recommends caching prompts >1024 tokens.

        Args:
            prompt_length: Length in tokens

        Returns:
            True if should cache
        """
        # Cache if prompt is substantial (saves more than costs)
        MIN_TOKENS_TO_CACHE = 1024
        return prompt_length >= MIN_TOKENS_TO_CACHE

    @staticmethod
    def should_cache_tools(num_tools: int) -> bool:
        """
        Determine if tools should be cached.

        Args:
            num_tools: Number of tools

        Returns:
            True if should cache
        """
        # Cache if more than 3 tools (they're substantial)
        return num_tools > 3

    @staticmethod
    def should_cache_conversation_history(num_turns: int) -> bool:
        """
        Determine if conversation history should be cached.

        Args:
            num_turns: Number of conversation turns

        Returns:
            True if should cache
        """
        # Cache if conversation is multi-turn
        return num_turns > 2

    @staticmethod
    def get_optimal_cache_points(
        system_prompt_tokens: int,
        num_tools: int,
        conversation_turns: int
    ) -> Dict[str, bool]:
        """
        Get optimal caching strategy for a request.

        Args:
            system_prompt_tokens: System prompt length
            num_tools: Number of tools
            conversation_turns: Number of turns

        Returns:
            Dict with cache recommendations
        """
        return {
            "cache_system": CacheStrategy.should_cache_system_prompt(system_prompt_tokens),
            "cache_tools": CacheStrategy.should_cache_tools(num_tools),
            "cache_history": CacheStrategy.should_cache_conversation_history(conversation_turns)
        }


# Global prompt cache instance
_prompt_cache: Optional[PromptCache] = None


def get_prompt_cache() -> PromptCache:
    """
    Get the global prompt cache instance (singleton pattern).

    Returns:
        PromptCache instance
    """
    global _prompt_cache

    if _prompt_cache is None:
        _prompt_cache = PromptCache()

    return _prompt_cache


# Example usage
"""
# Using prompt cache with an agent

from src.core.prompt_cache import get_prompt_cache

prompt_cache = get_prompt_cache()

# Create message with caching
response = prompt_cache.create_message_with_caching(
    client=anthropic_client,
    model="claude-sonnet-4-5",
    system=LONG_SYSTEM_PROMPT,  # Will be cached
    messages=[{"role": "user", "content": "Quick question"}],
    tools=available_tools,  # Will be cached
    cache_system=True,
    cache_tools=True
)

# First call: Normal cost
# Next 100 calls in 5 minutes: 90% discount on cached parts!

# Check savings
stats = prompt_cache.get_cache_stats()
print(f"Savings: ${stats['total_savings_usd']}")
print(f"Hit rate: {stats['hit_rate_percentage']}%")
"""
