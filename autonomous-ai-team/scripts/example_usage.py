"""
Example usage of the Autonomous AI Team system.
This script demonstrates how to use the agents directly (without the API).
"""

import asyncio
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.manager import ManagerAgent
from src.agents.analyst import AnalystAgent
from src.core.logger import setup_logging, get_logger
from src.core.config import settings

setup_logging()
logger = get_logger(__name__)


async def example_1_market_analysis():
    """Example 1: Market analysis using the Analyst agent directly."""
    print("\n" + "="*80)
    print("EXAMPLE 1: Direct Analyst Agent - Market Analysis")
    print("="*80 + "\n")

    analyst = AnalystAgent()

    task = """
    Analyze the market for AI-powered productivity tools for remote teams.
    Identify the top 3 underserved opportunities with specific market data.
    """

    print(f"Task: {task}\n")
    print("Running Analyst Agent...")

    result = await analyst.run(task=task)

    if result["success"]:
        print("\n✅ SUCCESS!\n")
        print(result["result"])
        print(f"\n📊 Stats: {result['iterations']} iterations, {result['elapsed_seconds']:.2f}s")
        print(f"💰 Tokens: {result['usage']['input_tokens']} in, {result['usage']['output_tokens']} out")
    else:
        print("\n❌ FAILED!\n")
        print(f"Error: {result.get('error')}")


async def example_2_manager_orchestration():
    """Example 2: Using Manager agent to orchestrate multiple specialists."""
    print("\n" + "="*80)
    print("EXAMPLE 2: Manager Agent - Multi-Agent Orchestration")
    print("="*80 + "\n")

    manager = ManagerAgent()

    task = """
    I'm launching a SaaS product for project management aimed at design teams.

    Please help me with:
    1. Identify the best market opportunities in this space
    2. Design a growth strategy to reach 1,000 customers in 60 days
    3. Create a landing page copy that converts

    Coordinate your team to deliver a comprehensive plan.
    """

    print(f"Task: {task}\n")
    print("Running Manager Agent (this will coordinate multiple specialists)...")

    result = await manager.run(task=task, max_iterations=15)

    if result["success"]:
        print("\n✅ SUCCESS!\n")
        print(result["result"])
        print(f"\n📊 Stats: {result['iterations']} iterations, {result['elapsed_seconds']:.2f}s")
        print(f"💰 Tokens: {result['usage']['input_tokens']} in, {result['usage']['output_tokens']} out")
    else:
        print("\n❌ FAILED!\n")
        print(f"Error: {result.get('error')}")


async def example_3_with_context():
    """Example 3: Providing rich context to agents."""
    print("\n" + "="*80)
    print("EXAMPLE 3: Manager Agent with Rich Context")
    print("="*80 + "\n")

    manager = ManagerAgent()

    task = "Create a growth strategy to acquire our next 500 customers"

    context = {
        "product": "AI-powered code review tool",
        "current_customers": 100,
        "monthly_revenue": "$5,000 MRR",
        "target_market": "software engineering teams at startups",
        "budget": "$10,000",
        "timeline": "90 days",
        "current_channels": "Product Hunt, Reddit, organic search"
    }

    print(f"Task: {task}\n")
    print("Context provided:")
    for key, value in context.items():
        print(f"  - {key}: {value}")
    print("\nRunning Manager Agent...")

    result = await manager.run(task=task, context=context)

    if result["success"]:
        print("\n✅ SUCCESS!\n")
        print(result["result"])
        print(f"\n📊 Stats: {result['iterations']} iterations, {result['elapsed_seconds']:.2f}s")
    else:
        print("\n❌ FAILED!\n")
        print(f"Error: {result.get('error')}")


async def main():
    """Run all examples."""
    print("\n" + "🤖"*40)
    print("AUTONOMOUS AI TEAM - USAGE EXAMPLES")
    print("🤖"*40)

    print(f"\n⚙️  Configuration:")
    print(f"   Model: {settings.default_model}")
    print(f"   Environment: {settings.environment}")
    print(f"   Max Tokens: {settings.max_tokens}")

    # Check API key
    if not settings.anthropic_api_key or settings.anthropic_api_key == "your_claude_api_key_here":
        print("\n❌ ERROR: Please set ANTHROPIC_API_KEY in your .env file!")
        print("   Copy .env.example to .env and add your API key.")
        return

    print("\n✅ API Key configured\n")

    # Uncomment the examples you want to run:

    # Example 1: Direct specialist agent usage
    await example_1_market_analysis()

    # Example 2: Manager orchestrating multiple agents
    # await example_2_manager_orchestration()

    # Example 3: Providing rich context
    # await example_3_with_context()

    print("\n" + "="*80)
    print("✨ Examples completed!")
    print("="*80 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
