# 🚀 Autonomous AI Team - Cloud Deployment Guide

## Overview
This guide provides comprehensive instructions for deploying your Autonomous AI Dream Team on various cloud platforms **without exposing API keys**. Perfect for testing the entire system remotely on affordable infrastructure.

---

## 🎯 Deployment Goals

✅ Deploy on cheap cloud infrastructure
✅ Keep API keys secure (environment variables)
✅ Test the full system without running locally
✅ Access via web API
✅ Monitor usage and costs

---

## 💰 Cost Comparison

| Platform | Monthly Cost | Setup Time | Best For |
|----------|-------------|------------|----------|
| **Railway** | $5-10 | 5 mins | Fastest, simplest |
| **Render** | $7-15 | 10 mins | Free tier available |
| **DigitalOcean App Platform** | $5-12 | 15 mins | Scalable |
| **Heroku** | $7-25 | 10 mins | Classic, reliable |
| **Fly.io** | $3-10 | 10 mins | Global edge, fast |
| **Google Cloud Run** | $5-15 | 20 mins | Pay-per-use, scalable |
| **AWS Fargate** | $10-20 | 30 mins | Enterprise grade |

**Recommended: Railway or Render** (easiest, cheapest)

---

## 🚂 Option 1: Railway (Recommended - Simplest)

### **Why Railway?**
- ✅ **Easiest deployment** (1-click GitHub integration)
- ✅ **Cheap** ($5/month for 8GB memory, $10/month for 16GB)
- ✅ **Free trial** ($5 credit)
- ✅ **Secure environment variables**
- ✅ **Auto HTTPS**
- ✅ **Simple monitoring**

### **Step-by-Step Deployment**

#### **1. Prepare Your Repository**

Create `railway.json` in project root:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install -r requirements.txt"
  },
  "deploy": {
    "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE"
  }
}
```

Ensure `main.py` supports dynamic port:

```python
import os
from fastapi import FastAPI
import uvicorn

app = FastAPI()

# ... your app code ...

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

#### **2. Deploy to Railway**

1. **Sign up:** https://railway.app (use GitHub account)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose: `avaluev/avaluev.github.io`
5. Set **Root Directory:** `autonomous-ai-team`
6. Click **"Deploy"**

#### **3. Add Environment Variables**

In Railway dashboard:

1. Go to **Variables** tab
2. Add your secrets:

```env
ANTHROPIC_API_KEY=sk-ant-xxxxx
BRAVE_API_KEY=your_brave_key_optional
DEFAULT_MODEL=claude-sonnet-4-5
MAX_TOKENS=4096
TEMPERATURE=0.7
MAX_COST_PER_DAY=50.0
ENVIRONMENT=production
LOG_LEVEL=INFO
```

#### **4. Access Your App**

Railway will generate a URL like:
```
https://autonomous-ai-team-production.up.railway.app
```

Test it:
```bash
curl https://your-app.up.railway.app/health
```

#### **5. Test API**

```bash
curl -X POST "https://your-app.up.railway.app/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Analyze the AI SaaS market and identify top 3 opportunities"
  }'
```

---

## 🎨 Option 2: Render (Free Tier Available)

### **Why Render?**
- ✅ **Free tier** (500 hours/month)
- ✅ **Auto-deploy** from GitHub
- ✅ **Secure env vars**
- ✅ **Auto HTTPS**

### **Step-by-Step Deployment**

#### **1. Create `render.yaml`**

```yaml
services:
  - type: web
    name: autonomous-ai-team
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /health
    envVars:
      - key: ENVIRONMENT
        value: production
      - key: LOG_LEVEL
        value: INFO
```

#### **2. Deploy to Render**

1. **Sign up:** https://render.com (use GitHub)
2. Click **"New +"** → **"Web Service"**
3. Connect GitHub repo: `avaluev/avaluev.github.io`
4. **Root Directory:** `autonomous-ai-team`
5. **Build Command:** `pip install -r requirements.txt`
6. **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
7. Select **Free** or **Starter** plan ($7/month)

#### **3. Add Environment Variables**

In Render dashboard → Environment:

```env
ANTHROPIC_API_KEY=sk-ant-xxxxx
DEFAULT_MODEL=claude-sonnet-4-5
MAX_COST_PER_DAY=50.0
```

#### **4. Access Your App**

Render URL:
```
https://autonomous-ai-team.onrender.com
```

**Note:** Free tier spins down after inactivity (cold start ~30s)

---

## 🌊 Option 3: DigitalOcean App Platform

### **Why DigitalOcean?**
- ✅ **Simple pricing** ($5-12/month)
- ✅ **Predictable costs**
- ✅ **Good docs**
- ✅ **Free static site hosting**

### **Step-by-Step Deployment**

#### **1. Create `.do/app.yaml`**

```yaml
name: autonomous-ai-team
region: nyc

services:
  - name: api
    github:
      repo: avaluev/avaluev.github.io
      branch: master
      deploy_on_push: true
    source_dir: /autonomous-ai-team

    run_command: uvicorn main:app --host 0.0.0.0 --port 8080

    instance_size_slug: basic-xxs  # $5/month
    instance_count: 1

    http_port: 8080

    health_check:
      http_path: /health

    envs:
      - key: ENVIRONMENT
        value: production
      - key: PORT
        value: "8080"
```

#### **2. Deploy**

1. **Sign up:** https://cloud.digitalocean.com
2. Go to **Apps** → **Create App**
3. Connect GitHub: `avaluev/avaluev.github.io`
4. **Source Directory:** `autonomous-ai-team`
5. Choose **Basic** plan ($5/month)
6. Add environment variables (see below)
7. Click **Create Resources**

#### **3. Environment Variables**

```env
ANTHROPIC_API_KEY=sk-ant-xxxxx
DEFAULT_MODEL=claude-sonnet-4-5
MAX_COST_PER_DAY=50.0
PORT=8080
```

#### **4. Access**

DigitalOcean URL:
```
https://autonomous-ai-team-xxxxx.ondigitalocean.app
```

---

## 🦅 Option 4: Heroku (Classic)

### **Why Heroku?**
- ✅ **Most mature** platform
- ✅ **Great docs**
- ✅ **Add-ons ecosystem**
- ⚠️ **No free tier** ($7/month minimum)

### **Step-by-Step Deployment**

#### **1. Create `Procfile`**

```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

#### **2. Create `runtime.txt`**

```
python-3.11.6
```

#### **3. Deploy via Heroku CLI**

```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Create app
cd autonomous-ai-team
heroku create autonomous-ai-team-alex

# Set environment variables
heroku config:set ANTHROPIC_API_KEY=sk-ant-xxxxx
heroku config:set DEFAULT_MODEL=claude-sonnet-4-5
heroku config:set MAX_COST_PER_DAY=50.0
heroku config:set ENVIRONMENT=production

# Push to Heroku
git push heroku master
# OR if in subdirectory:
git subtree push --prefix autonomous-ai-team heroku master

# Open app
heroku open
```

#### **4. Alternative: Heroku GitHub Integration**

1. Go to: https://dashboard.heroku.com
2. **New** → **Create new app**
3. Connect GitHub repo
4. Enable **Automatic Deploys**
5. Add **Config Vars** (environment variables)
6. **Manual Deploy** → **Deploy Branch**

---

## 🪂 Option 5: Fly.io (Global Edge Network)

### **Why Fly.io?**
- ✅ **Cheap** ($3-10/month)
- ✅ **Global edge** deployment
- ✅ **Fast cold starts**
- ✅ **Good free tier** (3 VMs)

### **Step-by-Step Deployment**

#### **1. Install Fly CLI**

```bash
curl -L https://fly.io/install.sh | sh
```

#### **2. Create `fly.toml`**

```toml
app = "autonomous-ai-team"
primary_region = "ewr"  # Newark (or your nearest region)

[build]
  builder = "paketobuildpacks/builder:base"
  buildpacks = ["gcr.io/paketo-buildpacks/python"]

[env]
  PORT = "8080"
  ENVIRONMENT = "production"

[[services]]
  http_checks = []
  internal_port = 8080
  protocol = "tcp"

  [[services.ports]]
    handlers = ["http"]
    port = 80
    force_https = true

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443

  [[services.http_checks]]
    interval = 10000
    timeout = 2000
    path = "/health"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0
```

#### **3. Deploy**

```bash
# Login
flyctl auth login

# Launch app
cd autonomous-ai-team
flyctl launch

# Set secrets
flyctl secrets set ANTHROPIC_API_KEY=sk-ant-xxxxx
flyctl secrets set DEFAULT_MODEL=claude-sonnet-4-5
flyctl secrets set MAX_COST_PER_DAY=50.0

# Deploy
flyctl deploy

# Open
flyctl open
```

---

## ☁️ Option 6: Google Cloud Run (Serverless, Pay-per-use)

### **Why Cloud Run?**
- ✅ **Pay only when used** (scales to zero)
- ✅ **Generous free tier** (2M requests/month)
- ✅ **Fast autoscaling**
- ⚠️ More complex setup

### **Step-by-Step Deployment**

#### **1. Install gcloud CLI**

```bash
# Install gcloud
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Login
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

#### **2. Create Dockerfile** (if not exists)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

#### **3. Deploy to Cloud Run**

```bash
cd autonomous-ai-team

# Build and deploy
gcloud run deploy autonomous-ai-team \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="ENVIRONMENT=production" \
  --set-secrets="ANTHROPIC_API_KEY=projects/YOUR_PROJECT/secrets/anthropic-key:latest"

# OR with direct secrets
gcloud run deploy autonomous-ai-team \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --update-env-vars ANTHROPIC_API_KEY=sk-ant-xxxxx,DEFAULT_MODEL=claude-sonnet-4-5
```

#### **4. Access**

Cloud Run URL:
```
https://autonomous-ai-team-xxxxx-uc.a.run.app
```

---

## 🔒 Security Best Practices

### **1. Never Commit API Keys**

✅ **DO:**
- Use `.env` files (add to `.gitignore`)
- Store secrets in platform's secret manager
- Use environment variables

❌ **DON'T:**
- Commit `.env` files
- Hardcode API keys in code
- Share API keys in public repos

### **2. Verify .gitignore**

```gitignore
# Environment variables
.env
.env.local
.env.production

# API keys
*.key
secrets.json

# Database
*.db
*.sqlite

# Logs
logs/
*.log
```

### **3. Use Secret Managers**

For production, use platform-specific secret managers:

- **Railway:** Built-in encrypted variables
- **Render:** Encrypted environment variables
- **Heroku:** Config Vars (encrypted)
- **GCP:** Secret Manager
- **AWS:** Secrets Manager

### **4. Limit API Key Permissions**

In Anthropic Console:
1. Create separate API keys for different environments
2. Set spending limits per key
3. Monitor usage regularly
4. Rotate keys periodically

---

## 📊 Monitoring & Cost Control

### **1. Set Up Logging**

Add structured logging to `main.py`:

```python
import structlog
import logging

# Configure logging
logging.basicConfig(
    format="%(message)s",
    level=logging.INFO,
)
logger = structlog.get_logger()

@app.post("/api/v1/tasks")
async def create_task(task_request: TaskRequest):
    logger.info("task_started", task=task_request.task)
    # ... your code ...
    logger.info("task_completed", duration=elapsed, tokens=usage)
```

### **2. Monitor API Costs**

Track Claude API usage:

```python
# In your agent code
def log_usage(usage_data):
    logger.info(
        "api_usage",
        input_tokens=usage_data.input_tokens,
        output_tokens=usage_data.output_tokens,
        cost_estimate=calculate_cost(usage_data)
    )

def calculate_cost(usage):
    # Claude Sonnet 4.5 pricing (example)
    input_cost = (usage.input_tokens / 1_000_000) * 3.00  # $3 per M tokens
    output_cost = (usage.output_tokens / 1_000_000) * 15.00  # $15 per M tokens
    return input_cost + output_cost
```

### **3. Set Daily Spending Limits**

In `.env`:
```env
MAX_COST_PER_DAY=50.0
ALERT_THRESHOLD=40.0
```

Implement limit checking:

```python
import datetime
from collections import defaultdict

daily_costs = defaultdict(float)

def check_cost_limit(cost):
    today = datetime.date.today().isoformat()
    daily_costs[today] += cost

    if daily_costs[today] > float(os.getenv("MAX_COST_PER_DAY", 50)):
        raise Exception("Daily cost limit exceeded")

    if daily_costs[today] > float(os.getenv("ALERT_THRESHOLD", 40)):
        logger.warning("approaching_cost_limit", current=daily_costs[today])
```

### **4. Platform-Specific Monitoring**

**Railway:**
- Dashboard shows metrics, logs, costs
- Set up alerts for errors

**Render:**
- Logs tab for application logs
- Metrics tab for CPU/Memory
- Alerts for failures

**Google Cloud:**
- Cloud Logging for structured logs
- Cloud Monitoring for metrics
- Budget alerts

---

## 🧪 Testing Your Deployment

### **1. Health Check**

```bash
curl https://your-app-url.com/health
```

Expected response:
```json
{"status": "healthy"}
```

### **2. List Available Agents**

```bash
curl https://your-app-url.com/api/v1/agents
```

### **3. Submit a Test Task**

```bash
curl -X POST "https://your-app-url.com/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "List your team capabilities",
    "agent": "manager"
  }'
```

### **4. Complex Task Test**

```bash
curl -X POST "https://your-app-url.com/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Analyze the AI coding assistant market. Identify top 3 competitors and their pricing strategies.",
    "context": {
      "budget": "$10,000",
      "timeline": "60 days"
    }
  }'
```

---

## 🎯 Recommended Deployment Strategy

### **For Testing / MVP:**
**Railway** ($5-10/month)
- Easiest setup
- Fast deployments
- Good for prototyping

### **For Production / Scale:**
**Google Cloud Run** ($10-50/month depending on usage)
- Pay only when used
- Auto-scaling
- Enterprise-grade

### **For Budget-Conscious:**
**Render Free Tier** → **Fly.io** ($3-5/month)
- Start free
- Upgrade when needed

---

## 📋 Deployment Checklist

- [ ] Platform account created (Railway/Render/etc.)
- [ ] GitHub repo connected
- [ ] Environment variables configured (ANTHROPIC_API_KEY, etc.)
- [ ] `.env.example` updated with all required vars
- [ ] `.gitignore` excludes `.env` and secrets
- [ ] Health check endpoint working (`/health`)
- [ ] API endpoints tested (`/api/v1/agents`, `/api/v1/tasks`)
- [ ] Logging configured
- [ ] Cost limits set in environment variables
- [ ] Monitoring/alerts configured
- [ ] Domain configured (optional)
- [ ] HTTPS enabled
- [ ] Documentation updated with deployment URL

---

## 🆘 Troubleshooting

### Issue: "Application crashed on startup"
**Solutions:**
- Check logs for errors
- Verify `requirements.txt` is complete
- Ensure port is read from environment: `PORT = os.getenv("PORT", 8000)`
- Check start command is correct

### Issue: "API key not working"
**Solutions:**
- Verify environment variable name matches code
- Check key is not truncated (no spaces, newlines)
- Test key locally first
- Ensure key has sufficient quota/credits

### Issue: "High costs"
**Solutions:**
- Implement request caching
- Reduce `MAX_TOKENS` setting
- Add rate limiting
- Monitor per-request costs
- Use cheaper model for simple tasks (future: Haiku)

### Issue: "Slow response times"
**Solutions:**
- Choose region closer to you
- Enable HTTP/2 and compression
- Implement response streaming
- Cache frequent queries
- Optimize agent prompts for conciseness

---

## 📚 Additional Resources

- **Railway Docs:** https://docs.railway.app/
- **Render Docs:** https://render.com/docs
- **DigitalOcean Docs:** https://docs.digitalocean.com/products/app-platform/
- **Heroku Docs:** https://devcenter.heroku.com/
- **Fly.io Docs:** https://fly.io/docs/
- **Google Cloud Run:** https://cloud.google.com/run/docs
- **Anthropic API Docs:** https://docs.anthropic.com/

---

## 🚀 Next Steps

1. **Choose a platform** (recommended: Railway for simplicity)
2. **Deploy your app** following the guide above
3. **Test the endpoints** with curl or Postman
4. **Monitor costs** for first week
5. **Iterate and improve** based on usage patterns

---

**🎉 Congratulations! Your Autonomous AI Team is now running in the cloud!**

Access your API at: `https://your-deployment-url.com/docs` for interactive API documentation.
