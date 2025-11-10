# 🤖 Autonomous AI Dream Team

A sophisticated multi-agent AI system powered by Claude Sonnet 4.5 that accelerates business growth through intelligent task orchestration. This system coordinates 5 specialized AI agents to handle market research, growth strategies, sales copy, process automation, and content creation.

## 🌟 Key Features

- **🎯 Manager-Pattern Architecture**: Central orchestrator coordinates 5 specialized agents
- **🔄 Autonomous Operation**: Agents use tools and collaborate without human intervention
- **🚀 Production-Ready**: FastAPI backend, Docker deployment, comprehensive logging
- **💰 Cost-Efficient**: ~$300-500/month operational costs
- **⚡ Fast**: Claude Sonnet 4.5 with optimized prompts and tool use
- **🔒 Safe**: Built-in guardrails, human approval workflows for high-stakes decisions

## 🤝 The Agent Team

### 1. **Manager Agent** (Orchestrator)
- Routes tasks to appropriate specialists
- Coordinates multi-agent workflows
- Validates outputs for quality
- Manages human approval workflows

### 2. **Analyst Agent**
- Market research and sizing
- Competitive analysis
- Opportunity identification
- Data-driven insights

### 3. **Growth Hacker Agent**
- Customer acquisition strategies
- Growth experiment design
- Viral loop mechanics
- Rapid scaling tactics

### 4. **Sales Machine Agent**
- High-converting sales copy
- Landing page optimization
- Email sequences
- Objection handling scripts

### 5. **System Builder Agent**
- Process documentation (SOPs)
- Automation workflow design
- Scaling playbooks
- Operational systems

### 6. **Brand Builder Agent**
- Content strategy and creation
- SEO optimization
- Social media content
- Thought leadership

## 🏗️ Architecture

```
User Request
    ↓
Manager Agent (Claude Sonnet 4.5)
    ↓
┌────────┬──────────┬──────────┬──────────┐
│Analyst │Growth    │Sales     │System    │Brand
│        │Hacker    │Machine   │Builder   │Builder
└────────┴──────────┴──────────┴──────────┘
    ↓
Tools Layer (Web Search, Data Extraction, etc.)
    ↓
Results Aggregation & Validation
    ↓
User Response
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose (optional, for containerized deployment)
- Anthropic API Key (Claude)
- Optional: Brave Search API or SerpAPI key for web search

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd autonomous-ai-team
   ```

2. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**

   **Option A: Direct Python**
   ```bash
   python main.py
   ```

   **Option B: Uvicorn**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   **Option C: Docker**
   ```bash
   cd docker
   docker-compose up --build
   ```

5. **Access the API**
   - API: http://localhost:8000
   - Interactive Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 📖 Usage Examples

### Example 1: Direct API Call

```bash
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Analyze the SaaS project management market and identify top 3 opportunities for design teams",
    "context": {
      "product": "AI-powered task management for designers",
      "budget": "$10,000"
    }
  }'
```

### Example 2: Using Python Script

```python
import asyncio
from src.agents.manager import ManagerAgent

async def main():
    manager = ManagerAgent()

    result = await manager.run(
        task="Create a growth strategy to acquire 1,000 customers in 60 days",
        context={
            "product": "AI code review tool",
            "current_customers": 100,
            "budget": "$15,000"
        }
    )

    print(result["result"])

asyncio.run(main())
```

### Example 3: Direct Specialist Agent

```python
from src.agents.analyst import AnalystAgent

async def analyze_market():
    analyst = AnalystAgent()

    result = await analyst.run(
        task="Analyze the AI-powered productivity tools market"
    )

    print(result["result"])
```

### Example 4: Running Example Scripts

```bash
python scripts/example_usage.py
```

## 🔧 Configuration

Edit `.env` file to configure:

```env
# Required
ANTHROPIC_API_KEY=your_claude_api_key

# Optional
BRAVE_API_KEY=your_brave_search_key  # For web search
SERPAPI_KEY=your_serpapi_key         # Alternative web search

# Model Settings
DEFAULT_MODEL=claude-sonnet-4-5
MAX_TOKENS=4096
TEMPERATURE=0.7

# Rate Limiting
MAX_COST_PER_DAY=50.0
RATE_LIMIT_PER_MINUTE=60

# Human Approval
FINANCIAL_APPROVAL_THRESHOLD=1000.0
AUTO_APPROVE_CONTENT=true
AUTO_APPROVE_ANALYSIS=true
```

## 📡 API Endpoints

### `POST /api/v1/tasks`
Create and execute a task

**Request:**
```json
{
  "task": "Your task description",
  "context": {
    "key": "value"
  },
  "agent": "manager",  // or specific agent: analyst, growth_hacker, etc.
  "max_iterations": 10
}
```

**Response:**
```json
{
  "task_id": "task_abc123",
  "success": true,
  "agent_id": "manager",
  "result": "Detailed result...",
  "iterations": 3,
  "elapsed_seconds": 12.5,
  "usage": {
    "input_tokens": 1500,
    "output_tokens": 2000
  }
}
```

### `GET /api/v1/agents`
List all available agents and their capabilities

### `GET /api/v1/config`
Get current system configuration

### `GET /health`
Health check endpoint

## 🏗️ Project Structure

```
autonomous-ai-team/
├── src/
│   ├── agents/              # Agent implementations
│   │   ├── manager.py       # Manager agent (orchestrator)
│   │   ├── analyst.py       # Market research agent
│   │   ├── growth_hacker.py # Growth strategy agent
│   │   ├── sales_machine.py # Sales copy agent
│   │   ├── system_builder.py # Process automation agent
│   │   └── brand_builder.py  # Content creation agent
│   ├── core/                # Core system components
│   │   ├── agent_base.py    # Base agent class
│   │   ├── tools.py         # Tool implementations
│   │   ├── prompts.py       # System prompts for all agents
│   │   ├── config.py        # Configuration management
│   │   └── logger.py        # Logging setup
│   └── api/                 # FastAPI application
│       ├── routes.py        # API endpoints
│       └── models.py        # Pydantic models
├── docker/                  # Docker configuration
│   ├── Dockerfile
│   └── docker-compose.yml
├── scripts/                 # Utility scripts
│   └── example_usage.py    # Usage examples
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
└── main.py                 # Application entry point
```

## 🔐 Security & Safety

### Built-in Guardrails

1. **Cost Control**: Max daily spending limits
2. **Rate Limiting**: Request throttling
3. **Human Approval**: High-stakes decisions require approval
4. **Input Validation**: Sanitized inputs
5. **Error Handling**: Graceful degradation

### Human Approval Triggers

The system automatically requests human approval for:
- Financial commitments >$1,000
- Major strategic pivots
- Legal/compliance matters
- Brand-impacting public communications

Configure thresholds in `.env`:
```env
FINANCIAL_APPROVAL_THRESHOLD=1000.0
AUTO_APPROVE_CONTENT=true
AUTO_APPROVE_ANALYSIS=true
```

## 📊 Monitoring & Logging

The system uses structured logging (structlog) with the following levels:

- `INFO`: Normal operations, agent executions
- `WARNING`: Human approval requests, retries
- `ERROR`: Failures, exceptions

View logs:
```bash
# Docker
docker-compose logs -f app

# Direct
# Logs are output to console
```

## 🧪 Testing

```bash
# Run example scripts
python scripts/example_usage.py

# Test API endpoints
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/agents

# Test a simple task
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{"task": "List the capabilities of your team"}'
```

## 🚀 Deployment

### Local Development
```bash
uvicorn main:app --reload
```

### Docker (Recommended)
```bash
cd docker
docker-compose up -d
```

### Production (AWS/GCP)

1. **Build and push Docker image**
   ```bash
   docker build -f docker/Dockerfile -t autonomous-ai-team:latest .
   docker tag autonomous-ai-team:latest your-registry/autonomous-ai-team:latest
   docker push your-registry/autonomous-ai-team:latest
   ```

2. **Deploy to cloud**
   - AWS: Use ECS/Fargate or EC2
   - GCP: Use Cloud Run or Compute Engine
   - Azure: Use Container Instances or App Service

3. **Set up monitoring**
   - CloudWatch (AWS) / Cloud Logging (GCP)
   - Set up alerts for errors and high costs

4. **Configure auto-scaling**
   - Scale based on API request volume
   - Monitor token usage and costs

## 💰 Cost Estimation

### MVP (Development)
- **Claude API**: ~$200-300/month (3-5M tokens)
- **Infrastructure**: ~$50-100/month (small instance)
- **Web Search API**: ~$50/month
- **Total**: **$300-450/month**

### Production (10K customers served)
- **Claude API**: ~$1,000-1,500/month (10-15M tokens)
- **Infrastructure**: ~$200-300/month (scaled instances)
- **Web Search API**: ~$100-200/month
- **Total**: **$1,300-2,000/month**

### Cost Optimization Tips
1. Use aggressive caching for repeated queries
2. Batch similar requests
3. Monitor and set daily spending limits
4. Use Haiku model for simple tasks (future enhancement)

## 🛠️ Customization

### Adding a New Agent

1. **Create agent class** in `src/agents/`:
   ```python
   from src.core.agent_base import SpecialistAgent
   from src.core.prompts import PROMPTS

   class MyCustomAgent(SpecialistAgent):
       def __init__(self, model: str = None):
           super().__init__(
               agent_id="my_custom_agent",
               specialty="my_specialty",
               model=model
           )

       @property
       def system_prompt(self) -> str:
           return PROMPTS["my_custom_agent"]
   ```

2. **Add prompt** to `src/core/prompts.py`:
   ```python
   MY_CUSTOM_AGENT_PROMPT = """
   # IDENTITY
   You are...

   # MISSION
   ...
   """

   PROMPTS["my_custom_agent"] = MY_CUSTOM_AGENT_PROMPT
   ```

3. **Register in Manager** (`src/agents/manager.py`):
   ```python
   from .my_custom_agent import MyCustomAgent

   self.specialist_agents["my_custom"] = MyCustomAgent(model=model)
   ```

### Adding a New Tool

1. **Create tool class** in `src/core/tools.py`:
   ```python
   class MyCustomTool(Tool):
       @property
       def name(self) -> str:
           return "my_tool"

       @property
       def description(self) -> str:
           return "Description of what my tool does"

       @property
       def input_schema(self) -> Dict[str, Any]:
           return {...}

       async def execute(self, **kwargs) -> Dict[str, Any]:
           # Tool implementation
           return {"success": True, "data": ...}
   ```

2. **Register tool**:
   ```python
   tool_registry.register(MyCustomTool())
   ```

## 📚 Documentation

- **API Documentation**: http://localhost:8000/docs
- **Architecture**: See PRD in project root (if included)
- **Claude Documentation**: https://docs.anthropic.com/
- **Prompt Engineering**: https://docs.anthropic.com/claude/docs/prompt-engineering

## 🐛 Troubleshooting

### Common Issues

**1. API Key Not Working**
```bash
# Verify your .env file
cat .env | grep ANTHROPIC_API_KEY

# Test the key
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01"
```

**2. Web Search Not Working**
- Ensure you have either `BRAVE_API_KEY` or `SERPAPI_KEY` set
- Check API key validity
- Agents will work without web search but with limited research capabilities

**3. Docker Container Won't Start**
```bash
# Check logs
docker-compose logs app

# Rebuild
docker-compose down
docker-compose up --build
```

**4. High Token Usage / Costs**
- Reduce `MAX_TOKENS` in .env
- Decrease `max_iterations` in API requests
- Implement caching for repeated queries
- Use more specific, focused prompts

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Additional specialist agents (e.g., Data Analyst, Customer Success)
- More sophisticated tools (database queries, API integrations)
- Advanced evaluation metrics
- Dashboard UI for monitoring
- Celery integration for async task processing
- PostgreSQL integration for persistent storage

## 📄 License

[Your License Here]

## 🙏 Acknowledgments

- Built with [Claude Sonnet 4.5](https://www.anthropic.com/claude) by Anthropic
- Inspired by modern agentic AI patterns
- Designed for real-world business impact

## 📞 Support

For issues, questions, or feature requests:
- Open an issue on GitHub
- [Your contact information]

---

**Built with ❤️ and 🤖 by [Your Name/Company]**
