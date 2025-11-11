---
name: system-automation
description: Automate desktop tasks including scheduled jobs, file monitoring, system maintenance, batch operations, and workflow automation. Use when setting up cron jobs, automating repetitive tasks, creating scripts, or managing system processes. Supports bash scripting, Python automation, and system scheduling.
---

# System Automation

Automate repetitive desktop tasks and system operations for improved productivity.

## Core Capabilities

1. **Scheduled Tasks**: Set up cron jobs and scheduled automation
2. **File Monitoring**: Watch directories and respond to file changes
3. **Batch Operations**: Automate bulk file and data processing
4. **System Maintenance**: Automated cleanup and optimization
5. **Workflow Automation**: Chain multiple tasks together
6. **Process Management**: Start, stop, monitor processes

## Instructions

### Automation Workflow

1. **Identify Task**
   - Determine what needs automation
   - Identify triggers and frequency
   - Define success criteria
   - Plan error handling

2. **Design Automation**
   - Break down into steps
   - Choose appropriate tools
   - Plan scheduling
   - Design logging and monitoring

3. **Implement**
   - Write scripts
   - Test thoroughly
   - Set up scheduling
   - Configure error notifications

4. **Monitor and Maintain**
   - Check logs regularly
   - Update as needed
   - Optimize performance
   - Document changes

## Scheduled Tasks (Cron Jobs)

### Cron Syntax

```bash
# ┌───────────── minute (0 - 59)
# │ ┌───────────── hour (0 - 23)
# │ │ ┌───────────── day of month (1 - 31)
# │ │ │ ┌───────────── month (1 - 12)
# │ │ │ │ ┌───────────── day of week (0 - 6) (Sunday to Saturday)
# │ │ │ │ │
# * * * * * command to execute
```

### Common Schedules

```bash
# Every day at 2 AM
0 2 * * * /path/to/script.sh

# Every Monday at 9 AM
0 9 * * 1 /path/to/script.sh

# Every hour
0 * * * * /path/to/script.sh

# Every 15 minutes
*/15 * * * * /path/to/script.sh

# First day of every month
0 0 1 * * /path/to/script.sh

# Weekdays at 6 PM
0 18 * * 1-5 /path/to/script.sh
```

### Managing Cron Jobs

```bash
# List current cron jobs
crontab -l

# Edit cron jobs
crontab -e

# Remove all cron jobs
crontab -r

# View cron logs
grep CRON /var/log/syslog
```

## File Monitoring

### Watch Directory for Changes

```python
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileChangeHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"File created: {event.src_path}")
            self.process_file(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            print(f"File modified: {event.src_path}")
            self.process_file(event.src_path)

    def process_file(self, filepath):
        # Your processing logic here
        print(f"Processing {filepath}")

# Set up monitoring
path = "/path/to/watch"
event_handler = FileChangeHandler()
observer = Observer()
observer.schedule(event_handler, path, recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
```

### Bash File Monitor

```bash
#!/bin/bash

WATCH_DIR="/path/to/watch"
PROCESS_SCRIPT="/path/to/process.sh"

inotifywait -m -e create -e modify --format '%w%f' "$WATCH_DIR" | while read FILE
do
    echo "File changed: $FILE"
    "$PROCESS_SCRIPT" "$FILE"
done
```

## Batch Operations

### Batch File Processing

```python
import os
import shutil
from pathlib import Path

def batch_process_files(source_dir, dest_dir, file_pattern="*.txt"):
    """Process files matching pattern"""
    source_path = Path(source_dir)
    dest_path = Path(dest_dir)
    dest_path.mkdir(parents=True, exist_ok=True)

    processed = 0
    errors = []

    for file in source_path.glob(file_pattern):
        try:
            # Process file (example: copy)
            shutil.copy2(file, dest_path / file.name)
            processed += 1
            print(f"Processed: {file.name}")
        except Exception as e:
            errors.append(f"{file.name}: {str(e)}")
            print(f"Error processing {file.name}: {e}")

    print(f"\nSummary: {processed} files processed, {len(errors)} errors")
    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"  - {error}")

# Usage
batch_process_files("~/Downloads", "~/Documents/processed", "*.pdf")
```

### Parallel Batch Processing

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import time

def process_file(filepath):
    """Process a single file"""
    try:
        # Simulate processing
        time.sleep(0.1)
        return filepath.name, True, None
    except Exception as e:
        return filepath.name, False, str(e)

def batch_process_parallel(source_dir, file_pattern="*", max_workers=4):
    """Process files in parallel"""
    source_path = Path(source_dir)
    files = list(source_path.glob(file_pattern))

    results = {'success': 0, 'failed': 0, 'errors': []}

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_file, f): f for f in files}

        for future in as_completed(futures):
            filename, success, error = future.result()
            if success:
                results['success'] += 1
                print(f"✓ {filename}")
            else:
                results['failed'] += 1
                results['errors'].append(f"{filename}: {error}")
                print(f"✗ {filename}: {error}")

    print(f"\nProcessed {results['success']} files successfully")
    print(f"Failed: {results['failed']}")

    return results

# Usage
batch_process_parallel("~/Documents", "*.txt", max_workers=8)
```

## System Maintenance

### Disk Cleanup Script

```bash
#!/bin/bash

LOG_FILE="$HOME/cleanup.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "Starting system cleanup..."

# Clear old logs
log "Cleaning old logs..."
find /var/log -type f -name "*.log" -mtime +30 -delete

# Clear temporary files
log "Cleaning temporary files..."
rm -rf /tmp/*
rm -rf ~/.cache/thumbnails/*

# Clear package manager cache
log "Cleaning package cache..."
sudo apt-get clean

# Find and report large files
log "Finding large files..."
find ~ -type f -size +100M -exec ls -lh {} \; | awk '{print $9, $5}' >> "$LOG_FILE"

# Clear old downloads
log "Cleaning old downloads..."
find ~/Downloads -type f -mtime +30 -delete

# Optimize databases
log "Optimizing SQLite databases..."
find ~ -name "*.db" -exec sqlite3 {} "VACUUM;" \;

log "Cleanup complete!"

# Show disk usage
df -h | tee -a "$LOG_FILE"
```

### Backup Automation

```python
import os
import shutil
from datetime import datetime
from pathlib import Path
import tarfile

def create_backup(source_dirs, backup_dir, retention_days=30):
    """Create compressed backup of directories"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = Path(backup_dir)
    backup_path.mkdir(parents=True, exist_ok=True)

    backup_file = backup_path / f"backup_{timestamp}.tar.gz"

    print(f"Creating backup: {backup_file}")

    with tarfile.open(backup_file, "w:gz") as tar:
        for source in source_dirs:
            source_path = Path(source).expanduser()
            if source_path.exists():
                print(f"  Adding: {source_path}")
                tar.add(source_path, arcname=source_path.name)

    # Remove old backups
    for old_backup in backup_path.glob("backup_*.tar.gz"):
        age_days = (datetime.now() - datetime.fromtimestamp(
            old_backup.stat().st_mtime
        )).days

        if age_days > retention_days:
            print(f"Removing old backup: {old_backup.name}")
            old_backup.unlink()

    print(f"Backup complete: {backup_file}")
    print(f"Size: {backup_file.stat().st_size / (1024*1024):.2f} MB")

# Usage
create_backup(
    source_dirs=[
        "~/Documents",
        "~/Projects",
        "~/.config"
    ],
    backup_dir="~/Backups",
    retention_days=30
)
```

## Workflow Automation

### Multi-Step Workflow

```python
import subprocess
import sys
from datetime import datetime

class WorkflowStep:
    def __init__(self, name, command=None, function=None):
        self.name = name
        self.command = command
        self.function = function

    def execute(self):
        print(f"\n{'='*60}")
        print(f"Step: {self.name}")
        print(f"{'='*60}")

        try:
            if self.command:
                result = subprocess.run(
                    self.command,
                    shell=True,
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    raise Exception(f"Command failed: {result.stderr}")
                print(result.stdout)
            elif self.function:
                self.function()

            print(f"✓ {self.name} completed successfully")
            return True
        except Exception as e:
            print(f"✗ {self.name} failed: {e}")
            return False

class Workflow:
    def __init__(self, name):
        self.name = name
        self.steps = []
        self.log_file = f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    def add_step(self, step):
        self.steps.append(step)

    def run(self):
        print(f"\n{'#'*60}")
        print(f"Workflow: {self.name}")
        print(f"Started: {datetime.now()}")
        print(f"{'#'*60}")

        for i, step in enumerate(self.steps, 1):
            print(f"\n[{i}/{len(self.steps)}] Running step...")
            if not step.execute():
                print(f"\n✗ Workflow failed at step: {step.name}")
                return False

        print(f"\n{'#'*60}")
        print(f"✓ Workflow completed successfully!")
        print(f"Finished: {datetime.now()}")
        print(f"{'#'*60}")
        return True

# Example workflow
workflow = Workflow("Daily Data Processing")

workflow.add_step(WorkflowStep(
    "Fetch data",
    command="python fetch_data.py"
))

workflow.add_step(WorkflowStep(
    "Process data",
    command="python process_data.py"
))

workflow.add_step(WorkflowStep(
    "Generate report",
    command="python generate_report.py"
))

workflow.add_step(WorkflowStep(
    "Send notification",
    function=lambda: print("Report generated successfully!")
))

# Run workflow
workflow.run()
```

## Process Management

### Process Monitor

```python
import psutil
import time

def monitor_process(process_name, interval=5):
    """Monitor CPU and memory usage of a process"""
    print(f"Monitoring process: {process_name}")
    print("Press Ctrl+C to stop\n")

    while True:
        found = False
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            if process_name.lower() in proc.info['name'].lower():
                found = True
                print(f"PID: {proc.info['pid']}")
                print(f"CPU: {proc.info['cpu_percent']}%")
                print(f"Memory: {proc.info['memory_percent']:.2f}%")
                print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
                print("-" * 40)

        if not found:
            print(f"Process '{process_name}' not found")

        time.sleep(interval)

# Usage
# monitor_process("python", interval=5)
```

### Service Manager

```bash
#!/bin/bash

SERVICE_NAME="myapp"
PID_FILE="/var/run/$SERVICE_NAME.pid"
LOG_FILE="/var/log/$SERVICE_NAME.log"
COMMAND="/path/to/myapp"

start() {
    if [ -f "$PID_FILE" ]; then
        echo "Service already running (PID: $(cat $PID_FILE))"
        return 1
    fi

    echo "Starting $SERVICE_NAME..."
    $COMMAND >> "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    echo "Started with PID: $(cat $PID_FILE)"
}

stop() {
    if [ ! -f "$PID_FILE" ]; then
        echo "Service not running"
        return 1
    fi

    PID=$(cat "$PID_FILE")
    echo "Stopping $SERVICE_NAME (PID: $PID)..."
    kill $PID
    rm "$PID_FILE"
    echo "Stopped"
}

status() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null; then
            echo "Service running (PID: $PID)"
        else
            echo "PID file exists but process not running"
            rm "$PID_FILE"
        fi
    else
        echo "Service not running"
    fi
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        sleep 2
        start
        ;;
    status)
        status
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
esac
```

## Best Practices

1. **Logging**: Always log automation activities
2. **Error Handling**: Handle failures gracefully
3. **Idempotency**: Make scripts safe to run multiple times
4. **Testing**: Test thoroughly before scheduling
5. **Monitoring**: Set up alerts for failures
6. **Documentation**: Document what automation does
7. **Maintenance**: Review and update regularly

## Common Pitfalls

- Not handling errors properly
- Missing absolute paths in cron jobs
- Not setting proper permissions
- Forgetting to redirect output
- Not testing edge cases
- Hardcoding values instead of using variables

## Integration with Other Skills

- Use with **desktop-file-organizer** for automated file management
- Combine with **local-data-analyzer** for automated data processing
- Work with **document-generator** for automated reporting
- Use with **code-workspace-manager** for project automation
