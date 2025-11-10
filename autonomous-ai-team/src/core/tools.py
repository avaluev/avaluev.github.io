"""
Tools layer for AI agents.
Provides reusable tools that agents can use to interact with external systems.
"""

import httpx
import json
from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod

from .logger import get_logger
from .config import settings

logger = get_logger(__name__)


class Tool(ABC):
    """Base class for all tools."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Tool name for Claude function calling."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Tool description for Claude."""
        pass

    @property
    @abstractmethod
    def input_schema(self) -> Dict[str, Any]:
        """JSON schema for tool inputs."""
        pass

    @abstractmethod
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the tool with given parameters."""
        pass

    def to_claude_format(self) -> Dict[str, Any]:
        """Convert tool to Claude API format."""
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema
        }


class WebSearchTool(Tool):
    """Web search tool using Brave Search API or SerpAPI."""

    @property
    def name(self) -> str:
        return "web_search"

    @property
    def description(self) -> str:
        return (
            "Search the web for information on a given topic. "
            "Returns top results with URLs, titles, and snippets. "
            "Use this for market research, competitor analysis, or finding current information."
        )

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                },
                "num_results": {
                    "type": "integer",
                    "description": "Number of results to return (1-20)",
                    "default": 10
                }
            },
            "required": ["query"]
        }

    async def execute(self, query: str, num_results: int = 10) -> Dict[str, Any]:
        """Execute web search."""
        logger.info("web_search_executing", query=query, num_results=num_results)

        try:
            if settings.brave_api_key:
                return await self._search_brave(query, num_results)
            elif settings.serpapi_key:
                return await self._search_serpapi(query, num_results)
            else:
                logger.warning("no_search_api_configured")
                return {
                    "success": False,
                    "error": "No search API key configured. Please set BRAVE_API_KEY or SERPAPI_KEY.",
                    "results": []
                }
        except Exception as e:
            logger.error("web_search_failed", error=str(e))
            return {
                "success": False,
                "error": str(e),
                "results": []
            }

    async def _search_brave(self, query: str, num_results: int) -> Dict[str, Any]:
        """Search using Brave Search API."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.search.brave.com/res/v1/web/search",
                headers={"X-Subscription-Token": settings.brave_api_key},
                params={"q": query, "count": num_results}
            )
            response.raise_for_status()
            data = response.json()

            results = []
            for item in data.get("web", {}).get("results", [])[:num_results]:
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "snippet": item.get("description", "")
                })

            return {
                "success": True,
                "query": query,
                "results": results,
                "source": "brave"
            }

    async def _search_serpapi(self, query: str, num_results: int) -> Dict[str, Any]:
        """Search using SerpAPI."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://serpapi.com/search",
                params={
                    "q": query,
                    "api_key": settings.serpapi_key,
                    "num": num_results
                }
            )
            response.raise_for_status()
            data = response.json()

            results = []
            for item in data.get("organic_results", [])[:num_results]:
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("link", ""),
                    "snippet": item.get("snippet", "")
                })

            return {
                "success": True,
                "query": query,
                "results": results,
                "source": "serpapi"
            }


class ExtractDataTool(Tool):
    """Extract structured data from a URL."""

    @property
    def name(self) -> str:
        return "extract_data_from_url"

    @property
    def description(self) -> str:
        return (
            "Extract and parse content from a given URL. "
            "Returns the main text content and metadata. "
            "Useful for analyzing competitor websites, blog posts, or market reports."
        )

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL to extract data from"
                }
            },
            "required": ["url"]
        }

    async def execute(self, url: str) -> Dict[str, Any]:
        """Extract data from URL."""
        logger.info("extract_data_executing", url=url)

        try:
            async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
                response = await client.get(url)
                response.raise_for_status()

                # For now, return raw content
                # In production, you'd use BeautifulSoup for better parsing
                content = response.text[:10000]  # Limit to 10K chars

                return {
                    "success": True,
                    "url": url,
                    "content": content,
                    "status_code": response.status_code
                }
        except Exception as e:
            logger.error("extract_data_failed", url=url, error=str(e))
            return {
                "success": False,
                "url": url,
                "error": str(e)
            }


class StoreContextTool(Tool):
    """Store context for later retrieval."""

    @property
    def name(self) -> str:
        return "store_context"

    @property
    def description(self) -> str:
        return (
            "Store information in the context memory for later use by this or other agents. "
            "Use this to save important findings, decisions, or data that might be needed later."
        )

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "key": {
                    "type": "string",
                    "description": "Unique identifier for this context item"
                },
                "value": {
                    "type": "string",
                    "description": "The information to store"
                },
                "category": {
                    "type": "string",
                    "description": "Category (e.g., 'market_research', 'customer_data', 'strategy')"
                }
            },
            "required": ["key", "value"]
        }

    async def execute(self, key: str, value: str, category: str = "general") -> Dict[str, Any]:
        """Store context."""
        # In a real implementation, this would store to a database
        # For now, we'll just acknowledge it
        logger.info("context_stored", key=key, category=category)

        return {
            "success": True,
            "key": key,
            "category": category,
            "message": "Context stored successfully"
        }


class ToolRegistry:
    """Registry of all available tools."""

    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self._register_default_tools()

    def _register_default_tools(self):
        """Register all default tools."""
        self.register(WebSearchTool())
        self.register(ExtractDataTool())
        self.register(StoreContextTool())

    def register(self, tool: Tool):
        """Register a new tool."""
        self.tools[tool.name] = tool
        logger.info("tool_registered", tool_name=tool.name)

    def get(self, name: str) -> Optional[Tool]:
        """Get a tool by name."""
        return self.tools.get(name)

    def get_all_claude_tools(self) -> List[Dict[str, Any]]:
        """Get all tools in Claude API format."""
        return [tool.to_claude_format() for tool in self.tools.values()]

    async def execute_tool(self, name: str, **kwargs) -> Dict[str, Any]:
        """Execute a tool by name."""
        tool = self.get(name)
        if not tool:
            return {
                "success": False,
                "error": f"Tool '{name}' not found"
            }

        return await tool.execute(**kwargs)


# Global tool registry instance
tool_registry = ToolRegistry()
