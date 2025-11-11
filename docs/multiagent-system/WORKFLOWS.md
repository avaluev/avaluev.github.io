# Common Workflows

This document provides detailed workflows for common desktop tasks using the multiagent system.

## Table of Contents

1. [Daily Desktop Automation](#daily-desktop-automation)
2. [Data Analysis Workflows](#data-analysis-workflows)
3. [Code Development Workflows](#code-development-workflows)
4. [File Management Workflows](#file-management-workflows)
5. [Documentation Workflows](#documentation-workflows)
6. [System Maintenance Workflows](#system-maintenance-workflows)

---

## Daily Desktop Automation

### Workflow 1: Automated File Organization

**Objective**: Automatically organize downloads and desktop files daily

**Components Used**:
- `desktop-file-organizer` skill
- `desktop-automation` subagent
- Filesystem MCP (optional)

**Steps**:

```
User: "Set up daily automation to organize my Downloads and Desktop"

Claude orchestrates:
1. Analyzes current file distribution
2. Proposes organization strategy
3. Creates organization script
4. Sets up cron job for daily execution
5. Creates logging for tracking
```

**Script Created**:
```bash
#!/bin/bash
# Daily file organization script

LOG_FILE="$HOME/organization.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "Starting daily file organization..."

# Organize Downloads
python3 << 'EOF'
import os
import shutil
from pathlib import Path
from datetime import datetime

downloads = Path.home() / 'Downloads'
organized = Path.home() / 'Documents' / 'Organized'

# File type mappings
categories = {
    'documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.pptx'],
    'images': ['.jpg', '.jpeg', '.png', '.gif', '.svg'],
    'videos': ['.mp4', '.mov', '.avi', '.mkv'],
    'archives': ['.zip', '.tar', '.gz', '.rar'],
    'code': ['.py', '.js', '.java', '.cpp', '.html', '.css']
}

for file in downloads.glob('*'):
    if file.is_file():
        ext = file.suffix.lower()

        # Find category
        category = 'misc'
        for cat, extensions in categories.items():
            if ext in extensions:
                category = cat
                break

        # Create destination directory
        dest_dir = organized / category / datetime.now().strftime('%Y-%m')
        dest_dir.mkdir(parents=True, exist_ok=True)

        # Move file
        dest_file = dest_dir / file.name
        if not dest_file.exists():
            shutil.move(str(file), str(dest_file))
            print(f"Moved {file.name} to {category}")

EOF

log "Organization complete"
```

**Cron Schedule**:
```cron
# Run daily at 11 PM
0 23 * * * /home/user/scripts/organize_files.sh
```

**Benefits**:
- Automatic daily cleanup
- Consistent organization
- Activity logging
- Customizable categories

---

### Workflow 2: Morning Briefing Generation

**Objective**: Generate daily briefing with system status and tasks

**Components Used**:
- `data-analyst` subagent
- `document-generator` skill
- Memory MCP

**Steps**:

```
User: "Create a morning briefing system that summarizes my tasks and system status"

Claude creates:
1. Task aggregation script
2. System status checker
3. Briefing generator
4. Email/display automation
```

**Implementation**:
```python
#!/usr/bin/env python3
"""Morning briefing generator"""

import os
import psutil
from datetime import datetime
from pathlib import Path

def get_system_status():
    """Get system resource status"""
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    return {
        'cpu': f"{cpu_percent}%",
        'memory': f"{memory.percent}%",
        'disk': f"{disk.percent}%"
    }

def get_pending_tasks():
    """Extract TODO items from project files"""
    todos = []
    for file in Path.home().glob('**/*.md'):
        if file.is_file():
            try:
                content = file.read_text()
                for line in content.split('\n'):
                    if 'TODO' in line or '- [ ]' in line:
                        todos.append({
                            'file': file.name,
                            'task': line.strip()
                        })
            except:
                pass
    return todos[:10]  # Top 10

def get_recent_activity():
    """Get recently modified files"""
    recent = []
    for file in Path.home().glob('**/*'):
        if file.is_file():
            try:
                mtime = file.stat().st_mtime
                age = datetime.now().timestamp() - mtime
                if age < 86400:  # Last 24 hours
                    recent.append({
                        'file': file.name,
                        'time': datetime.fromtimestamp(mtime).strftime('%H:%M')
                    })
            except:
                pass
    return sorted(recent, key=lambda x: x['time'], reverse=True)[:5]

def generate_briefing():
    """Generate morning briefing"""
    briefing = f"""
# Morning Briefing - {datetime.now().strftime('%A, %B %d, %Y')}

## System Status
- CPU Usage: {get_system_status()['cpu']}
- Memory Usage: {get_system_status()['memory']}
- Disk Usage: {get_system_status()['disk']}

## Pending Tasks
"""

    todos = get_pending_tasks()
    if todos:
        for todo in todos:
            briefing += f"- [{todo['file']}] {todo['task']}\n"
    else:
        briefing += "- No pending tasks found\n"

    briefing += "\n## Recent Activity\n"
    recent = get_recent_activity()
    if recent:
        for item in recent:
            briefing += f"- {item['time']}: {item['file']}\n"

    briefing += f"\n---\nGenerated at {datetime.now().strftime('%H:%M:%S')}\n"

    return briefing

if __name__ == '__main__':
    briefing = generate_briefing()

    # Save to file
    output = Path.home() / 'Documents' / 'briefings' / f"briefing_{datetime.now().strftime('%Y-%m-%d')}.md"
    output.parent.mkdir(exist_ok=True)
    output.write_text(briefing)

    # Display
    print(briefing)
```

**Schedule**:
```cron
# Run every weekday at 8 AM
0 8 * * 1-5 /home/user/scripts/morning_briefing.py
```

---

## Data Analysis Workflows

### Workflow 3: Automated Data Processing Pipeline

**Objective**: Process CSV files automatically when added to a folder

**Components Used**:
- `local-data-analyzer` skill
- `system-automation` skill
- `document-generator` skill
- SQLite MCP

**Process Flow**:

```
1. Monitor directory for new CSV files
2. Validate and clean data
3. Perform analysis
4. Store results in SQLite
5. Generate report
6. Archive processed file
```

**File Monitor**:
```python
#!/usr/bin/env python3
"""Watch directory for new data files and process them"""

import time
import sys
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pandas as pd
import sqlite3
from datetime import datetime

class DataFileHandler(FileSystemEventHandler):
    def __init__(self, db_path):
        self.db_path = db_path

    def on_created(self, event):
        if event.is_directory:
            return

        filepath = Path(event.src_path)
        if filepath.suffix.lower() == '.csv':
            print(f"New file detected: {filepath.name}")
            self.process_file(filepath)

    def process_file(self, filepath):
        """Process CSV file"""
        try:
            # Load data
            df = pd.read_csv(filepath)
            print(f"Loaded {len(df)} records from {filepath.name}")

            # Clean data
            df = self.clean_data(df)

            # Analyze
            analysis = self.analyze_data(df)

            # Store in database
            self.store_results(filepath.name, analysis)

            # Generate report
            self.generate_report(filepath.name, df, analysis)

            # Archive file
            self.archive_file(filepath)

            print(f"Processing complete for {filepath.name}")

        except Exception as e:
            print(f"Error processing {filepath.name}: {e}")

    def clean_data(self, df):
        """Clean data"""
        # Remove duplicates
        df = df.drop_duplicates()

        # Handle missing values
        numeric_cols = df.select_dtypes(include=['number']).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

        return df

    def analyze_data(self, df):
        """Perform analysis"""
        analysis = {
            'record_count': len(df),
            'column_count': len(df.columns),
            'numeric_summary': df.describe().to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'timestamp': datetime.now().isoformat()
        }
        return analysis

    def store_results(self, filename, analysis):
        """Store results in SQLite"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY,
                filename TEXT,
                record_count INTEGER,
                timestamp TEXT
            )
        ''')

        cursor.execute(
            'INSERT INTO analyses (filename, record_count, timestamp) VALUES (?, ?, ?)',
            (filename, analysis['record_count'], analysis['timestamp'])
        )

        conn.commit()
        conn.close()

    def generate_report(self, filename, df, analysis):
        """Generate analysis report"""
        report = f"""# Data Analysis Report: {filename}

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
- Total Records: {analysis['record_count']:,}
- Total Columns: {analysis['column_count']}

## Data Quality
- Duplicates Removed: {df.duplicated().sum()}
- Missing Values: {sum(analysis['missing_values'].values())}

## Statistical Summary
{df.describe().to_markdown()}

## Column Details
"""
        for col in df.columns:
            report += f"\n### {col}\n"
            report += f"- Type: {df[col].dtype}\n"
            report += f"- Unique Values: {df[col].nunique()}\n"
            report += f"- Missing: {df[col].isnull().sum()}\n"

        # Save report
        report_path = Path.home() / 'Documents' / 'data_reports' / f"{Path(filename).stem}_report.md"
        report_path.parent.mkdir(exist_ok=True)
        report_path.write_text(report)
        print(f"Report saved: {report_path}")

    def archive_file(self, filepath):
        """Move processed file to archive"""
        archive_dir = Path.home() / 'Documents' / 'data_archive'
        archive_dir.mkdir(exist_ok=True)

        archive_path = archive_dir / filepath.name
        filepath.rename(archive_path)

if __name__ == '__main__':
    watch_dir = Path.home() / 'Documents' / 'data_incoming'
    watch_dir.mkdir(exist_ok=True)

    db_path = Path.home() / 'Documents' / 'data_analysis.db'

    event_handler = DataFileHandler(str(db_path))
    observer = Observer()
    observer.schedule(event_handler, str(watch_dir), recursive=False)
    observer.start()

    print(f"Watching {watch_dir} for new CSV files...")
    print("Press Ctrl+C to stop")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
```

---

## Code Development Workflows

### Workflow 4: New Project Setup

**Objective**: Create complete project with best practices

**Components Used**:
- `code-workspace-manager` skill
- `development-assistant` subagent
- `documentation-writer` subagent
- Git MCP

**Command**:
```
User: "Create a new Python data analysis project called 'sales-analytics'"
```

**Process**:
```
1. Create project structure
2. Initialize git repository
3. Set up virtual environment
4. Configure development tools
5. Create initial documentation
6. Set up testing framework
```

**Generated Structure**:
```
sales-analytics/
├── .git/
├── .gitignore
├── README.md
├── requirements.txt
├── setup.py
├── pyproject.toml
├── .env.example
├── src/
│   └── sales_analytics/
│       ├── __init__.py
│       ├── main.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── docs/
│   ├── API.md
│   └── CONTRIBUTING.md
└── scripts/
    ├── setup.sh
    └── run_tests.sh
```

---

### Workflow 5: Code Review and Optimization

**Objective**: Review code quality and optimize performance

**Components Used**:
- `development-assistant` subagent
- `performance-optimizer` subagent
- `documentation-writer` skill

**Command**:
```
User: "Review my Python project and optimize performance"
```

**Process**:
```
1. Code quality analysis
   - Style issues
   - Best practices
   - Security concerns

2. Performance profiling
   - Identify bottlenecks
   - Measure execution time
   - Memory usage analysis

3. Optimization implementation
   - Algorithm improvements
   - Data structure optimization
   - Caching strategies

4. Documentation
   - Document changes
   - Performance benchmarks
   - Maintenance notes
```

---

## File Management Workflows

### Workflow 6: Duplicate File Detection and Cleanup

**Objective**: Find and handle duplicate files across directories

**Components Used**:
- `file-system-expert` subagent
- `desktop-file-organizer` skill
- Filesystem MCP

**Command**:
```
User: "Find and remove duplicate files in my Documents folder"
```

**Process**:
```python
#!/usr/bin/env python3
"""Find and handle duplicate files"""

import hashlib
from pathlib import Path
from collections import defaultdict

def hash_file(filepath):
    """Calculate MD5 hash of file"""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hasher.update(chunk)
    return hasher.hexdigest()

def find_duplicates(directory):
    """Find duplicate files by hash"""
    hashes = defaultdict(list)

    for file in Path(directory).rglob('*'):
        if file.is_file():
            try:
                file_hash = hash_file(file)
                hashes[file_hash].append(file)
            except Exception as e:
                print(f"Error processing {file}: {e}")

    # Return only duplicates
    duplicates = {k: v for k, v in hashes.items() if len(v) > 1}
    return duplicates

def handle_duplicates(duplicates, strategy='keep_newest'):
    """Handle duplicate files based on strategy"""
    report = []

    for file_hash, files in duplicates.items():
        if strategy == 'keep_newest':
            # Sort by modification time
            files = sorted(files, key=lambda f: f.stat().st_mtime, reverse=True)
            keep = files[0]
            remove = files[1:]
        elif strategy == 'keep_largest':
            # Sort by size
            files = sorted(files, key=lambda f: f.stat().st_size, reverse=True)
            keep = files[0]
            remove = files[1:]
        else:
            keep = files[0]
            remove = files[1:]

        report.append({
            'keep': str(keep),
            'remove': [str(f) for f in remove],
            'size_saved': sum(f.stat().st_size for f in remove)
        })

    return report

if __name__ == '__main__':
    docs_dir = Path.home() / 'Documents'

    print(f"Scanning {docs_dir} for duplicates...")
    duplicates = find_duplicates(docs_dir)

    if not duplicates:
        print("No duplicates found!")
    else:
        print(f"\nFound {len(duplicates)} sets of duplicates")

        total_files = sum(len(files) - 1 for files in duplicates.values())
        total_size = sum(
            sum(f.stat().st_size for f in files[1:])
            for files in duplicates.values()
        )

        print(f"Total duplicate files: {total_files}")
        print(f"Total space to save: {total_size / (1024*1024):.2f} MB")

        # Show some examples
        print("\nExamples:")
        for i, (file_hash, files) in enumerate(list(duplicates.items())[:5]):
            print(f"\nSet {i+1}:")
            for f in files:
                print(f"  - {f}")
```

---

## Documentation Workflows

### Workflow 7: API Documentation Generation

**Objective**: Generate comprehensive API documentation from code

**Components Used**:
- `documentation-writer` subagent
- `development-assistant` subagent

**Command**:
```
User: "Generate API documentation for my Python project"
```

**Process**:
```
1. Extract docstrings from code
2. Analyze function signatures
3. Generate markdown documentation
4. Create examples
5. Build navigation
```

---

## System Maintenance Workflows

### Workflow 8: Weekly System Cleanup

**Objective**: Automated weekly system maintenance

**Components Used**:
- `system-automation` skill
- `desktop-automation` subagent
- `performance-optimizer` subagent

**Script**:
```bash
#!/bin/bash
# Weekly system maintenance

LOG_FILE="$HOME/maintenance.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "Starting weekly maintenance..."

# Clear temporary files
log "Cleaning temporary files..."
rm -rf /tmp/*
rm -rf ~/.cache/thumbnails/*

# Clear old logs
log "Rotating logs..."
find /var/log -type f -name "*.log" -mtime +30 -delete

# Update package lists
log "Updating package lists..."
sudo apt-get update

# Clean package cache
log "Cleaning package cache..."
sudo apt-get clean
sudo apt-get autoremove -y

# Find large files
log "Scanning for large files..."
find ~ -type f -size +100M -exec ls -lh {} \; | \
    awk '{print $9, $5}' >> "$LOG_FILE"

# Archive old files
log "Archiving old files..."
ARCHIVE_DIR="$HOME/Archive/$(date +%Y-%m)"
mkdir -p "$ARCHIVE_DIR"

find ~/Documents -type f -mtime +180 -exec mv {} "$ARCHIVE_DIR/" \;

# System status
log "System status:"
df -h | tee -a "$LOG_FILE"

log "Maintenance complete!"
```

**Schedule**:
```cron
# Run every Sunday at 2 AM
0 2 * * 0 /home/user/scripts/weekly_maintenance.sh
```

---

## Composite Workflows

### Workflow 9: Complete Project Lifecycle

**Objective**: From project creation to deployment

**Phases**:

1. **Initialization** (`code-workspace-manager`)
   - Create project structure
   - Set up version control
   - Configure development environment

2. **Development** (`development-assistant`)
   - Write code
   - Create tests
   - Review code quality

3. **Documentation** (`documentation-writer`)
   - Generate API docs
   - Write user guides
   - Create README

4. **Optimization** (`performance-optimizer`)
   - Profile performance
   - Optimize bottlenecks
   - Benchmark improvements

5. **Deployment Prep** (`system-automation`)
   - Create deployment scripts
   - Set up CI/CD
   - Configure monitoring

---

## Integration Patterns

### Pattern 1: Sequential Processing

```
Skill 1 → Skill 2 → Skill 3 → Result
```

**Example**: Data pipeline
```
local-data-analyzer → document-generator → desktop-automation
```

### Pattern 2: Parallel Processing

```
       ┌─ Subagent 1 ─┐
Task ──┤─ Subagent 2 ─├─ Combine → Result
       └─ Subagent 3 ─┘
```

**Example**: Code review
```
development-assistant (code review)
performance-optimizer (performance)
documentation-writer (docs check)
→ Combined report
```

### Pattern 3: Coordinator Pattern

```
Main Claude
    ├─ Delegates to Subagent 1
    ├─ Uses Skill 2
    └─ Coordinates with MCP
    → Final result
```

---

## Tips for Creating Custom Workflows

1. **Start Simple**: Begin with basic automation
2. **Test Incrementally**: Test each step before combining
3. **Add Logging**: Track what happens at each stage
4. **Handle Errors**: Plan for failures
5. **Document**: Write clear documentation
6. **Iterate**: Improve based on usage

---

## Next Steps

- See [EXAMPLES.md](EXAMPLES.md) for more detailed examples
- Check [MCP_INTEGRATION.md](MCP_INTEGRATION.md) for MCP setup
- Review [README.md](README.md) for system overview
