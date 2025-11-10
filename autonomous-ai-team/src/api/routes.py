"""
API routes for the Autonomous AI Team system.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uuid
from datetime import datetime

from src.api.models import TaskRequest, TaskResponse, HealthResponse
from src.agents.manager import ManagerAgent
from src.agents.analyst import AnalystAgent
from src.agents.growth_hacker import GrowthHackerAgent
from src.agents.sales_machine import SalesMachineAgent
from src.agents.system_builder import SystemBuilderAgent
from src.agents.brand_builder import BrandBuilderAgent
from src.core.logger import get_logger, setup_logging
from src.core.config import settings

# Setup logging
setup_logging()
logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Autonomous AI Team API",
    description="Multi-agent AI system for accelerating business growth",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents (singleton pattern)
_manager_agent = None
_specialist_agents = {}


def get_manager_agent() -> ManagerAgent:
    """Get or create the manager agent singleton."""
    global _manager_agent
    if _manager_agent is None:
        _manager_agent = ManagerAgent()
        logger.info("manager_agent_singleton_created")
    return _manager_agent


def get_specialist_agent(agent_type: str):
    """Get or create a specialist agent singleton."""
    global _specialist_agents

    if agent_type not in _specialist_agents:
        agent_classes = {
            "analyst": AnalystAgent,
            "growth_hacker": GrowthHackerAgent,
            "sales_machine": SalesMachineAgent,
            "system_builder": SystemBuilderAgent,
            "brand_builder": BrandBuilderAgent
        }

        agent_class = agent_classes.get(agent_type)
        if not agent_class:
            raise ValueError(f"Unknown agent type: {agent_type}")

        _specialist_agents[agent_type] = agent_class()
        logger.info("specialist_agent_singleton_created", agent_type=agent_type)

    return _specialist_agents[agent_type]


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - health check."""
    return HealthResponse(
        status="healthy",
        version="0.1.0"
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="0.1.0"
    )


@app.post("/api/v1/tasks", response_model=TaskResponse)
async def create_task(request: TaskRequest):
    """
    Create and execute a new task.

    This endpoint routes the task to the appropriate agent:
    - If agent is specified, routes directly to that agent
    - If not specified, routes to Manager agent for intelligent routing

    The agent will autonomously use tools and specialists as needed.
    """
    task_id = f"task_{uuid.uuid4().hex[:12]}"

    logger.info(
        "task_received",
        task_id=task_id,
        task=request.task[:100],
        agent=request.agent
    )

    try:
        # Determine which agent to use
        if request.agent and request.agent != "manager":
            # Direct to specialist
            agent = get_specialist_agent(request.agent)
        else:
            # Use manager for intelligent routing
            agent = get_manager_agent()

        # Execute the task
        result = await agent.run(
            task=request.task,
            context=request.context,
            max_iterations=request.max_iterations
        )

        # Build response
        response = TaskResponse(
            task_id=task_id,
            success=result.get("success", False),
            agent_id=result.get("agent_id", agent.agent_id),
            result=result.get("result"),
            error=result.get("error"),
            iterations=result.get("iterations"),
            elapsed_seconds=result.get("elapsed_seconds"),
            usage=result.get("usage")
        )

        logger.info(
            "task_completed",
            task_id=task_id,
            success=response.success,
            agent_id=response.agent_id
        )

        return response

    except Exception as e:
        logger.error("task_failed", task_id=task_id, error=str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Task execution failed: {str(e)}"
        )


@app.get("/api/v1/agents")
async def list_agents():
    """List all available agents and their capabilities."""
    return {
        "manager": {
            "id": "manager",
            "name": "Manager Agent",
            "description": "Orchestrates specialist agents and routes tasks intelligently",
            "capabilities": [
                "Task routing",
                "Multi-agent coordination",
                "Quality validation",
                "Human approval workflows"
            ]
        },
        "analyst": {
            "id": "analyst",
            "name": "Analyst Agent",
            "description": "Market research, competitive analysis, opportunity identification",
            "capabilities": [
                "Market research",
                "Competitive analysis",
                "Opportunity identification",
                "Data-driven insights"
            ]
        },
        "growth_hacker": {
            "id": "growth_hacker",
            "name": "Growth Hacker Agent",
            "description": "Customer acquisition strategies, growth experiments, scaling tactics",
            "capabilities": [
                "Growth strategy design",
                "Experiment frameworks",
                "Viral loop mechanics",
                "Metrics tracking"
            ]
        },
        "sales_machine": {
            "id": "sales_machine",
            "name": "Sales Machine Agent",
            "description": "Sales copy, conversion optimization, offer design",
            "capabilities": [
                "Sales copywriting",
                "Offer design",
                "Email sequences",
                "Objection handling"
            ]
        },
        "system_builder": {
            "id": "system_builder",
            "name": "System Builder Agent",
            "description": "Process documentation, automation workflows, scaling plans",
            "capabilities": [
                "Process mapping",
                "Automation design",
                "SOP creation",
                "Scaling playbooks"
            ]
        },
        "brand_builder": {
            "id": "brand_builder",
            "name": "Brand Builder Agent",
            "description": "Content creation, authority building, audience engagement",
            "capabilities": [
                "Content strategy",
                "SEO optimization",
                "Social media content",
                "Thought leadership"
            ]
        }
    }


@app.get("/api/v1/config")
async def get_config():
    """Get current system configuration (non-sensitive)."""
    return {
        "environment": settings.environment,
        "default_model": settings.default_model,
        "max_tokens": settings.max_tokens,
        "temperature": settings.temperature,
        "task_timeout_seconds": settings.task_timeout_seconds,
        "features": {
            "web_search": bool(settings.brave_api_key or settings.serpapi_key),
            "auto_approve_content": settings.auto_approve_content,
            "auto_approve_analysis": settings.auto_approve_analysis
        }
    }


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize system on startup."""
    logger.info(
        "system_startup",
        environment=settings.environment,
        model=settings.default_model
    )


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("system_shutdown")
