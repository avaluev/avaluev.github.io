---
name: local-data-analyzer
description: Analyze local data files including CSV, JSON, Excel, SQLite databases, and log files. Use when working with data analysis, generating reports, data visualization, or exploring datasets on the local filesystem. Provides statistical analysis, data cleaning, and insight generation.
---

# Local Data Analyzer

Comprehensive data analysis for local files with support for multiple formats and advanced analytics.

## Supported Formats

- **CSV/TSV**: Comma and tab-separated values
- **JSON/JSONL**: JSON objects and JSON lines
- **Excel**: .xlsx and .xls files
- **SQLite**: Local database files
- **Parquet**: Columnar data format
- **Log Files**: Application and system logs
- **XML**: Structured XML data

## Core Capabilities

1. **Data Exploration**: Quick statistical summaries and profiling
2. **Data Cleaning**: Handle missing values, duplicates, outliers
3. **Analysis**: Aggregations, correlations, trend analysis
4. **Visualization**: Generate charts and plots (describe data patterns)
5. **Export**: Convert between formats, create reports

## Instructions

### Data Analysis Workflow

1. **Initial Inspection**
   ```bash
   # For CSV files
   head -n 10 data.csv
   wc -l data.csv

   # For JSON files
   jq '.[0]' data.json
   jq 'length' data.json
   ```

2. **Data Profiling**
   - Count records and columns
   - Identify data types
   - Check for missing values
   - Calculate basic statistics
   - Detect outliers

3. **Analysis**
   - Group and aggregate data
   - Calculate correlations
   - Identify trends and patterns
   - Filter and subset data
   - Join multiple datasets

4. **Report Generation**
   - Summarize key findings
   - Create visualizations (describe patterns)
   - Export processed data
   - Generate documentation

## Common Analysis Tasks

### CSV Analysis with Python
```python
import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('data.csv')

# Basic info
print(df.info())
print(df.describe())
print(df.head())

# Missing values
print(df.isnull().sum())

# Unique values
print(df.nunique())

# Value counts
print(df['column'].value_counts())

# Correlations
print(df.corr())

# Group by analysis
print(df.groupby('category').agg({
    'value': ['mean', 'sum', 'count']
}))
```

### JSON Analysis
```python
import json
from collections import Counter

with open('data.json') as f:
    data = json.load(f)

# Count records
print(f"Total records: {len(data)}")

# Analyze structure
if data:
    print(f"Keys: {data[0].keys()}")

# Count occurrences
field_values = [item['field'] for item in data]
print(Counter(field_values))
```

### SQLite Analysis
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('database.db')

# List tables
tables = pd.read_sql(
    "SELECT name FROM sqlite_master WHERE type='table'",
    conn
)
print(tables)

# Query data
df = pd.read_sql("SELECT * FROM table_name LIMIT 100", conn)
print(df.describe())

conn.close()
```

### Log File Analysis
```bash
# Count log levels
grep -oP '(ERROR|WARN|INFO|DEBUG)' app.log | sort | uniq -c

# Find errors with context
grep -A 3 -B 3 'ERROR' app.log

# Time-based analysis
awk '{print $1, $2}' app.log | sort | uniq -c

# Extract specific patterns
grep -oP 'user_id=\K\d+' app.log | sort | uniq -c
```

## Statistical Analysis

### Descriptive Statistics
- Mean, median, mode
- Standard deviation, variance
- Percentiles and quartiles
- Min, max, range

### Data Quality Checks
- Missing value percentage
- Duplicate detection
- Outlier identification
- Data type validation
- Constraint violations

### Advanced Analysis
- Time series analysis
- Cohort analysis
- A/B test results
- Distribution analysis
- Correlation matrices

## Data Cleaning

### Handle Missing Values
```python
# Remove rows with missing values
df_clean = df.dropna()

# Fill missing values
df['column'] = df['column'].fillna(df['column'].mean())
df['category'] = df['category'].fillna('Unknown')

# Forward fill
df['value'] = df['value'].ffill()
```

### Remove Duplicates
```python
# Find duplicates
duplicates = df[df.duplicated()]
print(f"Found {len(duplicates)} duplicates")

# Remove duplicates
df_clean = df.drop_duplicates()

# Remove duplicates based on specific columns
df_clean = df.drop_duplicates(subset=['id'])
```

### Handle Outliers
```python
# Z-score method
from scipy import stats
z_scores = np.abs(stats.zscore(df['value']))
df_clean = df[z_scores < 3]

# IQR method
Q1 = df['value'].quantile(0.25)
Q3 = df['value'].quantile(0.75)
IQR = Q3 - Q1
df_clean = df[
    (df['value'] >= Q1 - 1.5 * IQR) &
    (df['value'] <= Q3 + 1.5 * IQR)
]
```

## Data Export

### Convert Formats
```python
# CSV to JSON
df = pd.read_csv('data.csv')
df.to_json('data.json', orient='records', indent=2)

# JSON to CSV
df = pd.read_json('data.json')
df.to_csv('data.csv', index=False)

# Excel to CSV
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')
df.to_csv('data.csv', index=False)

# CSV to SQLite
import sqlite3
conn = sqlite3.connect('database.db')
df.to_sql('table_name', conn, if_exists='replace', index=False)
conn.close()
```

## Best Practices

1. **Data Validation**: Always validate data before analysis
2. **Documentation**: Document assumptions and transformations
3. **Reproducibility**: Save analysis scripts for repeatability
4. **Performance**: Use efficient methods for large datasets
5. **Backup**: Keep original data files unchanged

## Common Pitfalls

- Not checking for missing values
- Ignoring data types
- Forgetting to handle duplicates
- Not validating results
- Losing data during transformations

## Integration with Other Skills

- Use with **desktop-file-organizer** to organize data files
- Combine with **document-generator** for analysis reports
- Work with **screenshot-processor** to document visualizations
