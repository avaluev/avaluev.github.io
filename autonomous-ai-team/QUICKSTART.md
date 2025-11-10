# 🚀 Quick Start Guide

Get up and running with the Autonomous AI Team in 5 minutes.

## 1️⃣ Get Your API Key

1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create a new key and copy it

## 2️⃣ Setup (Choose One Method)

### Option A: Automated Setup (Recommended)

```bash
cd autonomous-ai-team
./scripts/setup.sh
```

Then edit `.env` and add your API key:
```bash
nano .env
# Replace 'your_claude_api_key_here' with your actual key
```

### Option B: Manual Setup

```bash
cd autonomous-ai-team

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Add your ANTHROPIC_API_KEY
```

### Option C: Docker

```bash
cd autonomous-ai-team
cp .env.example .env
nano .env  # Add your ANTHROPIC_API_KEY

cd docker
docker-compose up --build
```

## 3️⃣ Run Your First Agent

### Try the Example Script

```bash
source venv/bin/activate
python scripts/example_usage.py
```

This will run a market analysis example that demonstrates the Analyst agent.

### Or Start the API Server

```bash
source venv/bin/activate
python main.py
```

Then visit:
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Or Make a Direct API Call

```bash
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "What are the capabilities of your team?",
    "agent": "manager"
  }'
```

## 4️⃣ Try Real Tasks

### Market Research
```bash
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Analyze the AI-powered productivity tools market and identify top 3 opportunities",
    "context": {
      "product": "Task management for remote teams",
      "budget": "$10,000"
    }
  }'
```

### Growth Strategy
```bash
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Design a growth strategy to reach 1,000 customers in 60 days",
    "context": {
      "product": "AI code review tool",
      "current_customers": 50,
      "budget": "$15,000"
    }
  }'
```

### Sales Copy
```bash
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Create a landing page copy for my SaaS product",
    "context": {
      "product": "Project management for designers",
      "target_audience": "creative agencies",
      "main_benefit": "15% faster project delivery"
    }
  }'
```

## 5️⃣ Use Python Directly

Create a file `my_agent_test.py`:

```python
import asyncio
from src.agents.manager import ManagerAgent

async def main():
    manager = ManagerAgent()

    result = await manager.run(
        task="Help me understand my team's capabilities and suggest a good first task",
        context={
            "business": "B2B SaaS startup",
            "stage": "Pre-launch"
        }
    )

    if result["success"]:
        print("✅ SUCCESS!\n")
        print(result["result"])
    else:
        print("❌ ERROR:", result.get("error"))

asyncio.run(main())
```

Run it:
```bash
python my_agent_test.py
```

## 🎯 What Each Agent Does

| Agent | Best For | Example Task |
|-------|----------|--------------|
| **Manager** | Complex, multi-step tasks | "Create a complete go-to-market strategy" |
| **Analyst** | Market research | "Analyze the SaaS productivity market" |
| **Growth Hacker** | Customer acquisition | "Design experiments to grow from 0 to 1K users" |
| **Sales Machine** | Sales copy | "Write a landing page for my product" |
| **System Builder** | Process automation | "Create an SOP for customer onboarding" |
| **Brand Builder** | Content creation | "Write 10 LinkedIn posts about AI" |

## 🔧 Quick Configuration

Edit `.env` to customize:

```env
# Model Settings
DEFAULT_MODEL=claude-sonnet-4-5  # The AI model to use
MAX_TOKENS=4096                   # Max response length
TEMPERATURE=0.7                   # Creativity (0.0-1.0)

# Cost Control
MAX_COST_PER_DAY=50.0            # Daily spending limit

# Features
AUTO_APPROVE_CONTENT=true         # Auto-approve content creation
AUTO_APPROVE_ANALYSIS=true        # Auto-approve market analysis
```

## 📊 Understanding Results

Each task returns:

```json
{
  "task_id": "task_abc123",           // Unique identifier
  "success": true,                     // Did it work?
  "agent_id": "manager",               // Which agent handled it
  "result": "The actual output...",    // Main result (markdown)
  "iterations": 3,                     // Tool use rounds
  "elapsed_seconds": 12.5,             // Time taken
  "usage": {                           // Cost tracking
    "input_tokens": 1500,
    "output_tokens": 2000
  }
}
```

## 💡 Pro Tips

1. **Be Specific**: More context = better results
   ```json
   {
     "task": "Analyze market opportunities",
     "context": {
       "product": "AI writing assistant",
       "target_market": "content marketers",
       "budget": "$20k",
       "timeline": "6 months"
     }
   }
   ```

2. **Use Manager for Complex Tasks**: Let it coordinate specialists
   ```json
   {
     "task": "Research the market, design a growth strategy, and create sales copy",
     "agent": "manager"
   }
   ```

3. **Direct to Specialists for Speed**: Skip routing for known tasks
   ```json
   {
     "task": "Write an email sequence",
     "agent": "sales_machine"
   }
   ```

4. **Monitor Costs**: Check logs for token usage
   ```bash
   # Watch logs in real-time
   docker-compose logs -f app
   ```

## 🐛 Troubleshooting

**"No module named 'src'"**
```bash
# Make sure you're in the autonomous-ai-team directory
cd autonomous-ai-team
python -c "import src; print('✓ Working!')"
```

**"API key not configured"**
```bash
# Check your .env file
cat .env | grep ANTHROPIC_API_KEY

# Should NOT be: your_claude_api_key_here
# Should be: sk-ant-...
```

**"Connection refused"**
```bash
# Make sure the server is running
python main.py

# Or with Docker
cd docker && docker-compose up
```

**"Rate limit exceeded"**
- You're hitting Anthropic's rate limits
- Wait a few seconds and try again
- Consider reducing `MAX_TOKENS` in `.env`

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore [scripts/example_usage.py](scripts/example_usage.py) for more examples
- Check the API docs at http://localhost:8000/docs
- Customize agents in `src/agents/`
- Add new tools in `src/core/tools.py`

## 🆘 Need Help?

- Check the [README.md](README.md) for comprehensive documentation
- Look at example scripts in `scripts/`
- Review logs for error details
- Open an issue on GitHub

---

**Ready to accelerate your business growth? Let's go! 🚀**
