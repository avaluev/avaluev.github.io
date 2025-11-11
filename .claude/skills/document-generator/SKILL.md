---
name: document-generator
description: Generate comprehensive documentation including README files, technical specs, API docs, user guides, and reports. Use when creating documentation, writing guides, generating reports, or documenting code and systems. Supports Markdown, HTML, and PDF formats.
---

# Document Generator

Create professional, comprehensive documentation for projects, APIs, systems, and processes.

## Core Capabilities

1. **README Generation**: Project overviews, setup guides, usage docs
2. **API Documentation**: Endpoint specs, examples, response formats
3. **Technical Specifications**: Architecture, design decisions, requirements
4. **User Guides**: Step-by-step tutorials and how-to guides
5. **Reports**: Analysis reports, status updates, summaries
6. **Code Documentation**: Function docs, module descriptions

## Instructions

### Documentation Workflow

1. **Gather Information**
   - Read relevant code files
   - Analyze project structure
   - Review existing documentation
   - Identify key features and requirements

2. **Plan Document Structure**
   - Define sections and hierarchy
   - Identify required examples
   - Plan diagrams and visuals
   - Determine target audience

3. **Write Content**
   - Create clear, concise sections
   - Add code examples
   - Include practical examples
   - Provide context and rationale

4. **Review and Polish**
   - Check for completeness
   - Verify technical accuracy
   - Ensure consistency
   - Test code examples

## Document Templates

### README Template

```markdown
# Project Name

Brief description of what this project does and who it's for.

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

```bash
# Installation commands
npm install project-name
```

## Quick Start

```javascript
// Basic usage example
const project = require('project-name');
project.doSomething();
```

## Usage

### Basic Example

Explain basic usage with code examples.

### Advanced Example

Show more complex scenarios.

## Configuration

Describe configuration options.

## API Reference

Link to detailed API documentation.

## Contributing

Guidelines for contributors.

## License

License information.
```

### API Documentation Template

```markdown
# API Documentation

## Overview

API description and base URL.

## Authentication

How to authenticate requests.

## Endpoints

### GET /api/resource

Retrieve resources.

**Parameters:**
- `id` (string, optional): Resource ID
- `limit` (number, optional): Number of results

**Response:**
```json
{
  "data": [],
  "total": 0
}
```

**Example:**
```bash
curl -X GET "https://api.example.com/api/resource?limit=10"
```

### POST /api/resource

Create new resource.

**Request Body:**
```json
{
  "name": "string",
  "value": "string"
}
```

**Response:**
```json
{
  "id": "string",
  "created_at": "timestamp"
}
```

## Error Handling

Common error codes and responses.

## Rate Limiting

Rate limit information.
```

### Technical Specification Template

```markdown
# Technical Specification: [Feature Name]

## Overview

High-level description of the feature.

## Goals

- Goal 1
- Goal 2
- Goal 3

## Non-Goals

What this feature will NOT do.

## Background

Context and motivation.

## Design

### Architecture

Describe system architecture.

### Components

#### Component 1
Description and responsibilities.

#### Component 2
Description and responsibilities.

### Data Model

Describe data structures.

### API Design

Proposed API endpoints and interfaces.

### Security Considerations

Security aspects and mitigations.

### Performance Considerations

Performance implications and optimizations.

## Implementation Plan

### Phase 1
- Task 1
- Task 2

### Phase 2
- Task 3
- Task 4

## Testing Strategy

How to test this feature.

## Rollout Plan

How to deploy safely.

## Metrics and Monitoring

What to measure and monitor.

## Open Questions

Unresolved issues and decisions needed.
```

### User Guide Template

```markdown
# User Guide: [Feature Name]

## Introduction

What this guide covers.

## Prerequisites

What users need before starting.

## Step-by-Step Guide

### Step 1: [Action]

Detailed instructions with screenshots.

### Step 2: [Action]

Continue with next steps.

## Common Tasks

### Task 1
How to accomplish common task.

### Task 2
Another common scenario.

## Troubleshooting

### Issue 1
Problem description and solution.

### Issue 2
Another common issue.

## FAQ

**Q: Common question?**
A: Answer with details.

## Additional Resources

- Link to related docs
- External references
```

### Report Template

```markdown
# [Report Title]

**Date:** 2025-11-11
**Author:** [Name]
**Status:** [Draft/Final]

## Executive Summary

Key findings and recommendations in 2-3 paragraphs.

## Background

Context and reason for the report.

## Methodology

How data was collected and analyzed.

## Findings

### Finding 1
Detailed description with data.

### Finding 2
Another key finding.

## Analysis

Interpretation of findings.

## Recommendations

1. Recommendation 1 with rationale
2. Recommendation 2 with rationale

## Conclusion

Summary and next steps.

## Appendix

### Data Tables
Raw data and detailed tables.

### References
Sources and citations.
```

## Best Practices

### Writing Style

1. **Clarity**: Use simple, direct language
2. **Consistency**: Maintain consistent terminology
3. **Examples**: Provide practical, working examples
4. **Context**: Explain why, not just how
5. **Audience**: Write for your target readers

### Structure

1. **Hierarchy**: Use clear heading structure
2. **Sections**: Break content into digestible sections
3. **Navigation**: Include table of contents for long docs
4. **Links**: Link to related documentation
5. **Summary**: Start with overview, end with summary

### Code Examples

```markdown
## Good Example

```python
# Clear, commented example
def calculate_total(items):
    """Calculate total price of items.

    Args:
        items: List of item dictionaries with 'price' key

    Returns:
        Total price as float
    """
    return sum(item['price'] for item in items)

# Usage
items = [{'price': 10.99}, {'price': 5.99}]
total = calculate_total(items)
print(f"Total: ${total:.2f}")
```

Include:
- Comments explaining logic
- Type hints or documentation
- Usage examples
- Expected output
```

### Diagrams and Visuals

```markdown
## Architecture Diagram

```
┌─────────────┐      ┌──────────────┐
│   Client    │─────▶│    API       │
└─────────────┘      └──────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │   Database   │
                     └──────────────┘
```

Use ASCII diagrams for simple visuals.
```

## Document Generation Scripts

### Auto-generate README from Code

```python
import os
import ast

def extract_functions(filepath):
    """Extract function names and docstrings from Python file"""
    with open(filepath, 'r') as f:
        tree = ast.parse(f.read())

    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            docstring = ast.get_docstring(node)
            functions.append({
                'name': node.name,
                'docstring': docstring or 'No description'
            })

    return functions

def generate_api_docs(source_dir):
    """Generate API documentation from Python files"""
    docs = ["# API Documentation\n\n"]

    for filename in os.listdir(source_dir):
        if filename.endswith('.py'):
            filepath = os.path.join(source_dir, filename)
            functions = extract_functions(filepath)

            docs.append(f"## {filename}\n\n")
            for func in functions:
                docs.append(f"### `{func['name']}`\n\n")
                docs.append(f"{func['docstring']}\n\n")

    return ''.join(docs)

# Usage
api_docs = generate_api_docs('./src')
with open('API.md', 'w') as f:
    f.write(api_docs)
```

### Generate Table of Contents

```python
import re

def generate_toc(markdown_file):
    """Generate table of contents from Markdown headings"""
    with open(markdown_file, 'r') as f:
        content = f.read()

    # Find all headings
    headings = re.findall(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE)

    toc = ["## Table of Contents\n\n"]
    for level, title in headings:
        indent = "  " * (len(level) - 1)
        link = title.lower().replace(' ', '-')
        link = re.sub(r'[^\w-]', '', link)
        toc.append(f"{indent}- [{title}](#{link})\n")

    return ''.join(toc)

# Usage
toc = generate_toc('README.md')
print(toc)
```

## Format Conversion

### Markdown to HTML

```python
import markdown

def md_to_html(md_file, html_file):
    """Convert Markdown to HTML"""
    with open(md_file, 'r') as f:
        md_content = f.read()

    html_content = markdown.markdown(
        md_content,
        extensions=['extra', 'codehilite', 'toc']
    )

    # Wrap in HTML template
    full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Documentation</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        code {{ background: #f4f4f4; padding: 2px 5px; }}
        pre {{ background: #f4f4f4; padding: 10px; overflow-x: auto; }}
    </style>
</head>
<body>
{html_content}
</body>
</html>
"""

    with open(html_file, 'w') as f:
        f.write(full_html)

# Usage
md_to_html('README.md', 'README.html')
```

## Quality Checklist

- [ ] Clear title and introduction
- [ ] Table of contents for long documents
- [ ] All code examples tested and working
- [ ] Consistent formatting and style
- [ ] No broken links
- [ ] Proper grammar and spelling
- [ ] Appropriate level of detail
- [ ] Examples for common use cases
- [ ] Troubleshooting section
- [ ] Contact or support information

## Integration with Other Skills

- Use with **code-workspace-manager** to document projects
- Combine with **screenshot-processor** for visual documentation
- Work with **local-data-analyzer** for data-driven reports
- Use with **desktop-file-organizer** to organize documentation files
