"""
Pydantic models for API requests and responses.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class TaskRequest(BaseModel):
    """Request model for creating a new task."""

    task: str = Field(..., description="The task description or user request")
    context: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional context for the task"
    )
    agent: Optional[str] = Field(
        None,
        description="Specific agent to use (manager, analyst, growth_hacker, sales_machine, system_builder, brand_builder). If not specified, manager will route."
    )
    max_iterations: int = Field(
        10,
        description="Maximum number of tool use iterations",
        ge=1,
        le=20
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "task": "Analyze the SaaS productivity tools market and identify top 3 opportunities",
                    "context": {
                        "product": "AI-powered task management tool",
                        "target_audience": "remote teams"
                    }
                }
            ]
        }
    }


class TaskResponse(BaseModel):
    """Response model for task results."""

    task_id: str = Field(..., description="Unique task identifier")
    success: bool = Field(..., description="Whether the task completed successfully")
    agent_id: str = Field(..., description="ID of the agent that processed the task")
    result: Optional[str] = Field(None, description="The task result")
    error: Optional[str] = Field(None, description="Error message if task failed")
    iterations: Optional[int] = Field(None, description="Number of iterations used")
    elapsed_seconds: Optional[float] = Field(None, description="Time taken to complete")
    usage: Optional[Dict[str, int]] = Field(None, description="Token usage statistics")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "task_id": "task_123abc",
                    "success": True,
                    "agent_id": "manager",
                    "result": "## Market Opportunities Analysis\n\n### Opportunity #1: Remote Team Collaboration...",
                    "iterations": 3,
                    "elapsed_seconds": 12.5,
                    "usage": {
                        "input_tokens": 1500,
                        "output_tokens": 2000
                    },
                    "timestamp": "2025-01-15T10:30:00Z"
                }
            ]
        }
    }


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    version: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
