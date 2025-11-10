# macOS Setup Guide - Autonomous AI Team

Complete guide to download, setup, and run the multi-agent system on macOS using VSCode and Claude Code.

## Prerequisites

### Required Software

1. **macOS** 12.0 (Monterey) or later
2. **Homebrew** (package manager)
3. **Python 3.11+**
4. **Git**
5. **VSCode**
6. **Claude Code** (VSCode extension)

### API Keys Required

- **Anthropic API Key** (required) - Get from https://console.anthropic.com/
- **Brave Search API Key** (optional) - Get from https://brave.com/search/api/
- **SerpAPI Key** (optional, alternative to Brave) - Get from https://serpapi.com/

---

## Step 1: Install Required Software

### 1.1 Install Homebrew (if not already installed)

```bash
# Check if Homebrew is installed
brew --version

# If not installed, install it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Follow the instructions to add Homebrew to your PATH
```

### 1.2 Install Python 3.11+

```bash
# Install Python 3.11
brew install python@3.11

# Verify installation
python3.11 --version
# Should show: Python 3.11.x

# Set as default python3 (optional)
brew link python@3.11
```

### 1.3 Install Git (if not already installed)

```bash
# Check if Git is installed
git --version

# If not installed
brew install git

# Configure Git
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 1.4 Install Visual Studio Code

**Option A: Download from website**
1. Go to https://code.visualstudio.com/
2. Download for macOS
3. Drag to Applications folder
4. Open VSCode

**Option B: Install via Homebrew**
```bash
brew install --cask visual-studio-code
```

### 1.5 Install Claude Code Extension

1. Open VSCode
2. Click Extensions icon (⇧⌘X) or View → Extensions
3. Search for "Claude Code"
4. Click "Install" on "Claude Code" by Anthropic
5. Reload VSCode

**Or install via command line:**
```bash
code --install-extension anthropic.claude-code
```

---

## Step 2: Download the Repository

### 2.1 Clone the Repository

```bash
# Navigate to where you want the project
cd ~/Documents  # Or your preferred location

# Clone the repository
git clone https://github.com/avaluev/avaluev.github.io.git

# Navigate into the project
cd avaluev.github.io/autonomous-ai-team

# Verify you're in the right place
ls -la
# You should see: README.md, src/, config/, docker/, etc.
```

### 2.2 Switch to the Development Branch (if needed)

```bash
# See all branches
git branch -a

# Switch to the multi-agent branch
git checkout claude/multiagent-subagent-setup-011CUzdMMdeEtP8X8h3BYims

# Or if it's merged, stay on main
git checkout main
```

---

## Step 3: Setup Python Environment

### 3.1 Create Virtual Environment

```bash
# Make sure you're in the autonomous-ai-team directory
cd ~/Documents/avaluev.github.io/autonomous-ai-team

# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Your prompt should now start with (venv)
```

### 3.2 Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt

# Verify installation
pip list
# Should see: anthropic, fastapi, structlog, tiktoken, etc.
```

---

## Step 4: Configure Environment Variables

### 4.1 Create .env File

```bash
# Copy the example file
cp .env.example .env

# Open in your preferred editor
# Using VSCode:
code .env

# Or using nano:
nano .env

# Or using vim:
vim .env
```

### 4.2 Add Your API Keys

Edit `.env` and add your keys:

```bash
# REQUIRED: Anthropic API Key
ANTHROPIC_API_KEY=sk-ant-api03-YOUR_KEY_HERE

# OPTIONAL: Web Search API (choose one)
BRAVE_API_KEY=your_brave_key_here
# OR
SERPAPI_KEY=your_serpapi_key_here

# OPTIONAL: Google/Gemini (for Phase 3)
GOOGLE_API_KEY=your_google_key_here

# Database (use SQLite for local development)
DATABASE_URL=sqlite:///./ai_agents.db

# Redis (use local Redis or skip for now)
REDIS_URL=redis://localhost:6379/0

# Application Settings
ENVIRONMENT=development
LOG_LEVEL=INFO
MAX_RETRIES=3

# Agent Settings
DEFAULT_MODEL=claude-sonnet-4-5
MAX_TOKENS=4096
TEMPERATURE=0.7

# Cost & Rate Limiting
MAX_COST_PER_DAY=50.0
RATE_LIMIT_PER_MINUTE=60

# Human Approval Thresholds
FINANCIAL_APPROVAL_THRESHOLD=1000.0
AUTO_APPROVE_CONTENT=true
AUTO_APPROVE_ANALYSIS=true
```

**Save and close the file** (Ctrl+X in nano, :wq in vim, ⌘S in VSCode)

### 4.3 Get Your Anthropic API Key

1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to "API Keys"
4. Click "Create Key"
5. Copy the key (starts with `sk-ant-api03-`)
6. Paste into `.env` file

### 4.4 (Optional) Get Web Search API Key

**Option A: Brave Search API** (Recommended)
1. Go to https://brave.com/search/api/
2. Sign up for free tier (2,000 queries/month free)
3. Get API key
4. Add to `.env`

**Option B: SerpAPI**
1. Go to https://serpapi.com/
2. Sign up for free tier (100 queries/month free)
3. Get API key
4. Add to `.env`

---

## Step 5: Verify Installation

### 5.1 Check Python Imports

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Test imports
python3 -c "import anthropic; print('✓ Anthropic installed')"
python3 -c "import fastapi; print('✓ FastAPI installed')"
python3 -c "import structlog; print('✓ Structlog installed')"
python3 -c "import tiktoken; print('✓ Tiktoken installed')"

# All should print checkmarks
```

### 5.2 Validate Configuration Files

```bash
# Validate JSON files
python3 -c "import json; json.load(open('config/agents.json')); print('✓ agents.json valid')"
python3 -c "import json; json.load(open('config/tools.json')); print('✓ tools.json valid')"
python3 -c "import json; json.load(open('config/evaluation/test_cases.json')); print('✓ test_cases.json valid')"
```

### 5.3 Test API Connection

```bash
# Create a simple test
cat > test_connection.py << 'EOF'
import os
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=100,
    messages=[
        {"role": "user", "content": "Say hello!"}
    ]
)

print("✓ API connection successful!")
print(f"Response: {message.content[0].text}")
EOF

# Run the test
python3 test_connection.py

# Should print: "✓ API connection successful!" and a greeting

# Clean up
rm test_connection.py
```

---

## Step 6: Run the System

### 6.1 Start the FastAPI Server

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Make sure you're in the project directory
cd ~/Documents/avaluev.github.io/autonomous-ai-team

# Start the server
python main.py

# You should see:
# INFO:     Started server process
# INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Keep this terminal open** - the server is running.

### 6.2 Test the API (in a new terminal)

Open a **new terminal window/tab** and run:

```bash
# Test health check
curl http://localhost:8000/health

# Should return: {"status":"healthy","version":"0.1.0"}

# List available agents
curl http://localhost:8000/api/v1/agents

# Test a simple task
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "List the capabilities of your team",
    "agent": "manager"
  }'
```

### 6.3 View API Documentation

1. Keep the server running
2. Open your browser
3. Go to http://localhost:8000/docs
4. You'll see interactive API documentation
5. Try out endpoints directly from the browser

---

## Step 7: Use with VSCode and Claude Code

### 7.1 Open Project in VSCode

```bash
# Open the project in VSCode
code ~/Documents/avaluev.github.io/autonomous-ai-team
```

### 7.2 Configure Claude Code Extension

1. In VSCode, press `⇧⌘P` (Command Palette)
2. Type "Claude Code: Settings"
3. Select "Claude Code: Configure"
4. Enter your Anthropic API key
5. Select model: "claude-sonnet-4-5"

### 7.3 Use Claude Code for Development

**Example: Ask Claude Code about the system**

1. Open Claude Code chat (`⌘L` or click Claude icon)
2. Ask questions like:
   - "Explain how the Manager Agent works"
   - "Show me how to create a new tool"
   - "How does token tracking work?"
   - "Walk me through creating a new specialist agent"

**Example: Use Claude Code to modify code**

1. Open a file (e.g., `src/agents/analyst.py`)
2. Select some code
3. Press `⌘L` to open Claude Code
4. Ask: "Refactor this to use the new prompt loader"
5. Claude Code will suggest changes

### 7.4 Run Example Scripts

```bash
# Activate virtual environment
source venv/bin/activate

# Run the example usage script
python scripts/example_usage.py

# This will run a market analysis demo
```

---

## Step 8: Run with Docker (Optional)

### 8.1 Install Docker

```bash
# Install Docker Desktop for Mac
brew install --cask docker

# Start Docker Desktop
open -a Docker

# Wait for Docker to start (whale icon in menu bar)

# Verify Docker is running
docker --version
docker-compose --version
```

### 8.2 Build and Run with Docker

```bash
# Navigate to docker directory
cd ~/Documents/avaluev.github.io/autonomous-ai-team/docker

# Make sure .env file exists in parent directory
ls ../.env

# Build and start containers
docker-compose up --build

# The system will start on http://localhost:8000

# To run in background:
docker-compose up -d

# To stop:
docker-compose down
```

---

## Step 9: Development Workflow

### 9.1 Daily Workflow

```bash
# 1. Navigate to project
cd ~/Documents/avaluev.github.io/autonomous-ai-team

# 2. Activate virtual environment
source venv/bin/activate

# 3. Pull latest changes (if working with a team)
git pull

# 4. Install any new dependencies
pip install -r requirements.txt

# 5. Start the server
python main.py

# 6. Open VSCode in another window
code .

# 7. Start developing!
```

### 9.2 Making Changes

**Modify Prompts:**
```bash
# Edit prompt files directly
code config/prompts/analyst.md

# No code changes needed - prompts are loaded dynamically
# Restart server to see changes
```

**Modify Configuration:**
```bash
# Edit agent configuration
code config/agents.json

# Edit tool configuration
code config/tools.json

# Restart server to see changes
```

**Add New Features:**
```bash
# Create a new branch
git checkout -b feature/my-new-feature

# Make your changes
code src/agents/my_new_agent.py

# Test your changes
python -m pytest tests/

# Commit your changes
git add .
git commit -m "feat: Add my new feature"

# Push to GitHub
git push origin feature/my-new-feature
```

### 9.3 Testing

```bash
# Run example scripts
python scripts/example_usage.py

# Test API endpoints
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{"task": "Test task", "agent": "analyst"}'

# Check token usage
curl http://localhost:8000/api/v1/usage
```

---

## Step 10: Troubleshooting

### Common Issues and Solutions

#### Issue: "command not found: python3.11"

**Solution:**
```bash
# Use python3 instead
python3 --version

# Or create an alias
echo 'alias python3.11=python3' >> ~/.zshrc
source ~/.zshrc
```

#### Issue: "No module named 'anthropic'"

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### Issue: "anthropic.AuthenticationError"

**Solution:**
```bash
# Check your API key
cat .env | grep ANTHROPIC_API_KEY

# Make sure it starts with sk-ant-api03-
# If not, get a new key from console.anthropic.com
```

#### Issue: "Port 8000 already in use"

**Solution:**
```bash
# Find what's using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use a different port
uvicorn main:app --port 8001
```

#### Issue: "redis.exceptions.ConnectionError"

**Solution:**
```bash
# Either install Redis:
brew install redis
brew services start redis

# Or disable Redis in .env:
# REDIS_URL=  # Leave empty
```

#### Issue: VSCode can't find Python interpreter

**Solution:**
1. Press `⇧⌘P` in VSCode
2. Type "Python: Select Interpreter"
3. Choose the venv interpreter: `./venv/bin/python`

#### Issue: Changes not reflected

**Solution:**
```bash
# Restart the server
# Stop with Ctrl+C
# Start again
python main.py

# For prompt changes, no code restart needed
# Just reload the prompt loader cache
```

---

## Step 11: Next Steps

### Learn the System

1. **Read Documentation:**
   - [README.md](../README.md) - Overview
   - [ARCHITECTURE.md](../ARCHITECTURE.md) - System design
   - [TOOLS_AND_TECHNIQUES.md](./TOOLS_AND_TECHNIQUES.md) - Tools guide
   - [QUICKSTART.md](../QUICKSTART.md) - Quick reference

2. **Explore Prompts:**
   ```bash
   # Read each agent's prompt
   cat config/prompts/manager.md
   cat config/prompts/analyst.md
   # etc.
   ```

3. **Study Configuration:**
   ```bash
   # Review agent configs
   cat config/agents.json | python -m json.tool

   # Review tool configs
   cat config/tools.json | python -m json.tool
   ```

4. **Run Examples:**
   ```bash
   # Try different agents
   python scripts/example_usage.py
   ```

### Customize for Your Use Case

1. **Modify Prompts:**
   - Edit `config/prompts/*.md`
   - Adjust for your industry
   - Add your company context

2. **Configure Agents:**
   - Edit `config/agents.json`
   - Adjust temperature, max_tokens
   - Enable/disable capabilities

3. **Add Custom Tools:**
   - Create new tool in `src/core/tools.py`
   - Define in `config/tools.json`
   - Register in ToolRegistry

4. **Create New Agents:**
   - Copy existing agent (e.g., `analyst.py`)
   - Create prompt in `config/prompts/`
   - Add to `config/agents.json`
   - Register in Manager

### Monitor Costs

```bash
# Check daily usage
curl http://localhost:8000/api/v1/usage

# Review token manager stats
python -c "
from src.core.token_manager import get_token_manager
tm = get_token_manager()
print(tm.get_summary())
"

# Monitor logs
tail -f logs/app.log  # If you set up logging to file
```

### Join the Community

- Star the repository on GitHub
- Report issues
- Contribute improvements
- Share your use cases

---

## Useful Commands Reference

```bash
# Virtual Environment
source venv/bin/activate          # Activate
deactivate                        # Deactivate

# Server
python main.py                    # Start server
uvicorn main:app --reload         # Start with auto-reload
uvicorn main:app --port 8001      # Use different port

# Testing
curl http://localhost:8000/health           # Health check
curl http://localhost:8000/api/v1/agents    # List agents
python scripts/example_usage.py             # Run examples

# Git
git status                        # Check status
git pull                          # Update from remote
git checkout -b feature/name      # New branch
git add .                         # Stage changes
git commit -m "message"           # Commit
git push                          # Push to remote

# Docker
docker-compose up                 # Start containers
docker-compose down               # Stop containers
docker-compose logs -f app        # View logs

# Debugging
python -m pdb main.py             # Debug mode
python -i main.py                 # Interactive mode
```

---

## Support

### Getting Help

1. **Check Documentation:**
   - Read docs in `docs/` directory
   - Review `ARCHITECTURE.md`
   - Check `TOOLS_AND_TECHNIQUES.md`

2. **Ask Claude Code:**
   - Open VSCode
   - Press `⌘L`
   - Ask specific questions about the code

3. **Search Issues:**
   - Check GitHub Issues
   - Search closed issues too

4. **Create Issue:**
   - Go to GitHub repository
   - Click "Issues" → "New Issue"
   - Provide details:
     - macOS version
     - Python version
     - Error messages
     - Steps to reproduce

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## Success Checklist

- [ ] Homebrew installed
- [ ] Python 3.11+ installed
- [ ] Git installed
- [ ] VSCode installed
- [ ] Claude Code extension installed
- [ ] Repository cloned
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] `.env` file configured
- [ ] API key added
- [ ] Server starts successfully
- [ ] API responds to requests
- [ ] Can access docs at /docs
- [ ] Example scripts run
- [ ] VSCode opens project
- [ ] Claude Code configured

**If all checked: You're ready to build! 🚀**

---

## Additional Resources

- **Anthropic Documentation**: https://docs.anthropic.com/
- **Claude API Reference**: https://docs.anthropic.com/claude/reference/
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Python Virtual Environments**: https://docs.python.org/3/tutorial/venv.html
- **Git Basics**: https://git-scm.com/doc

---

**Last Updated**: 2025-01-15
**Version**: 1.0.0
