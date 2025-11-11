# Desktop Multiagent System for Claude Code

A comprehensive multiagent system leveraging Agent Skills, Subagents, and MCP integration for powerful desktop automation and productivity workflows.

## Overview

This system provides a complete framework for desktop computing tasks using Claude Code's advanced agent capabilities. It combines:

- **6 Agent Skills**: Modular capabilities for specific desktop tasks
- **6 Specialized Subagents**: AI agents with focused expertise
- **MCP Integration**: Extended functionality through Model Context Protocol servers
- **Coordinated Workflows**: Skills and subagents working together seamlessly

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Claude Code                              │
│                     (Main Orchestrator)                         │
└──────────────┬──────────────────────────┬───────────────────────┘
               │                          │
               ▼                          ▼
    ┌──────────────────┐      ┌─────────────────────┐
    │  Agent Skills    │      │    Subagents        │
    │  (Capabilities)  │      │  (Specialists)      │
    └──────────────────┘      └─────────────────────┘
               │                          │
               │                          │
               ├──────────────────────────┤
               │                          │
               ▼                          ▼
    ┌──────────────────────────────────────────┐
    │         MCP Servers                      │
    │  (Extended Functionality)                │
    │  • Filesystem • SQLite • Git             │
    │  • Memory • Postgres • Browser           │
    └──────────────────────────────────────────┘
               │
               ▼
    ┌──────────────────────────────────────────┐
    │      Desktop Environment                 │
    │  Files • Databases • Code • System       │
    └──────────────────────────────────────────┘
```

## Components

### Agent Skills

Agent Skills are modular capabilities that Claude can invoke automatically based on context.

| Skill | Purpose | Use Cases |
|-------|---------|-----------|
| **desktop-file-organizer** | File and directory organization | Cleaning up directories, organizing downloads, finding duplicates |
| **local-data-analyzer** | Data analysis for local files | Analyzing CSV/JSON/Excel, generating reports, data cleaning |
| **screenshot-processor** | Screenshot and image processing | OCR text extraction, image comparison, batch processing |
| **document-generator** | Documentation creation | README files, API docs, user guides, technical specs |
| **system-automation** | Task automation | Cron jobs, file monitoring, batch operations, workflows |
| **code-workspace-manager** | Development environment management | Project setup, dependency management, workspace organization |

**Location**: `.claude/skills/`

### Specialized Subagents

Subagents are AI specialists with focused expertise and separate context windows.

| Subagent | Expertise | Tools | Model |
|----------|-----------|-------|-------|
| **desktop-automation** | Automating desktop tasks | Bash, Read, Write, Edit, Glob, Grep | Sonnet |
| **file-system-expert** | File operations | Bash, Read, Write, Edit, Glob, Grep | Sonnet |
| **data-analyst** | Data analysis | Bash, Read, Write, Edit, Glob, Grep | Sonnet |
| **documentation-writer** | Technical writing | Read, Write, Edit, Glob, Grep, Bash | Sonnet |
| **performance-optimizer** | Performance optimization | Bash, Read, Write, Edit, Glob, Grep | Sonnet |
| **development-assistant** | Code development | Read, Write, Edit, Bash, Glob, Grep | Sonnet |

**Location**: `.claude/agents/`

### MCP Integration

Model Context Protocol servers extend functionality with specialized tools.

Recommended MCP servers for desktop use:
- **Filesystem MCP**: Advanced file operations
- **SQLite MCP**: Local database queries
- **Git MCP**: Repository management
- **Memory MCP**: Persistent context
- **Postgres MCP**: PostgreSQL access (optional)
- **Browser MCP**: Web automation (optional)

See [MCP_INTEGRATION.md](MCP_INTEGRATION.md) for detailed setup.

## Quick Start

### 1. Installation

The multiagent system is already set up in this repository. If you're setting it up in a new project:

```bash
# Clone or copy the .claude directory to your project
cp -r .claude ~/your-project/

# Or copy to your user directory for global access
cp -r .claude/skills ~/.claude/
cp -r .claude/agents ~/.claude/
```

### 2. Verify Installation

Ask Claude:
```
What Skills are available?
```

Check subagents:
```
/agents
```

### 3. Install MCP Servers (Optional but Recommended)

```bash
# Install recommended MCP servers
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-sqlite
npm install -g @modelcontextprotocol/server-git
npm install -g @modelcontextprotocol/server-memory
```

Configure in Claude Code settings (see [MCP_INTEGRATION.md](MCP_INTEGRATION.md)).

### 4. Try It Out

```
# File organization
"Organize my Downloads folder by file type"

# Data analysis
"Analyze the sales data in data.csv and create a summary report"

# Automation
"Create a script to backup my Documents folder daily"

# Code development
"Set up a new Python project with tests and documentation"
```

## Usage Examples

### Example 1: Data Analysis Pipeline

**Task**: Analyze local CSV file and generate report

```
User: "Analyze sales_data.csv and create a comprehensive report"

Claude:
1. Invokes `local-data-analyzer` skill
2. Skill reads and analyzes CSV
3. Delegates report creation to `document-generator` skill
4. Both skills coordinate to deliver complete analysis and report
```

**Output**:
- Statistical analysis summary
- Data quality report
- Visualizations (described)
- Formatted markdown report

### Example 2: Project Organization

**Task**: Clean up and organize project files

```
User: "My project directory is messy. Please organize it properly"

Claude:
1. Invokes `file-system-expert` subagent
2. Subagent analyzes current structure
3. Proposes organization strategy
4. After confirmation, reorganizes files
5. Creates organization report
```

**Output**:
- Organized directory structure
- Files categorized by type/purpose
- Summary of changes
- Documentation of new structure

### Example 3: Automated Workflow

**Task**: Set up automated data processing

```
User: "Set up automation to process CSV files from downloads and save reports"

Claude:
1. Invokes `desktop-automation` subagent
2. Uses `system-automation` skill for scripting
3. Creates file monitoring script
4. Sets up cron job for scheduled runs
5. Tests the automation
```

**Output**:
- Monitoring script
- Processing script
- Cron configuration
- Documentation and usage guide

### Example 4: Development Workflow

**Task**: Create new project with complete setup

```
User: "Create a new Node.js TypeScript project with all best practices"

Claude:
1. Invokes `code-workspace-manager` skill
2. Creates project structure
3. Initializes git repository (via Git MCP)
4. Sets up dependencies
5. Configures linting and formatting
6. Uses `documentation-writer` for README
```

**Output**:
- Complete project structure
- Configured development environment
- Git repository initialized
- Comprehensive README
- Setup documentation

## Advanced Usage

### Combining Skills and Subagents

Skills and subagents can work together for complex tasks:

```
User: "Analyze my codebase performance and create an optimization plan"

Claude orchestrates:
1. `performance-optimizer` subagent profiles code
2. `development-assistant` subagent reviews code
3. `document-generator` skill creates optimization plan
4. All components coordinate to deliver comprehensive analysis
```

### Using MCP Tools

With MCP servers configured, skills and subagents gain enhanced capabilities:

```
User: "Find all TODO comments in my git repository and create a task list"

Process:
1. `development-assistant` uses Git MCP to search repository
2. Extracts TODO comments across all branches
3. `document-generator` creates organized task list
4. Memory MCP remembers project context for future sessions
```

### Custom Workflows

Create complex workflows by chaining capabilities:

```
User: "Set up a daily workflow: analyze logs, generate report, and email it"

Claude creates:
1. Log analysis script (data-analyst subagent)
2. Report generator (document-generator skill)
3. Automation script (desktop-automation subagent)
4. Email notification (system-automation skill)
5. Cron schedule for daily execution
```

## Customization

### Adding New Skills

Create a new skill in `.claude/skills/`:

```bash
mkdir -p .claude/skills/my-custom-skill
```

Create `SKILL.md`:
```markdown
---
name: my-custom-skill
description: What this skill does and when to use it
---

# My Custom Skill

Instructions for Claude on how to use this skill...
```

### Adding New Subagents

Create a new subagent in `.claude/agents/`:

```bash
touch .claude/agents/my-custom-agent.md
```

Define the subagent:
```markdown
---
name: my-custom-agent
description: When to use this agent
tools: Read, Write, Bash
model: sonnet
---

# My Custom Agent

You are a specialist in...
```

### Modifying Existing Components

1. Edit skill or subagent markdown files
2. Restart Claude Code to load changes
3. Test with relevant tasks

## Best Practices

### 1. Let Claude Choose

Don't explicitly invoke skills/subagents unless necessary:
- **Good**: "Organize my downloads"
- **Avoid**: "Use the file-organizer skill to organize downloads"

Claude will choose the best approach automatically.

### 2. Provide Context

Give Claude context for better results:
- **Good**: "Analyze sales_data.csv and focus on monthly trends"
- **Avoid**: "Analyze this file"

### 3. Confirm Destructive Operations

Always review before:
- Deleting files
- Modifying many files at once
- Running automated tasks

### 4. Use MCP for Enhanced Capabilities

Install relevant MCP servers for your workflow:
- Data work → SQLite/Postgres MCP
- File work → Filesystem MCP
- Code work → Git MCP

### 5. Iterate and Refine

Start simple and add complexity:
1. Try basic task
2. Refine based on results
3. Add automation as needed
4. Document your workflows

## Troubleshooting

### Skills Not Activating

**Problem**: Claude doesn't use expected skill

**Solutions**:
- Check skill description is specific
- Mention keywords from description
- Verify SKILL.md syntax is correct
- Restart Claude Code

### Subagent Not Available

**Problem**: Subagent not showing in `/agents`

**Solutions**:
- Check markdown frontmatter syntax
- Verify file is in `.claude/agents/`
- Restart Claude Code
- Check for duplicate names

### MCP Tools Not Working

**Problem**: MCP server tools unavailable

**Solutions**:
- Verify MCP server is installed
- Check configuration in settings
- Restart Claude Code
- Test MCP server manually

### Performance Issues

**Problem**: Slow responses or timeouts

**Solutions**:
- Disable unused MCP servers
- Reduce concurrent operations
- Check system resources
- Optimize skill/subagent prompts

## Performance Considerations

### Resource Usage

- **Skills**: Minimal overhead, part of main context
- **Subagents**: Separate context, some latency for initialization
- **MCP Servers**: External processes, monitor resource usage

### Optimization Tips

1. **Use Skills for Quick Tasks**: Skills have less overhead
2. **Use Subagents for Complex Work**: Better for focused, multi-step tasks
3. **Limit MCP Servers**: Only enable what you need
4. **Monitor Context Size**: Keep prompts concise

## System Requirements

- **Claude Code**: Version 1.0 or later
- **Node.js**: v18+ (for MCP servers)
- **Operating System**: Linux, macOS, Windows
- **Disk Space**: ~500MB for MCP servers
- **Memory**: 2GB+ recommended

## File Structure

```
avaluev.github.io/
├── .claude/
│   ├── skills/
│   │   ├── desktop-file-organizer/
│   │   │   └── SKILL.md
│   │   ├── local-data-analyzer/
│   │   │   └── SKILL.md
│   │   ├── screenshot-processor/
│   │   │   └── SKILL.md
│   │   ├── document-generator/
│   │   │   └── SKILL.md
│   │   ├── system-automation/
│   │   │   └── SKILL.md
│   │   └── code-workspace-manager/
│   │       └── SKILL.md
│   └── agents/
│       ├── desktop-automation.md
│       ├── file-system-expert.md
│       ├── data-analyst.md
│       ├── documentation-writer.md
│       ├── performance-optimizer.md
│       └── development-assistant.md
└── docs/
    └── multiagent-system/
        ├── README.md (this file)
        ├── MCP_INTEGRATION.md
        ├── WORKFLOWS.md
        └── EXAMPLES.md
```

## Contributing

Contributions welcome! To add new skills or subagents:

1. Create new skill/subagent following existing patterns
2. Test thoroughly with various use cases
3. Document usage and examples
4. Submit pull request with description

## License

MIT

## Resources

- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code)
- [Agent Skills Guide](https://docs.claude.com/en/docs/agents-and-tools/agent-skills)
- [Subagents Documentation](https://docs.claude.com/en/docs/claude-code/subagents)
- [MCP Documentation](https://modelcontextprotocol.io/)

## Support

For issues or questions:
- Check [Troubleshooting](#troubleshooting) section
- Review [MCP_INTEGRATION.md](MCP_INTEGRATION.md)
- Check [Examples](EXAMPLES.md) for usage patterns
- Open an issue on GitHub

---

Built with ❤️ using Claude Code's Agent Skills and Subagents
