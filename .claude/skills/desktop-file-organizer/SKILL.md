---
name: desktop-file-organizer
description: Organize files and directories on the desktop and in project folders. Use when the user mentions organizing files, cleaning up directories, sorting documents, or managing file structures. Handles file categorization, duplicate detection, and intelligent file organization.
---

# Desktop File Organizer

Automatically organize files and directories based on file types, dates, projects, or custom criteria.

## Core Capabilities

1. **Smart File Categorization**: Group files by type, extension, date, or custom rules
2. **Duplicate Detection**: Find and handle duplicate files across directories
3. **Batch Renaming**: Rename multiple files following patterns
4. **Directory Cleanup**: Identify and organize cluttered directories
5. **Archive Management**: Organize old files into dated archives

## Instructions

### File Organization Workflow

1. **Analyze Current Structure**
   - List directory contents with metadata
   - Identify file types and patterns
   - Detect potential duplicates
   - Calculate directory sizes

2. **Plan Organization**
   - Propose categorization strategy
   - Create logical directory structure
   - Define naming conventions
   - Identify files for archiving

3. **Execute Organization**
   - Create necessary directories
   - Move files to appropriate locations
   - Rename files following conventions
   - Update any file references

4. **Verification**
   - Confirm all files moved correctly
   - Verify no files were lost
   - Report organization summary

## Common Organization Patterns

### By File Type
```
organized/
├── documents/
│   ├── pdfs/
│   ├── word/
│   └── spreadsheets/
├── images/
│   ├── screenshots/
│   └── photos/
├── code/
│   ├── python/
│   └── javascript/
└── archives/
```

### By Date
```
organized/
├── 2025/
│   ├── 01-January/
│   └── 02-February/
└── 2024/
    └── 12-December/
```

### By Project
```
projects/
├── project-a/
│   ├── docs/
│   ├── code/
│   └── assets/
└── project-b/
    ├── docs/
    └── data/
```

## Best Practices

1. **Always Confirm**: Ask before moving or deleting files
2. **Backup First**: Suggest creating backups for major reorganizations
3. **Preserve History**: Maintain file modification times
4. **Document Changes**: Create a log of reorganization actions
5. **Handle Conflicts**: Check for naming conflicts before moving files

## Common Commands

### Find large files
```bash
find . -type f -size +100M -exec ls -lh {} \;
```

### Find duplicates by size and name
```bash
find . -type f -exec md5sum {} + | sort | uniq -w32 -dD
```

### Organize by extension
```bash
for file in *.*; do
    ext="${file##*.}"
    mkdir -p "$ext"
    mv "$file" "$ext/"
done
```

### Archive old files
```bash
find . -type f -mtime +365 -exec mv {} archives/$(date -r {} +%Y)/ \;
```

## Error Handling

- Check for sufficient disk space before moving files
- Verify write permissions on target directories
- Handle special characters in filenames
- Preserve file attributes and permissions
- Detect and report broken symlinks

## Integration with Other Skills

- Use with **local-data-analyzer** to analyze file metadata
- Combine with **system-automation** for scheduled cleanup
- Work with **document-generator** to create organization reports
