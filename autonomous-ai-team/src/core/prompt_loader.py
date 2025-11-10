"""
Prompt Loader - Loads and validates prompts from markdown files.
Implements caching for performance and token efficiency.
"""

import os
import json
from pathlib import Path
from typing import Dict, Optional, Any
from functools import lru_cache

from .logger import get_logger

logger = get_logger(__name__)


class PromptLoader:
    """
    Loads agent prompts from markdown files with caching and validation.

    Design Principles:
    - KISS: Simple file-based configuration
    - DRY: Prompts defined once, reused many times
    - Token Safety: Cached to avoid re-loading
    - Lean: Minimal dependencies, fast loading
    """

    def __init__(self, config_dir: str = "config"):
        """
        Initialize the prompt loader.

        Args:
            config_dir: Base directory for configuration files
        """
        self.config_dir = Path(config_dir)
        self.prompts_dir = self.config_dir / "prompts"
        self.knowledge_dir = self.config_dir / "knowledge"

        # Validate directories exist
        if not self.prompts_dir.exists():
            raise ValueError(f"Prompts directory not found: {self.prompts_dir}")

        logger.info("prompt_loader_initialized", prompts_dir=str(self.prompts_dir))

    @lru_cache(maxsize=32)
    def load_prompt(self, agent_id: str) -> str:
        """
        Load a prompt for a specific agent.

        Uses LRU cache to avoid re-loading the same prompt multiple times.
        This is critical for token efficiency.

        Args:
            agent_id: Agent identifier (e.g., "analyst", "manager")

        Returns:
            Prompt content as string

        Raises:
            FileNotFoundError: If prompt file doesn't exist
            ValueError: If prompt is empty or invalid
        """
        prompt_file = self.prompts_dir / f"{agent_id}.md"

        if not prompt_file.exists():
            error_msg = f"Prompt file not found: {prompt_file}"
            logger.error("prompt_file_not_found", agent_id=agent_id, file=str(prompt_file))
            raise FileNotFoundError(error_msg)

        try:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                prompt_content = f.read()

            # Validate prompt
            if not prompt_content.strip():
                raise ValueError(f"Prompt file is empty: {prompt_file}")

            # Check minimum length (prompts should be substantial)
            if len(prompt_content) < 100:
                logger.warning(
                    "prompt_suspiciously_short",
                    agent_id=agent_id,
                    length=len(prompt_content)
                )

            logger.info(
                "prompt_loaded",
                agent_id=agent_id,
                length=len(prompt_content),
                cached=True
            )

            return prompt_content

        except Exception as e:
            logger.error("prompt_load_failed", agent_id=agent_id, error=str(e))
            raise

    def load_agent_config(self) -> Dict[str, Any]:
        """
        Load agent configuration from JSON file.

        Returns:
            Dictionary with agent configurations
        """
        config_file = self.config_dir / "agents.json"

        if not config_file.exists():
            logger.warning("agent_config_not_found", using_defaults=True)
            return {}

        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            logger.info(
                "agent_config_loaded",
                agent_count=len(config.get("agents", {}))
            )

            return config

        except Exception as e:
            logger.error("agent_config_load_failed", error=str(e))
            return {}

    def load_tools_config(self) -> Dict[str, Any]:
        """
        Load tools configuration from JSON file.

        Returns:
            Dictionary with tool configurations
        """
        config_file = self.config_dir / "tools.json"

        if not config_file.exists():
            logger.warning("tools_config_not_found", using_defaults=True)
            return {}

        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            logger.info(
                "tools_config_loaded",
                tool_count=len(config.get("tools", {}))
            )

            return config

        except Exception as e:
            logger.error("tools_config_load_failed", error=str(e))
            return {}

    @lru_cache(maxsize=8)
    def load_knowledge(self, knowledge_file: str) -> str:
        """
        Load a knowledge base file.

        Args:
            knowledge_file: Name of knowledge file (e.g., "agent_guidelines.md")

        Returns:
            Knowledge content as string
        """
        file_path = self.knowledge_dir / knowledge_file

        if not file_path.exists():
            logger.warning("knowledge_file_not_found", file=knowledge_file)
            return ""

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            logger.info(
                "knowledge_loaded",
                file=knowledge_file,
                length=len(content)
            )

            return content

        except Exception as e:
            logger.error("knowledge_load_failed", file=knowledge_file, error=str(e))
            return ""

    def get_agent_metadata(self, agent_id: str) -> Dict[str, Any]:
        """
        Get metadata for a specific agent from config.

        Args:
            agent_id: Agent identifier

        Returns:
            Dictionary with agent metadata (model, temperature, etc.)
        """
        config = self.load_agent_config()
        agents = config.get("agents", {})

        if agent_id not in agents:
            logger.warning("agent_metadata_not_found", agent_id=agent_id)
            return {}

        return agents[agent_id]

    def get_tool_metadata(self, tool_name: str) -> Dict[str, Any]:
        """
        Get metadata for a specific tool from config.

        Args:
            tool_name: Tool name

        Returns:
            Dictionary with tool metadata
        """
        config = self.load_tools_config()
        tools = config.get("tools", {})

        if tool_name not in tools:
            logger.warning("tool_metadata_not_found", tool_name=tool_name)
            return {}

        return tools[tool_name]

    def validate_prompt_completeness(self, agent_id: str) -> Dict[str, Any]:
        """
        Validate that a prompt has all required sections.

        Args:
            agent_id: Agent identifier

        Returns:
            Dictionary with validation results
        """
        prompt = self.load_prompt(agent_id)

        required_sections = [
            "# Identity",
            "# Mission",
            "## Methodology",
            "## Output Format"
        ]

        missing_sections = []
        for section in required_sections:
            if section not in prompt:
                missing_sections.append(section)

        is_valid = len(missing_sections) == 0

        result = {
            "agent_id": agent_id,
            "is_valid": is_valid,
            "missing_sections": missing_sections,
            "prompt_length": len(prompt)
        }

        if not is_valid:
            logger.warning(
                "prompt_validation_failed",
                agent_id=agent_id,
                missing_sections=missing_sections
            )

        return result

    def list_available_prompts(self) -> list:
        """
        List all available prompt files.

        Returns:
            List of agent IDs with prompts
        """
        prompt_files = list(self.prompts_dir.glob("*.md"))
        agent_ids = [f.stem for f in prompt_files]

        logger.info("available_prompts_listed", count=len(agent_ids))

        return sorted(agent_ids)

    def clear_cache(self):
        """Clear the LRU cache to force reload of prompts."""
        self.load_prompt.cache_clear()
        self.load_knowledge.cache_clear()
        logger.info("prompt_cache_cleared")

    def get_cache_info(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache hit/miss info
        """
        prompt_cache = self.load_prompt.cache_info()
        knowledge_cache = self.load_knowledge.cache_info()

        return {
            "prompt_cache": {
                "hits": prompt_cache.hits,
                "misses": prompt_cache.misses,
                "size": prompt_cache.currsize,
                "maxsize": prompt_cache.maxsize
            },
            "knowledge_cache": {
                "hits": knowledge_cache.hits,
                "misses": knowledge_cache.misses,
                "size": knowledge_cache.currsize,
                "maxsize": knowledge_cache.maxsize
            }
        }


# Global prompt loader instance
_prompt_loader: Optional[PromptLoader] = None


def get_prompt_loader() -> PromptLoader:
    """
    Get the global prompt loader instance (singleton pattern).

    Returns:
        PromptLoader instance
    """
    global _prompt_loader

    if _prompt_loader is None:
        _prompt_loader = PromptLoader()

    return _prompt_loader


def load_prompt(agent_id: str) -> str:
    """
    Convenience function to load a prompt.

    Args:
        agent_id: Agent identifier

    Returns:
        Prompt content as string
    """
    loader = get_prompt_loader()
    return loader.load_prompt(agent_id)
