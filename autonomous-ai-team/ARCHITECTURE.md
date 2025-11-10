# System Architecture - Autonomous AI Team

## Design Principles

This system is built on four core principles:

### 1. KISS (Keep It Simple, Stupid)
- Simple solutions over complex ones
- Direct file-based configuration
- Minimal abstractions
- Clear code paths

### 2. DRY (Don't Repeat Yourself)
- Prompts defined once in markdown files
- Configuration centralized in JSON
- Reusable components
- Shared utilities

### 3. Token Safety
- Track every token used
- Budget management and alerts
- Caching to prevent redundant API calls
- Cost optimization suggestions

### 4. Lean Approach
- Minimal dependencies
- Fast startup and execution
- No unnecessary features
- Production-ready from day 1

---

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    CONFIGURATION LAYER                       │
│  ┌────────────────┬───────────────┬──────────────────────┐  │
│  │ config/prompts/│ config/*.json │ config/knowledge/    │  │
│  │ - manager.md   │ - agents.json │ - agent_guidelines.md│  │
│  │ - analyst.md   │ - tools.json  │ - best_practices.md  │  │
│  │ - ...          │ - ...         │ - ...                │  │
│  └────────────────┴───────────────┴──────────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                      CORE LAYER                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ PromptLoader: Load & cache prompts from markdown     │   │
│  │ TokenManager: Track usage & enforce budgets          │   │
│  │ AgentBase: Base class with prompt + token integration│   │
│  │ ToolRegistry: Centralized tool management            │   │
│  └──────────────────────────────────────────────────────┘   │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    AGENT LAYER                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Manager Agent ──┬─→ Analyst Agent                    │   │
│  │                 ├─→ Growth Hacker Agent              │   │
│  │                 ├─→ Sales Machine Agent              │   │
│  │                 ├─→ System Builder Agent             │   │
│  │                 └─→ Brand Builder Agent              │   │
│  └──────────────────────────────────────────────────────┘   │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                      API LAYER                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ FastAPI Application                                   │   │
│  │ - POST /api/v1/tasks                                  │   │
│  │ - GET /api/v1/agents                                  │   │
│  │ - GET /api/v1/usage (token tracking)                  │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Directory Structure

```
autonomous-ai-team/
├── config/                          # 📁 Configuration (KISS)
│   ├── prompts/                     # Agent prompts (markdown)
│   │   ├── manager.md               # Manager agent system prompt
│   │   ├── analyst.md               # Analyst agent system prompt
│   │   ├── growth_hacker.md         # Growth Hacker prompt
│   │   ├── sales_machine.md         # Sales Machine prompt
│   │   ├── system_builder.md        # System Builder prompt
│   │   └── brand_builder.md         # Brand Builder prompt
│   ├── knowledge/                   # Knowledge base (guidelines)
│   │   ├── agent_guidelines.md      # Best practices for all agents
│   │   └── ...                      # Additional knowledge files
│   ├── evaluation/                  # Test cases and benchmarks
│   │   └── test_cases.json          # Automated test scenarios
│   ├── schemas/                     # JSON schemas for validation
│   ├── agents.json                  # Agent metadata & configuration
│   └── tools.json                   # Tool definitions & metadata
│
├── src/
│   ├── core/                        # 🎯 Core Framework (DRY)
│   │   ├── agent_base.py            # Base agent class
│   │   ├── prompt_loader.py         # Loads prompts from markdown
│   │   ├── token_manager.py         # Token counting & budgets
│   │   ├── tools.py                 # Tool implementations
│   │   ├── config.py                # Settings management
│   │   └── logger.py                # Structured logging
│   │
│   ├── agents/                      # 🤖 Specialized Agents
│   │   ├── manager.py               # Manager (orchestrator)
│   │   ├── analyst.py               # Analyst specialist
│   │   ├── growth_hacker.py         # Growth Hacker specialist
│   │   ├── sales_machine.py         # Sales Machine specialist
│   │   ├── system_builder.py        # System Builder specialist
│   │   └── brand_builder.py         # Brand Builder specialist
│   │
│   ├── api/                         # 🌐 REST API
│   │   ├── routes.py                # API endpoints
│   │   └── models.py                # Request/response models
│   │
│   ├── db/                          # 💾 Data Layer
│   │   ├── models.py                # Database models
│   │   └── crud.py                  # CRUD operations
│   │
│   └── evaluation/                  # 🧪 Testing & Evaluation
│       ├── metrics.py               # Custom evaluation metrics
│       └── runner.py                # Test runner
│
├── docker/                          # 🐳 Deployment
│   ├── Dockerfile                   # Container image
│   └── docker-compose.yml           # Multi-container setup
│
├── scripts/                         # 🛠️ Utilities
│   ├── setup.sh                     # Quick setup script
│   ├── example_usage.py             # Usage examples
│   └── evaluate.sh                  # Run evaluation tests
│
├── tests/                           # ✅ Tests
│   └── integration/                 # Integration tests
│
├── .env.example                     # Environment template
├── requirements.txt                 # Python dependencies
├── main.py                          # Application entry point
├── README.md                        # User documentation
├── QUICKSTART.md                    # Quick start guide
└── ARCHITECTURE.md                  # This file
```

---

## Key Components

### 1. Configuration Layer (KISS + DRY)

#### Prompt Files (`config/prompts/*.md`)
- **Why Markdown**: Human-readable, version-controllable, easy to edit
- **Caching**: LRU cache prevents re-loading (saves tokens)
- **Structure**: Each prompt has clear sections (Identity, Methodology, Output Format)
- **Validation**: PromptLoader validates completeness

#### Configuration Files (`config/*.json`)
- **agents.json**: Agent metadata (model, temperature, costs, tools)
- **tools.json**: Tool definitions, rate limits, costs
- **Separation**: Configuration separate from code (12-factor app)

#### Knowledge Base (`config/knowledge/*.md`)
- **Guidelines**: Best practices, decision frameworks
- **Shared**: Available to all agents
- **Extensible**: Easy to add new knowledge

### 2. Core Framework

#### PromptLoader (`src/core/prompt_loader.py`)
**Purpose**: Load prompts from markdown files with caching

**Key Features**:
- LRU cache (maxsize=32) - prevents redundant loads
- Validation of prompt completeness
- Loads agent configs and tool configs
- Cache statistics for monitoring

**Usage**:
```python
from src.core.prompt_loader import load_prompt

prompt = load_prompt("analyst")  # Cached automatically
```

#### TokenManager (`src/core/token_manager.py`)
**Purpose**: Enforce Token Safety principle

**Key Features**:
- Estimate tokens before API calls (using tiktoken)
- Track actual usage (per agent, per day)
- Budget enforcement (daily limits)
- Cost optimization suggestions
- Multi-model pricing support

**Usage**:
```python
from src.core.token_manager import get_token_manager

tm = get_token_manager()

# Before API call
allowed, reason = tm.should_allow_call(input_text)

# After API call
tm.record_usage("analyst", input_tokens=1500, output_tokens=2000)

# Get stats
summary = tm.get_summary()
```

#### AgentBase (`src/core/agent_base.py`)
**Purpose**: Base class for all agents with built-in token management

**Key Features**:
- Loads prompt from PromptLoader (DRY)
- Tracks tokens automatically (Token Safety)
- Tool use via ToolRegistry (KISS)
- Conversation history management
- Error handling and retries

**Lifecycle**:
```
1. Initialize → Load prompt from file (cached)
2. Run task → Check budget before API call
3. Claude API → Execute with prompt + tools
4. Tool use → Handle tool calls
5. Record usage → Track tokens and cost
6. Return result → With metadata
```

#### ToolRegistry (`src/core/tools.py`)
**Purpose**: Centralized tool management (DRY)

**Key Features**:
- Register tools once, use everywhere
- Tool metadata from config/tools.json
- Rate limiting per tool
- Cost tracking per tool
- Enable/disable tools dynamically

### 3. Agent Layer

Each agent:
1. **Inherits** from `AgentBase` or `SpecialistAgent`
2. **Loads** its prompt from `config/prompts/{agent_id}.md`
3. **Uses** tools from `ToolRegistry`
4. **Tracks** tokens via `TokenManager`
5. **Returns** structured results

**Agent Configuration** (from `agents.json`):
```json
{
  "id": "analyst",
  "model": "claude-sonnet-4-5",
  "temperature": 0.5,
  "max_tokens": 4096,
  "max_iterations": 10,
  "capabilities": [...],
  "available_tools": [...],
  "quality_metrics": {...}
}
```

### 4. API Layer

#### REST API (`src/api/routes.py`)

**Endpoints**:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Health check |
| `/api/v1/tasks` | POST | Execute task (route to agents) |
| `/api/v1/agents` | GET | List agents and capabilities |
| `/api/v1/usage` | GET | Token usage and costs |
| `/api/v1/config` | GET | System configuration |

**Task Execution Flow**:
```
User Request
    ↓
POST /api/v1/tasks
    ↓
Determine Agent (manager or specific)
    ↓
Check Budget (TokenManager)
    ↓
Execute Agent.run()
    ↓
Track Tokens
    ↓
Return Response
```

---

## Token Safety Implementation

### Budget Enforcement

```python
# config/.env
MAX_COST_PER_DAY=50.0
```

**Flow**:
1. Every API call checks budget: `tm.check_budget_available()`
2. If 80% used → Warning logged
3. If 100% used → Calls rejected
4. Per-agent usage tracked for analysis

### Token Estimation

**Before API call**:
```python
estimated_tokens = tm.estimate_tokens(input_text)
estimated_cost = tm.estimate_call_cost(input_text, expected_output=1000)

if estimated_cost > remaining_budget:
    # Reject call or summarize context
```

**After API call**:
```python
tm.record_usage(
    agent_id="analyst",
    input_tokens=response.usage.input_tokens,
    output_tokens=response.usage.output_tokens
)
```

### Cost Optimization

**Automatic Suggestions**:
- High tokens per call → Break into smaller tasks
- Repeated searches → Implement caching
- Large context → Summarize history

**Manual Optimization**:
- Use prompt caching (LRU cache)
- Batch similar requests
- Use cheaper models for simple tasks (future: Haiku)

---

## Data Flow Examples

### Example 1: Simple Task (Analyst)

```
User: "Analyze the SaaS market"
    ↓
[API] POST /api/v1/tasks { task: "...", agent: "analyst" }
    ↓
[PromptLoader] Load analyst.md (cached if exists)
    ↓
[TokenManager] Check budget → OK
    ↓
[AnalystAgent] Claude API call with:
    - System prompt (from analyst.md)
    - Tools: web_search, extract_data, store_context
    - User message
    ↓
[Claude] Uses web_search tool → Results returned
    ↓
[AnalystAgent] Continues until complete (max 10 iterations)
    ↓
[TokenManager] Record usage: 2,500 input + 1,800 output = $0.035
    ↓
[API] Return result with metadata
```

**Cost**: ~$0.03-0.05 per analysis

### Example 2: Complex Multi-Agent Task

```
User: "Create a complete go-to-market strategy"
    ↓
[API] Routes to Manager Agent
    ↓
[Manager] Analyzes request → Needs Analyst + Growth Hacker + Sales Machine
    ↓
[Manager] Calls Analyst: "Find market opportunities"
    ↓
[Analyst] Executes, returns opportunities (cost: $0.04)
    ↓
[Manager] Calls Growth Hacker: "Design strategy for [opportunities]"
    ↓
[GrowthHacker] Executes, returns strategy (cost: $0.06)
    ↓
[Manager] Calls Sales Machine: "Create landing page for [product]"
    ↓
[SalesMachine] Executes, returns copy (cost: $0.05)
    ↓
[Manager] Synthesizes all outputs into cohesive plan
    ↓
[API] Returns integrated strategy
```

**Total Cost**: ~$0.20-0.30 for complex orchestration

---

## Configuration Management

### Agent Configuration (`config/agents.json`)

**Purpose**: Centralize agent metadata

**Benefits**:
- Change model per agent without code changes
- Adjust temperature for creativity
- Define cost per agent
- Enable/disable capabilities

**Example**:
```json
{
  "agents": {
    "analyst": {
      "model": "claude-sonnet-4-5",
      "temperature": 0.5,  # Lower = more factual
      "quality_metrics": {
        "min_data_sources": 3,
        "require_urls": true
      }
    },
    "sales_machine": {
      "model": "claude-sonnet-4-5",
      "temperature": 0.9,  # Higher = more creative
      "quality_metrics": {
        "require_cta": true,
        "require_ab_variants": true
      }
    }
  }
}
```

### Tool Configuration (`config/tools.json`)

**Purpose**: Define tool behavior and limits

**Benefits**:
- Enable/disable tools without code
- Set rate limits per tool
- Track costs per tool
- Configure API keys

**Example**:
```json
{
  "tools": {
    "web_search": {
      "enabled": true,
      "rate_limit_per_minute": 10,
      "cost_per_call": 0.001,
      "requires_api_key": true,
      "timeout_seconds": 30
    }
  }
}
```

---

## Evaluation Framework

### Test Cases (`config/evaluation/test_cases.json`)

**Purpose**: Automated quality assurance

**Structure**:
```json
{
  "test_cases": [
    {
      "id": "analyst_001",
      "agent": "analyst",
      "task": "...",
      "expected_outputs": {
        "opportunities_count": 3,
        "has_data_sources": true,
        "min_data_sources": 3
      },
      "quality_checks": [...],
      "max_cost_usd": 0.50,
      "max_duration_seconds": 120
    }
  ]
}
```

**Run Tests**:
```bash
python -m src.evaluation.runner
```

**Benefits**:
- Catch regressions
- Validate quality standards
- Monitor performance
- Track costs

---

## Performance Benchmarks

### Target Metrics (from `config/evaluation/test_cases.json`)

| Agent | Response Time | Iterations | Token Budget | Cost |
|-------|---------------|------------|--------------|------|
| Manager | <30s | 3-5 | 6,000 | $0.05-0.15 |
| Analyst | <60s | 5-8 | 8,000 | $0.03-0.08 |
| Growth Hacker | <45s | 4-6 | 7,000 | $0.04-0.10 |
| Sales Machine | <30s | 2-4 | 5,000 | $0.03-0.06 |
| System Builder | <60s | 5-8 | 8,000 | $0.04-0.10 |
| Brand Builder | <45s | 3-5 | 6,000 | $0.03-0.08 |

### Daily Budget Allocation

**Recommended** ($50/day budget):
- Manager: $15/day (30% - orchestration heavy)
- Analyst: $10/day (20% - data-intensive)
- Growth Hacker: $8/day (16%)
- Sales Machine: $6/day (12%)
- System Builder: $6/day (12%)
- Brand Builder: $5/day (10%)

---

## Deployment

### Development
```bash
python main.py
```

### Production (Docker)
```bash
cd docker
docker-compose up -d
```

### Environment Variables
See `.env.example` for required configuration.

---

## Monitoring & Observability

### Structured Logging
All operations logged with `structlog`:
```json
{
  "event": "token_usage_recorded",
  "agent_id": "analyst",
  "input_tokens": 1500,
  "output_tokens": 2000,
  "cost_usd": 0.0345,
  "timestamp": "2025-01-15T10:30:00Z"
}
```

### Token Usage Endpoint
```bash
GET /api/v1/usage
```

Returns:
```json
{
  "daily_usage": {
    "total_cost_usd": 12.45,
    "budget_remaining_usd": 37.55,
    "budget_used_percentage": 24.9
  },
  "agent_usage": {...},
  "optimization_suggestions": [...]
}
```

---

## Extending the System

### Adding a New Agent

1. **Create prompt file**: `config/prompts/my_agent.md`
2. **Add to agents.json**: Define metadata
3. **Create agent class**: `src/agents/my_agent.py`
4. **Register in Manager**: Add tool for calling agent
5. **Test**: Add test case in `test_cases.json`

### Adding a New Tool

1. **Define in tools.json**: Metadata, rate limits, cost
2. **Implement in tools.py**: Create Tool class
3. **Register**: `tool_registry.register(MyTool())`
4. **Test**: Verify tool works with agents

---

## Security & Compliance

### API Key Management
- Keys in `.env` (never committed)
- Accessed via `settings` (type-safe)
- Validated at startup

### Budget Controls
- Daily spending limits
- Per-agent tracking
- Automatic alerts at 80% budget
- Stop execution at 95% budget

### Data Handling
- No PII stored in logs
- Context storage (Redis) is ephemeral
- All communications over HTTPS in production

---

## Troubleshooting

### High Token Usage
```python
# Get optimization suggestions
tm = get_token_manager()
suggestions = tm.get_cost_optimization_suggestions()
```

### Prompt Not Loading
```python
# Check available prompts
from src.core.prompt_loader import get_prompt_loader
loader = get_prompt_loader()
prompts = loader.list_available_prompts()
```

### Budget Exceeded
```python
# Check usage
GET /api/v1/usage

# Adjust budget in .env
MAX_COST_PER_DAY=100.0
```

---

## Future Enhancements

### Phase 2
- [ ] Add Claude Haiku support for simple tasks (5x cheaper)
- [ ] Implement prompt caching API (Anthropic native)
- [ ] Add PostgreSQL for persistent storage
- [ ] Build web dashboard for monitoring

### Phase 3
- [ ] Multi-model support (Gemini for specific tasks)
- [ ] Advanced RAG for knowledge base
- [ ] A/B testing framework for prompts
- [ ] Automated prompt optimization

---

## Conclusion

This architecture implements a **bulletproof backbone** for autonomous multi-agent AI:

✅ **KISS**: Simple file-based configuration, clear code structure
✅ **DRY**: Prompts and configs defined once, reused everywhere
✅ **Token Safety**: Comprehensive tracking, budgets, optimization
✅ **Lean**: Production-ready, minimal overhead, fast execution

**Result**: A maintainable, cost-effective, production-ready system that scales from MVP to serving 10,000 customers.
