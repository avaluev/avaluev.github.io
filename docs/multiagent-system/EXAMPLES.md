# Multiagent System Examples

Real-world examples demonstrating the desktop multiagent system capabilities.

## Table of Contents

1. [File Management Examples](#file-management-examples)
2. [Data Analysis Examples](#data-analysis-examples)
3. [Automation Examples](#automation-examples)
4. [Development Examples](#development-examples)
5. [Documentation Examples](#documentation-examples)
6. [System Optimization Examples](#system-optimization-examples)
7. [Complex Multi-Agent Examples](#complex-multi-agent-examples)

---

## File Management Examples

### Example 1: Organize Messy Downloads Folder

**Scenario**: Downloads folder has 500+ files of various types accumulated over months

**User Request**:
```
"My Downloads folder is a mess with over 500 files. Please organize them intelligently."
```

**System Response**:

**Claude** invokes `file-system-expert` subagent:

```
Analyzing Downloads folder...

Found:
- 145 PDF documents
- 87 images (JPG, PNG)
- 45 ZIP archives
- 123 miscellaneous files
- 42 duplicate files

Proposing organization strategy:

Downloads/
├── documents/
│   ├── 2024/
│   ├── 2025/
│   └── receipts/
├── images/
│   ├── screenshots/
│   └── photos/
├── archives/
└── software/

Duplicate files:
- report-v1.pdf, report-v2.pdf, report-v3.pdf (keep newest)
- image (1).png through image (15).png (analyzing content...)

Would you like me to proceed with this organization?
```

**After Confirmation**:
```
Organizing files...
✓ Moved 145 documents
✓ Organized 87 images
✓ Archived 45 ZIP files
✓ Removed 42 duplicates (saved 245 MB)
✓ Categorized 123 misc files

Organization complete!

Created: Downloads/organization_report_2025-11-11.md
```

**Generated Report**:
```markdown
# Downloads Organization Report

**Date**: 2025-11-11
**Duration**: 45 seconds

## Summary
- Files processed: 485
- Files moved: 443
- Duplicates removed: 42
- Space saved: 245 MB
- Errors: 0

## New Structure
- documents/: 145 files (523 MB)
- images/: 87 files (156 MB)
- archives/: 45 files (1.2 GB)
- software/: 38 files (890 MB)

## Duplicates Removed
1. report.pdf (kept newest: 2025-11-10)
2. screenshot.png (kept highest resolution)
... (see full list below)
```

---

### Example 2: Find and Merge Similar Photos

**User Request**:
```
"Find similar photos in my Photos library and help me keep only the best versions"
```

**System Response**:

**Claude** uses `screenshot-processor` skill + `file-system-expert` subagent:

```
Scanning ~/Pictures for photos...
Found 1,247 images

Analyzing for similarities...
- Comparing image hashes
- Detecting duplicates
- Grouping similar shots

Found 78 sets of similar photos:

Group 1: Beach sunset (12 photos)
  - IMG_5421.jpg (3024x4032, sharp)  ← Best quality
  - IMG_5422.jpg (3024x4032, blurry)
  - IMG_5423.jpg (2048x1536, cropped)
  ...

Group 2: Family dinner (8 photos)
  - DSC_0891.jpg (4032x3024, well-lit)  ← Best quality
  - DSC_0892.jpg (4032x3024, dark)
  ...

Recommendation: Keep 78 best photos, archive 234 similar versions
Space to save: 1.2 GB

Proceed?
```

---

## Data Analysis Examples

### Example 3: Analyze Sales Data CSV

**Scenario**: Monthly sales data needs analysis and reporting

**User Request**:
```
"Analyze sales_2025.csv and create a comprehensive report with insights"
```

**Input File** (`sales_2025.csv`):
```csv
date,product,quantity,price,region
2025-01-01,Widget A,15,29.99,North
2025-01-01,Widget B,23,19.99,South
...
```

**System Response**:

**Claude** invokes `data-analyst` subagent:

```
Loading sales_2025.csv...
✓ Loaded 1,247 sales records

Data Quality Check:
✓ No missing values
✓ No duplicates
✓ Date range: 2025-01-01 to 2025-10-31
⚠ Found 3 outliers in quantity (investigating...)

Performing analysis...

Key Insights:
1. Total Revenue: $124,567
2. Best Selling Product: Widget A (45% of revenue)
3. Top Region: North (52% of sales)
4. Average Order Value: $99.81
5. Growth Trend: +15% month-over-month

Generating visualizations data...
Creating comprehensive report...

Report created: sales_analysis_2025-11-11.md
```

**Generated Report**:
```markdown
# Sales Analysis Report
**Period**: January - October 2025
**Generated**: 2025-11-11 14:30:00

## Executive Summary
Total revenue of $124,567 from 1,247 transactions shows strong
15% month-over-month growth. Widget A dominates with 45% revenue share.
North region leads with 52% of sales volume.

## Revenue Analysis

### Total Revenue: $124,567
- Month-over-month growth: +15%
- Average order value: $99.81
- Median order value: $75.50

### Revenue by Product
| Product | Revenue | % of Total | Units Sold |
|---------|---------|------------|------------|
| Widget A | $56,055 | 45% | 1,870 |
| Widget B | $37,370 | 30% | 1,870 |
| Widget C | $31,142 | 25% | 1,247 |

### Revenue by Region
| Region | Revenue | % of Total | Avg Order |
|--------|---------|------------|-----------|
| North | $64,775 | 52% | $108.42 |
| South | $35,828 | 29% | $95.15 |
| East | $23,964 | 19% | $87.23 |

## Trends

### Monthly Revenue Trend
- January: $10,234 (baseline)
- February: $11,450 (+12%)
- March: $12,875 (+12%)
- April: $14,120 (+10%)
...
- October: $15,890 (+13%)

Consistent growth indicates strong market demand.

### Seasonal Patterns
- Peak months: March, July, October
- Slow months: January, May
- Holiday impact: +25% in December (projected)

## Recommendations

1. **Inventory**: Increase Widget A stock by 20%
2. **Marketing**: Focus on East region (growth opportunity)
3. **Pricing**: Consider premium tier for Widget A
4. **Promotion**: Plan campaigns for slow months

## Data Quality Notes
- 3 outliers detected in quantity (100+ units):
  - 2025-03-15: 145 units (bulk order verified)
  - 2025-07-22: 132 units (corporate order)
  - 2025-09-30: 156 units (special promotion)

All outliers are legitimate transactions.

## Appendix

### Statistical Summary
```
       quantity      price       revenue
count   1247.00    1247.00      1247.00
mean      15.34      28.76        99.81
std        5.67       8.23        45.23
min        1.00      12.99        12.99
25%       11.00      19.99        65.50
50%       15.00      29.99        75.50
75%       19.00      34.99       125.75
max       45.00      49.99       299.95
```

---
*Analysis performed by data-analyst subagent*
*Report generated by document-generator skill*
```

---

### Example 4: Combine Multiple Data Sources

**User Request**:
```
"Combine data from sales.csv, inventory.db, and customer_feedback.json into a unified analysis"
```

**System Response**:

**Claude** uses:
- `local-data-analyzer` skill
- SQLite MCP for database
- `data-analyst` subagent

```
Loading data sources...

1. sales.csv: 1,247 records ✓
2. inventory.db: Connecting via SQLite MCP ✓
   - products table: 156 products
   - stock_levels table: 156 records
3. customer_feedback.json: 342 reviews ✓

Joining datasets...
- Matching sales to inventory by product_id
- Linking feedback to products
- Creating unified view

Analysis complete!

Key Findings:
1. Products with low stock but high sales:
   - Widget A: 15 units left, selling 50/week
   - Widget C: 8 units left, selling 35/week

2. Products with negative feedback:
   - Widget B: 3.2/5 stars, common complaint: "size"
   - Consider product revision

3. Overstock items:
   - Widget D: 450 units, selling 5/week
   - Recommend clearance sale

Generated: integrated_analysis.md
```

---

## Automation Examples

### Example 5: Automate Weekly Reports

**User Request**:
```
"Set up automation to generate weekly sales reports every Monday morning"
```

**System Response**:

**Claude** uses `desktop-automation` subagent + `system-automation` skill:

```
Creating weekly reporting automation...

Components:
1. Data extraction script
2. Analysis engine
3. Report generator
4. Email sender
5. Cron schedule

Created:
- ~/scripts/weekly_report.py
- ~/scripts/send_report.sh
- Cron job: 0 8 * * 1

Script will:
1. Extract data from sales.db
2. Analyze week-over-week changes
3. Generate markdown report
4. Convert to PDF
5. Email to stakeholders
6. Archive in ~/Reports/

Test run?
```

**Script Created**:
```python
#!/usr/bin/env python3
"""Weekly sales report generator"""

import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

def generate_weekly_report():
    """Generate report for past week"""

    # Date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    # Connect to database
    conn = sqlite3.connect(Path.home() / 'data' / 'sales.db')

    # Extract week's data
    query = """
        SELECT *
        FROM sales
        WHERE date BETWEEN ? AND ?
    """
    df = pd.read_sql(query, conn, params=(
        start_date.strftime('%Y-%m-%d'),
        end_date.strftime('%Y-%m-%d')
    ))

    conn.close()

    # Analysis
    total_revenue = df['revenue'].sum()
    total_orders = len(df)
    avg_order = df['revenue'].mean()
    top_products = df.groupby('product')['revenue'].sum().sort_values(ascending=False).head(5)

    # Generate report
    report = f"""# Weekly Sales Report
**Week of**: {start_date.strftime('%B %d')} - {end_date.strftime('%B %d, %Y')}

## Summary
- Total Revenue: ${total_revenue:,.2f}
- Total Orders: {total_orders:,}
- Average Order: ${avg_order:.2f}

## Top Products
{top_products.to_markdown()}

## Week-over-Week
... (calculate trends)

---
*Generated automatically on {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""

    # Save report
    report_dir = Path.home() / 'Reports' / 'Weekly'
    report_dir.mkdir(parents=True, exist_ok=True)

    report_file = report_dir / f"week_{start_date.strftime('%Y-%m-%d')}.md"
    report_file.write_text(report)

    return str(report_file)

if __name__ == '__main__':
    report = generate_weekly_report()
    print(f"Report generated: {report}")
```

---

## Development Examples

### Example 6: Create Full-Stack Project

**User Request**:
```
"Create a new full-stack web application with React frontend and Python backend"
```

**System Response**:

**Claude** uses `code-workspace-manager` skill + `development-assistant`:

```
Creating full-stack project: my-webapp

Setting up structure...

my-webapp/
├── frontend/          (React + TypeScript)
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── tsconfig.json
├── backend/           (FastAPI + Python)
│   ├── src/
│   ├── tests/
│   ├── requirements.txt
│   └── pyproject.toml
├── docker-compose.yml
├── .github/
│   └── workflows/
│       └── ci.yml
└── README.md

Installing dependencies...
✓ Frontend: npm install
✓ Backend: pip install -r requirements.txt

Initializing git...
✓ Git repository created
✓ Initial commit made

Setting up development tools...
✓ ESLint configured
✓ Prettier configured
✓ pytest configured
✓ pre-commit hooks installed

Creating documentation...
✓ README.md
✓ API.md
✓ CONTRIBUTING.md

Project ready!

Next steps:
1. cd my-webapp
2. docker-compose up
3. Open http://localhost:3000

Run 'npm run dev' in frontend for development
Run 'uvicorn src.main:app --reload' in backend
```

---

### Example 7: Code Review and Refactoring

**User Request**:
```
"Review my Python script and suggest improvements"
```

**Input Code**:
```python
def process(data):
    result = []
    for i in range(len(data)):
        if data[i] > 0:
            result.append(data[i] * 2)
    return result
```

**System Response**:

**Claude** uses `development-assistant` subagent:

```
Code Review Results:

## Issues Found

### 1. Inefficient Loop (Medium Priority)
Current:
for i in range(len(data)):
    if data[i] > 0:

Better: Use direct iteration
for item in data:
    if item > 0:

### 2. Not Following PEP 8 (Low Priority)
- Missing docstring
- Function name not descriptive

### 3. Opportunity for List Comprehension (Low Priority)
Can be simplified using list comprehension

## Suggested Refactoring

```python
def double_positive_values(values):
    """Double all positive values in the list.

    Args:
        values: List of numeric values

    Returns:
        List of doubled positive values

    Example:
        >>> double_positive_values([1, -2, 3, -4, 5])
        [2, 6, 10]
    """
    return [value * 2 for value in values if value > 0]
```

## Improvements
✓ 60% more concise
✓ Better performance (list comprehension)
✓ Descriptive name
✓ Complete docstring
✓ Type hints could be added for Python 3.9+

Apply these changes?
```

---

## Documentation Examples

### Example 8: Generate API Documentation

**User Request**:
```
"Generate API documentation from my FastAPI backend"
```

**System Response**:

**Claude** uses `documentation-writer` subagent:

```
Analyzing FastAPI application...

Found:
- 12 endpoints
- 4 data models
- 2 authentication methods

Generating documentation...

Created:
- docs/API.md (Complete API reference)
- docs/AUTHENTICATION.md (Auth guide)
- docs/EXAMPLES.md (Usage examples)
- docs/ERRORS.md (Error codes)

Preview: docs/API.md
```

**Generated Documentation** (excerpt):
```markdown
# API Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication
All endpoints require Bearer token authentication except public endpoints.

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:8000/api/v1/users
```

## Endpoints

### Users

#### GET /users
Retrieve list of users.

**Authentication**: Required
**Permissions**: admin

**Query Parameters**:
- `page` (integer, optional): Page number (default: 1)
- `limit` (integer, optional): Items per page (default: 20, max: 100)
- `search` (string, optional): Search term

**Response**:
```json
{
  "data": [
    {
      "id": 1,
      "email": "user@example.com",
      "name": "John Doe",
      "created_at": "2025-01-01T00:00:00Z"
    }
  ],
  "total": 100,
  "page": 1,
  "pages": 5
}
```

**Example**:
```bash
curl "http://localhost:8000/api/v1/users?page=1&limit=20"
```

**Errors**:
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
...
```

---

## System Optimization Examples

### Example 9: Optimize Slow Python Script

**User Request**:
```
"My data processing script is taking 10 minutes to run. Can you optimize it?"
```

**System Response**:

**Claude** uses `performance-optimizer` subagent:

```
Analyzing script performance...

Running profiler...
✓ Identified bottlenecks

## Performance Analysis

Current execution time: 623 seconds

Bottlenecks found:
1. Database queries in loop (57% of time)
   - Line 45: SELECT in for loop
   - 1,000 queries executed

2. Inefficient data structure (28% of time)
   - Line 78: Using list for lookups
   - O(n) search performed 10,000 times

3. Redundant calculations (12% of time)
   - Line 92: Same calculation repeated
   - Could be cached

## Proposed Optimizations

### 1. Batch Database Queries
```python
# Before (slow)
for item_id in items:
    item = db.execute("SELECT * FROM items WHERE id = ?", (item_id,))

# After (fast)
item_ids = ','.join(str(id) for id in items)
items = db.execute(f"SELECT * FROM items WHERE id IN ({item_ids})")
```

Expected improvement: 55% faster

### 2. Use Set for Lookups
```python
# Before (slow)
if value in my_list:  # O(n)

# After (fast)
if value in my_set:  # O(1)
```

Expected improvement: 25% faster

### 3. Cache Calculations
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def expensive_calculation(value):
    ...
```

Expected improvement: 10% faster

## Estimated Total Improvement
Current: 623 seconds
Optimized: ~80 seconds
**88% faster!**

Apply these optimizations?
```

---

## Complex Multi-Agent Examples

### Example 10: Complete Data Pipeline with Reporting

**User Request**:
```
"Set up a complete system to:
1. Monitor folder for new data files
2. Clean and analyze data
3. Store results in database
4. Generate weekly reports
5. Alert on anomalies"
```

**System Response**:

**Claude** coordinates multiple agents:

```
Creating comprehensive data pipeline...

Components:
1. File Monitor (system-automation)
2. Data Processor (data-analyst)
3. Report Generator (document-generator)
4. Alert System (desktop-automation)

Architecture:

[File Monitor] → [Data Processor] → [Database]
                        ↓
                  [Anomaly Detector]
                        ↓
                  [Alert System]
                        ↓
                [Report Generator]

Setting up components...
```

**Created System**:

1. **File Monitor** (`~/scripts/watch_data.py`)
2. **Data Processor** (`~/scripts/process_data.py`)
3. **Anomaly Detector** (`~/scripts/detect_anomalies.py`)
4. **Report Generator** (`~/scripts/generate_report.py`)
5. **Cron Jobs** for automation

**System Behavior**:
```
[New file detected] → data_20251111.csv
  ↓
[Processing] Cleaning data (removed 3 duplicates, filled 5 nulls)
  ↓
[Analysis] 247 records processed
  ↓
[Anomaly Check] ⚠ Revenue spike detected (+45% from average)
  ↓
[Alert] Desktop notification + Email sent
  ↓
[Database] Stored in analytics.db
  ↓
[Weekly] Report generated on Monday
```

---

## Best Practices Demonstrated

### 1. Let Claude Orchestrate
Don't specify which agent to use - let Claude decide:

**Good**: "Analyze this data and create a report"
**Less Good**: "Use data-analyst to analyze then use document-generator for report"

### 2. Provide Context
Give Claude context for better results:

**Good**: "Analyze sales data focusing on seasonal trends and regional differences"
**Less Good**: "Analyze this file"

### 3. Confirm Before Destructive Operations
Always confirm before:
- Deleting files
- Modifying many files
- Running automated tasks

### 4. Review Generated Code
Always review scripts before running:
- Check paths are correct
- Verify logic makes sense
- Test with small dataset first

---

## Next Steps

- Try these examples in your environment
- Customize for your specific needs
- Create your own workflows
- Share your successes!

## Resources

- [README.md](README.md) - System overview
- [WORKFLOWS.md](WORKFLOWS.md) - Detailed workflows
- [MCP_INTEGRATION.md](MCP_INTEGRATION.md) - MCP setup
