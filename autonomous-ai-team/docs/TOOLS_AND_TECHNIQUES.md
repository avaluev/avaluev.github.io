# Tools, Techniques, and Approaches Guide

## Table of Contents
1. [Agent Tools Overview](#agent-tools-overview)
2. [Web Search and Research](#web-search-and-research)
3. [Claude Native Features](#claude-native-features)
4. [Model Context Protocol (MCP)](#model-context-protocol-mcp)
5. [Agentic Patterns](#agentic-patterns)
6. [Cost Management](#cost-management)
7. [Safety and Compliance](#safety-and-compliance)

---

## Agent Tools Overview

### Current Tools Implementation

Each agent has access to specialized tools based on their role:

| Tool | Purpose | Agents | Cost | Rate Limit |
|------|---------|--------|------|------------|
| `web_search` | Search the web for information | All | $0.001/call | 10/min |
| `extract_data_from_url` | Parse content from URLs | All | Free | 20/min |
| `store_context` | Save findings for reuse | All | Free | 100/min |
| `retrieve_context` | Get saved context | All | Free | 100/min |
| `call_*_agent` | Invoke specialist agents | Manager only | Variable | N/A |
| `request_human_approval` | High-stakes decisions | Manager only | Free | N/A |

### Business Value by Agent

#### **Analyst Agent Tools**

**Technical Approach:**
- Uses `web_search` to find market data, competitor info, industry reports
- Employs `extract_data_from_url` to parse detailed reports
- Stores findings with `store_context` for other agents

**Business Value:**
- **Market Sizing**: Find TAM/SAM data ($XX billion markets)
- **Competitive Intelligence**: Identify competitors, their pricing, positioning
- **Trend Analysis**: Discover emerging opportunities
- **Customer Insights**: Find pain points from reviews, forums

**Example Workflow:**
```
1. web_search("SaaS productivity tools market size 2024")
2. extract_data_from_url(gartner_report_url)
3. web_search("SaaS productivity tools customer complaints")
4. store_context("market_analysis_2024", findings)
```

#### **Growth Hacker Agent Tools**

**Technical Approach:**
- Researches growth tactics via `web_search`
- Analyzes competitor strategies via `extract_data_from_url`
- References stored market data from Analyst

**Business Value:**
- **Channel Discovery**: Find underutilized acquisition channels
- **Tactic Validation**: Check what worked for similar companies
- **Cost Estimation**: Research typical CAC/LTV for strategies
- **Case Studies**: Learn from success stories

**Example Workflow:**
```
1. retrieve_context("market_analysis_2024")  # From Analyst
2. web_search("SaaS viral referral program case studies")
3. web_search("product hunt launch checklist 2024")
4. store_context("growth_strategies", compiled_tactics)
```

#### **Sales Machine Agent Tools**

**Technical Approach:**
- Analyzes high-converting copy via `web_search` and `extract_data_from_url`
- Studies competitor landing pages
- References market positioning from Analyst

**Business Value:**
- **Conversion Optimization**: Learn from top-performing pages
- **Objection Handling**: Find common objections in reviews
- **Value Prop Research**: See how competitors position
- **Pricing Strategy**: Analyze pricing pages

**Example Workflow:**
```
1. web_search("best SaaS landing pages 2024")
2. extract_data_from_url(competitor_landing_page)
3. web_search("SaaS pricing psychology case studies")
4. Generate copy based on insights
```

#### **System Builder Agent Tools**

**Technical Approach:**
- Researches automation tools via `web_search`
- Studies workflow examples via `extract_data_from_url`
- Documents processes for repeatability

**Business Value:**
- **Tool Discovery**: Find automation platforms (Zapier, Make, n8n)
- **Best Practices**: Learn SOPs from industry leaders
- **Integration Research**: Check API capabilities
- **Cost Analysis**: Compare tool pricing

**Example Workflow:**
```
1. web_search("customer onboarding automation tools")
2. extract_data_from_url(zapier_templates_page)
3. web_search("customer onboarding SOP best practices")
4. Design workflow with researched tools
```

#### **Brand Builder Agent Tools**

**Technical Approach:**
- Researches content strategies via `web_search`
- Analyzes top-performing content via `extract_data_from_url`
- Finds SEO keywords and trends

**Business Value:**
- **Content Ideas**: Find trending topics in niche
- **SEO Research**: Discover high-value keywords
- **Competitor Analysis**: See what content ranks
- **Format Research**: Learn what formats perform best

**Example Workflow:**
```
1. web_search("SaaS content marketing best practices 2024")
2. web_search("project management software blog topics")
3. extract_data_from_url(top_ranking_article)
4. Create content strategy based on gaps
```

---

## Web Search and Research

### Function Calling for Web Search

#### Current Implementation

```python
# Tool definition for Claude
{
  "name": "web_search",
  "description": "Search the web for information...",
  "input_schema": {
    "type": "object",
    "properties": {
      "query": {"type": "string"},
      "num_results": {"type": "integer", "default": 10}
    },
    "required": ["query"]
  }
}
```

#### How Claude Uses It

```python
# Agent makes decision to search
agent_reasoning: "I need market size data"

# Claude function call
{
  "type": "tool_use",
  "name": "web_search",
  "input": {
    "query": "SaaS productivity market size 2024 Gartner",
    "num_results": 5
  }
}

# System executes search
results = brave_search_api(query, num_results)

# Return to Claude
{
  "type": "tool_result",
  "content": [{
    "title": "SaaS Market Report 2024",
    "url": "https://gartner.com/...",
    "snippet": "$50B market growing 25% CAGR..."
  }]
}

# Claude continues with data
```

### Managing Search Depth and Cost

#### Strategy 1: Progressive Refinement

```python
# Start broad, then narrow
class SearchStrategy:
    def progressive_search(self, topic):
        # Phase 1: Overview (1 search)
        overview = web_search(f"{topic} overview 2024", num_results=5)

        # Phase 2: Specific (only if needed)
        if needs_more_detail(overview):
            detailed = web_search(f"{topic} detailed analysis", num_results=3)

        # Phase 3: Validation (only if conflicting)
        if has_conflicts(overview, detailed):
            validation = web_search(f"{topic} statistics report", num_results=2)

        return synthesize(overview, detailed, validation)
```

**Cost**: 1-3 searches vs 10+ searches = **70% cost reduction**

#### Strategy 2: Search Query Optimization

```python
# Bad: Vague queries → irrelevant results → more searches
web_search("productivity tools")  # 1M results, generic

# Good: Specific queries → relevant results → fewer searches
web_search("SaaS productivity tools market size 2024 Gartner IDC")  # Targeted
```

**Guidelines for Query Optimization:**
- Include year: "2024" for current data
- Include sources: "Gartner", "IDC", "Statista"
- Include specifics: "SaaS" not "software"
- Include intent: "market size", "pricing comparison", "case study"

#### Strategy 3: Result Caching

```python
# Cache search results for 24 hours
@cache(ttl=86400)
def cached_web_search(query):
    return web_search(query)

# Reuse results across agents
analyst_searches_market()  # Searches once
growth_hacker_uses_same_data()  # Uses cache, no search
```

**Cost**: Eliminates duplicate searches = **50% cost reduction**

#### Strategy 4: Batch Similar Searches

```python
# Bad: One query at a time
for competitor in competitors:
    web_search(f"{competitor} pricing")  # 10 searches

# Good: Combined query
web_search("SaaS CRM pricing comparison Salesforce HubSpot Pipedrive")  # 1 search
```

### Search Depth Configuration

```json
// config/tools.json
{
  "web_search": {
    "depth_limits": {
      "quick_check": {
        "max_searches": 2,
        "max_results": 5,
        "max_cost": 0.002,
        "use_case": "Quick validation"
      },
      "standard_research": {
        "max_searches": 5,
        "max_results": 10,
        "max_cost": 0.005,
        "use_case": "Normal analysis"
      },
      "deep_research": {
        "max_searches": 10,
        "max_results": 20,
        "max_cost": 0.010,
        "use_case": "Comprehensive research"
      }
    }
  }
}
```

### Search Depth Manager Implementation

```python
class SearchDepthManager:
    """Manage search depth to control costs."""

    def __init__(self, depth_level="standard_research"):
        self.config = load_depth_config(depth_level)
        self.searches_used = 0
        self.cost_spent = 0.0

    def should_allow_search(self) -> tuple[bool, str]:
        """Check if another search is allowed."""
        if self.searches_used >= self.config["max_searches"]:
            return False, "Max searches reached"

        if self.cost_spent >= self.config["max_cost"]:
            return False, "Max cost reached"

        return True, "Search allowed"

    def record_search(self, num_results: int, cost: float):
        """Record a search execution."""
        self.searches_used += 1
        self.cost_spent += cost

        logger.info(
            "search_recorded",
            searches_used=self.searches_used,
            max_searches=self.config["max_searches"],
            cost_spent=self.cost_spent,
            max_cost=self.config["max_cost"]
        )
```

---

## Safety and Compliance

### Avoiding Legal Violations

#### **LinkedIn Scraping - DO NOT DO**

```python
# ❌ NEVER DO THIS
web_search("linkedin.com employees at Microsoft")
extract_data_from_url("https://linkedin.com/company/microsoft/people/")

# Why: Violates LinkedIn ToS, could lead to legal issues
```

**Alternative Approaches:**
```python
# ✅ DO THIS INSTEAD
web_search("Microsoft employee count 2024 official")
web_search("Microsoft organizational structure public data")
extract_data_from_url("microsoft.com/about-us")  # Public info only
```

#### **Data Scraping Best Practices**

**Always Check:**
1. ✅ Public data only (no login required)
2. ✅ Not behind paywall
3. ✅ robots.txt allows access
4. ✅ Terms of Service allow scraping
5. ✅ Reasonable rate limiting (not DDoS)

**Safe Sources:**
- ✅ Company websites (public pages)
- ✅ Press releases
- ✅ Public reports (Gartner, IDC, etc.)
- ✅ News articles
- ✅ Government databases
- ✅ Academic papers

**Risky/Illegal Sources:**
- ❌ Social media profiles (LinkedIn, Facebook)
- ❌ Paywalled content
- ❌ Email addresses without permission
- ❌ Personal information (GDPR violations)
- ❌ Competitor proprietary data

#### **Compliance Checker**

```python
class ComplianceChecker:
    """Check if a URL/search is safe to access."""

    BLOCKED_DOMAINS = [
        "linkedin.com",
        "facebook.com/profile",
        "twitter.com/*/followers"  # Private follower lists
    ]

    ALLOWED_DOMAINS = [
        "linkedin.com/company/*/about",  # Public company pages OK
        "twitter.com/*/status"  # Public tweets OK
    ]

    def is_safe_to_scrape(self, url: str) -> tuple[bool, str]:
        """Check if URL is safe to scrape."""
        # Check blocked domains
        for blocked in self.BLOCKED_DOMAINS:
            if self._matches_pattern(url, blocked):
                return False, f"Blocked domain: {blocked}"

        # Check for personal data indicators
        if self._contains_personal_data_indicators(url):
            return False, "May contain personal data"

        # Check robots.txt (simplified)
        if not self._check_robots_txt(url):
            return False, "robots.txt disallows"

        return True, "Safe to scrape"

    def _contains_personal_data_indicators(self, url: str) -> bool:
        """Check for personal data indicators."""
        indicators = ["email=", "profile=", "user_id=", "/people/"]
        return any(ind in url.lower() for ind in indicators)
```

### Rate Limiting and Throttling

```python
class RateLimiter:
    """Rate limit tool usage to avoid abuse detection."""

    def __init__(self, requests_per_minute=10):
        self.rpm = requests_per_minute
        self.requests = []

    def wait_if_needed(self):
        """Wait if rate limit would be exceeded."""
        now = time.time()

        # Remove requests older than 1 minute
        self.requests = [r for r in self.requests if now - r < 60]

        # If at limit, wait
        if len(self.requests) >= self.rpm:
            wait_time = 60 - (now - self.requests[0])
            logger.warning("rate_limit_waiting", wait_seconds=wait_time)
            time.sleep(wait_time)

        self.requests.append(now)
```

---

## Claude Native Features

### 1. Extended Context (200K tokens)

**What**: Claude Sonnet 4.5 has 200K token context window

**Business Value**:
- Analyze entire documents (50+ page reports)
- Maintain conversation history across complex workflows
- Process multiple competitor websites in one call

**Usage**:
```python
# Load entire market report (30 pages)
report_text = load_pdf("gartner_report.pdf")  # 50K tokens

# Analyze in one call
result = analyst_agent.run(
    task=f"Analyze this report and identify top 3 opportunities:\n\n{report_text}"
)

# No need to chunk or summarize first
```

### 2. Streaming Responses

**What**: Get responses token-by-token as they're generated

**Business Value**:
- Real-time feedback for long tasks
- Better UX (user sees progress)
- Early termination if output goes wrong direction

**Usage**:
```python
# Enable streaming
with client.messages.stream(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    messages=[{"role": "user", "content": task}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
        # User sees output in real-time
```

### 3. Prompt Caching (Coming in Phase 2)

**What**: Cache parts of prompts to reduce costs by up to 90%

**Business Value**:
- **Huge cost savings** on repeated prompts
- Faster response times (cached content processed instantly)
- Enable longer system prompts without cost penalty

**Usage**:
```python
# Mark sections for caching
response = client.messages.create(
    model="claude-sonnet-4-5",
    system=[
        {
            "type": "text",
            "text": LONG_SYSTEM_PROMPT,  # 5K tokens
            "cache_control": {"type": "ephemeral"}  # Cache this!
        }
    ],
    messages=[{"role": "user", "content": "Quick question"}]
)

# First call: 5K input tokens charged
# Next 100 calls: 0 tokens charged for prompt (cache hit!)
# Savings: $0.015 → $0.000 per call (100% savings on prompt)
```

### 4. Function Calling (Tool Use)

**What**: Claude can decide when and how to call tools

**Business Value**:
- Agents autonomous decide what data they need
- No hardcoded workflows
- Natural language → structured tool calls

**Example**:
```python
# Claude decides: "I need market data"
# Automatically generates:
{
  "tool": "web_search",
  "input": {
    "query": "SaaS market size 2024",
    "num_results": 5
  }
}

# No need to tell Claude "search for X" - it figures it out
```

### 5. Vision (Multimodal)

**What**: Claude can analyze images

**Business Value**:
- Analyze competitor websites (screenshots)
- Extract data from infographics
- Process charts and diagrams from reports

**Usage**:
```python
# Analyze competitor landing page
screenshot = capture_screenshot("competitor.com")

response = client.messages.create(
    model="claude-sonnet-4-5",
    messages=[{
        "role": "user",
        "content": [
            {"type": "image", "source": {"type": "base64", "data": screenshot}},
            {"type": "text", "text": "Analyze this landing page design and copy"}
        ]
    }]
)
```

### 6. JSON Mode (Structured Output)

**What**: Force Claude to output valid JSON

**Business Value**:
- Reliable data extraction
- Easy parsing for downstream systems
- No manual JSON cleanup needed

**Usage**:
```python
# System prompt: "Output valid JSON only"
response = analyst_agent.run(
    task="Find top 3 opportunities as JSON",
    context={"output_format": "json"}
)

# Parse response
opportunities = json.loads(response["result"])
# Always valid JSON, no errors
```

---

## Model Context Protocol (MCP)

### What is MCP?

**MCP** = Anthropic's protocol for connecting Claude to external data sources and tools

**Think of it as**: USB for AI - standardized connections

### Available MCP Servers

#### **1. Filesystem MCP**

**What**: Read/write local files

**Business Value**:
- Save research findings to disk
- Load company data from files
- Process bulk data

**Example**:
```python
# Save market analysis
filesystem_server.write_file(
    "research/market_analysis_2024.md",
    analysis_content
)

# Load customer data
customer_data = filesystem_server.read_file("data/customers.csv")
```

#### **2. Database MCP**

**What**: Query databases (PostgreSQL, MySQL, etc.)

**Business Value**:
- Access real customer data
- Query analytics databases
- Update CRM records

**Example**:
```python
# Query customer metrics
results = database_server.query("""
    SELECT
        COUNT(*) as customers,
        AVG(mrr) as avg_mrr
    FROM customers
    WHERE created_at > '2024-01-01'
""")
```

#### **3. Google Drive MCP**

**What**: Access Google Drive files

**Business Value**:
- Read shared market reports
- Access team documents
- Collaborate on findings

#### **4. Slack MCP**

**What**: Post messages, read channels

**Business Value**:
- Notify team of findings
- Monitor customer feedback channels
- Automated reporting

#### **5. GitHub MCP**

**What**: Read code, create PRs

**Business Value**:
- Analyze competitor open source
- Auto-generate documentation
- Code review assistance

### Custom MCP Servers You Can Build

#### **CRM MCP**
```python
# Connect to Salesforce, HubSpot
crm_server = CRMMCPServer(api_key=settings.crm_api_key)

# Query pipeline data
pipeline = crm_server.get_pipeline_metrics()
```

#### **Analytics MCP**
```python
# Connect to Google Analytics, Mixpanel
analytics_server = AnalyticsMCPServer()

# Get conversion data
conversions = analytics_server.get_conversion_rate(
    date_range="last_30_days"
)
```

#### **Custom API MCP**
```python
# Wrap any API as MCP server
class CustomAPIMCP:
    def call_api(self, endpoint, params):
        return requests.get(f"{API_BASE}/{endpoint}", params=params)
```

---

## Agentic Patterns

### Pattern 1: ReAct (Reasoning + Acting)

**What**: Agent reasons about what to do, acts, then reflects

```python
# Analyst Agent using ReAct
thought: "I need market size data"
action: web_search("SaaS market size 2024")
observation: "Found $50B market"

thought: "Need to validate this with another source"
action: web_search("SaaS market size Gartner 2024")
observation: "Gartner confirms $52B"

thought: "Now I have validated data"
final_answer: "Market size is $50-52B"
```

**Business Value**: More reliable, self-correcting agents

### Pattern 2: Chain-of-Thought

**What**: Agent shows its reasoning step-by-step

```python
# Growth Hacker planning strategy
Step 1: Analyze current metrics
Step 2: Identify bottleneck (low activation)
Step 3: Research activation tactics
Step 4: Prioritize by ICE score
Step 5: Create action plan
```

**Business Value**: Explainable decisions, easier debugging

### Pattern 3: Self-Reflection

**What**: Agent critiques its own output

```python
# Sales Machine reviewing its copy
first_draft = generate_landing_page()

reflection: "This copy is too feature-focused, needs more benefits"

improved_draft = revise_copy(first_draft, reflection)

final_check: "Better! Now has clear value prop and CTA"
```

**Business Value**: Higher quality output without human review

### Pattern 4: Multi-Agent Collaboration

**What**: Agents work together, each contributing expertise

```python
# Complex workflow
Manager: "We need a go-to-market plan"
  → Analyst: "Found 3 market opportunities"
  → Growth Hacker: "Designed strategy for opportunity #1"
  → Sales Machine: "Created landing page copy"
  → System Builder: "Documented process"
  → Brand Builder: "Created content calendar"
Manager: "Synthesized into cohesive plan"
```

**Business Value**: Comprehensive solutions, division of labor

### Pattern 5: Hierarchical Planning

**What**: Break complex goals into sub-goals

```python
# Goal: Reach 10,000 customers
└─ Subgoal 1: Find target market
   └─ Task: Market research
└─ Subgoal 2: Design acquisition strategy
   └─ Task: Growth experiments
└─ Subgoal 3: Build assets
   └─ Task: Landing page copy
```

**Business Value**: Structured approach to complex problems

---

## Cost Management

### Cost by Model

| Model | Input (per 1M tokens) | Output (per 1M tokens) | Use Case |
|-------|----------------------|------------------------|----------|
| **Sonnet 4.5** | $3.00 | $15.00 | Complex reasoning, analysis |
| **Haiku 3.5** | $0.25 | $1.25 | Simple tasks, classification |
| **Opus 3** | $15.00 | $75.00 | Ultra-complex (rarely needed) |

### When to Use Each Model

#### Use Sonnet 4.5 (Current Default)
- ✅ Market analysis (complex reasoning)
- ✅ Strategy design (multi-step planning)
- ✅ Copy creation (creative work)
- ✅ Process design (systematic thinking)

#### Use Haiku 3.5 (Phase 2)
- ✅ Classification (is this relevant?)
- ✅ Extraction (pull out key points)
- ✅ Summarization (condense findings)
- ✅ Validation (check format)
- ✅ Routing (which agent?)

**Cost Savings Example:**
```python
# Before (all Sonnet): $0.50 per task
summarize_with_sonnet()  # $0.05
extract_with_sonnet()    # $0.05
classify_with_sonnet()   # $0.05
analyze_with_sonnet()    # $0.35

# After (mixed models): $0.12 per task
summarize_with_haiku()   # $0.002 (25x cheaper!)
extract_with_haiku()     # $0.002 (25x cheaper!)
classify_with_haiku()    # $0.002 (25x cheaper!)
analyze_with_sonnet()    # $0.35

# Savings: 76% cost reduction
```

### Cost Optimization Strategies

#### 1. Prompt Caching (Phase 2)
- Cache system prompts (5K tokens)
- Save $0.015 per call
- 90% cost reduction on repeated calls

#### 2. Model Selection (Phase 2)
- Use Haiku for simple tasks
- 20-25x cheaper
- 80% cost reduction overall

#### 3. Search Optimization
- Targeted queries (fewer searches)
- Result caching (eliminate duplicates)
- 50-70% cost reduction

#### 4. Context Management
- Don't repeat long context unnecessarily
- Summarize history when possible
- 30% cost reduction

**Combined Savings:**
```
Base cost: $50/day

- Prompt caching: -40% = $30/day
- Haiku for simple tasks: -50% = $15/day
- Search optimization: -30% = $10.50/day

Final cost: ~$10-15/day (70-80% savings!)
```

---

## Next Steps

1. **Read this document thoroughly**
2. **Review agent prompts** in `config/prompts/`
3. **Study tool configurations** in `config/tools.json`
4. **Test search strategies** with small budgets first
5. **Monitor costs** using TokenManager
6. **Implement safety checks** for all web access

For Phase 2 implementation (Haiku, caching, etc.), see the implementation files being created next.
