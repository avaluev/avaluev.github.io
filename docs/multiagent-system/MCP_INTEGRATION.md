# MCP Integration for Desktop Multiagent System

This guide shows how to integrate Model Context Protocol (MCP) servers with the desktop multiagent system to extend capabilities.

## What is MCP?

The Model Context Protocol (MCP) is a standard for connecting AI applications to various data sources and tools. MCP servers provide additional capabilities that can be used by Claude Code, Agent Skills, and Subagents.

## MCP Servers for Desktop Use Cases

### 1. Filesystem MCP

**Purpose**: Enhanced file system operations beyond basic read/write

**Capabilities**:
- Advanced file search with complex queries
- File metadata management
- Watch directories for changes
- Batch file operations
- Tree view generation

**Installation**:
```bash
npm install -g @modelcontextprotocol/server-filesystem
```

**Configuration** (add to Claude Code settings):
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/user"],
      "env": {}
    }
  }
}
```

**Use with Skills**: The `desktop-file-organizer` skill can leverage filesystem MCP for advanced operations.

**Use with Subagents**: The `file-system-expert` subagent can access filesystem MCP tools.

### 2. SQLite MCP

**Purpose**: Query and manage local SQLite databases

**Capabilities**:
- Execute SQL queries
- List tables and schemas
- Create and modify tables
- Export query results
- Database statistics

**Installation**:
```bash
npm install -g @modelcontextprotocol/server-sqlite
```

**Configuration**:
```json
{
  "mcpServers": {
    "sqlite": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sqlite", "/home/user/databases"],
      "env": {}
    }
  }
}
```

**Use with Skills**: The `local-data-analyzer` skill benefits from direct database access.

**Use with Subagents**: The `data-analyst` subagent can query databases directly.

### 3. Git MCP

**Purpose**: Advanced git operations

**Capabilities**:
- Complex git queries
- Repository analysis
- Commit history exploration
- Branch management
- Diff generation

**Installation**:
```bash
npm install -g @modelcontextprotocol/server-git
```

**Configuration**:
```json
{
  "mcpServers": {
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git"],
      "env": {}
    }
  }
}
```

**Use with Skills**: The `code-workspace-manager` skill uses git MCP for repository operations.

**Use with Subagents**: The `development-assistant` subagent accesses git operations.

### 4. Browser Automation MCP

**Purpose**: Control web browsers for automation and testing

**Capabilities**:
- Launch and control browsers
- Take screenshots of web pages
- Extract data from websites
- Automate web interactions
- Test web applications

**Installation**:
```bash
npm install -g @modelcontextprotocol/server-puppeteer
```

**Configuration**:
```json
{
  "mcpServers": {
    "browser": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-puppeteer"],
      "env": {}
    }
  }
}
```

**Use with Skills**: Can be used with `system-automation` for web-based tasks.

**Use with Subagents**: The `desktop-automation` subagent can automate browser tasks.

### 5. Postgres MCP

**Purpose**: Query and manage PostgreSQL databases

**Capabilities**:
- Execute complex SQL queries
- Manage database schemas
- Export/import data
- Database migrations
- Performance analysis

**Installation**:
```bash
npm install -g @modelcontextprotocol/server-postgres
```

**Configuration**:
```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_URL": "postgresql://user:password@localhost:5432/dbname"
      }
    }
  }
}
```

**Use with Skills**: Extends `local-data-analyzer` capabilities for PostgreSQL.

**Use with Subagents**: The `data-analyst` subagent can analyze PostgreSQL data.

### 6. Memory MCP

**Purpose**: Persistent memory across sessions

**Capabilities**:
- Store information between sessions
- Remember user preferences
- Track project context
- Maintain conversation history
- Store learned patterns

**Installation**:
```bash
npm install -g @modelcontextprotocol/server-memory
```

**Configuration**:
```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"],
      "env": {}
    }
  }
}
```

**Use with All Components**: Memory MCP enhances all skills and subagents with persistent context.

## Complete MCP Configuration Example

Here's a complete configuration file for Claude Code with all recommended desktop MCP servers:

**File**: `~/.config/claude/settings.json`

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/user"],
      "env": {},
      "description": "Enhanced file system operations"
    },
    "sqlite": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-sqlite",
        "/home/user/databases"
      ],
      "env": {},
      "description": "SQLite database access"
    },
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git"],
      "env": {},
      "description": "Advanced git operations"
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"],
      "env": {},
      "description": "Persistent memory across sessions"
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_URL": "postgresql://localhost:5432/mydb"
      },
      "description": "PostgreSQL database access",
      "disabled": true
    },
    "browser": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-puppeteer"],
      "env": {},
      "description": "Browser automation",
      "disabled": true
    }
  }
}
```

## MCP Integration with Skills and Subagents

### Skills with MCP Access

Agent Skills automatically inherit access to all configured MCP tools. When Claude invokes a skill, the skill can use any MCP server tools.

**Example**: The `local-data-analyzer` skill can use:
- Filesystem MCP for finding data files
- SQLite MCP for querying databases
- Memory MCP for remembering analysis preferences

### Subagents with MCP Access

Subagents can access MCP tools based on their configuration. When a subagent is invoked, it inherits MCP tools from the main thread unless restricted.

**Example**: The `data-analyst` subagent with MCP tools:

```markdown
---
name: data-analyst
description: Local data analysis specialist
tools: Bash, Read, Write, Edit, Glob, Grep
# MCP tools are automatically available unless restricted
---
```

To restrict MCP access for a subagent, explicitly list only the tools you want:

```markdown
---
name: restricted-analyst
description: Data analyst with limited tools
tools: Read, Grep
# Only Read and Grep available, no MCP tools
---
```

## MCP Tool Discovery

To see what MCP tools are available:

1. **In Claude Code**: Ask "What MCP servers are connected?"
2. **Check configuration**: Review `~/.config/claude/settings.json`
3. **List tools**: Use `/agents` command to see which tools each subagent can access

## Best Practices

### 1. Install Only Needed MCP Servers

Don't install all MCP servers. Choose based on your use cases:
- **File-heavy work**: Filesystem MCP
- **Data analysis**: SQLite/Postgres MCP
- **Code projects**: Git MCP
- **Web automation**: Browser MCP

### 2. Configure Paths Carefully

```json
{
  "filesystem": {
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/user"],
    // ⚠️ Be specific about allowed directories for security
  }
}
```

### 3. Use Environment Variables

```json
{
  "postgres": {
    "env": {
      "POSTGRES_URL": "${POSTGRES_URL}"
      // Reference environment variable instead of hardcoding
    }
  }
}
```

### 4. Enable/Disable as Needed

```json
{
  "browser": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-puppeteer"],
    "disabled": true  // Disable when not needed
  }
}
```

### 5. Monitor MCP Server Performance

MCP servers add latency. Monitor and optimize:
- Check server startup time
- Monitor memory usage
- Disable unused servers
- Update servers regularly

## Troubleshooting

### MCP Server Not Starting

```bash
# Test MCP server manually
npx -y @modelcontextprotocol/server-filesystem /home/user

# Check Node.js version
node --version  # Should be v18 or higher

# Clear npm cache
npm cache clean --force
```

### MCP Tools Not Appearing

1. Restart Claude Code after configuration changes
2. Check JSON syntax in configuration file
3. Verify MCP server is installed
4. Check server logs

### Permission Issues

```bash
# Ensure paths are accessible
ls -la /home/user/databases

# Check environment variables
echo $POSTGRES_URL
```

## Security Considerations

1. **Limit File System Access**: Only grant access to necessary directories
2. **Secure Database Credentials**: Use environment variables, not hardcoded passwords
3. **Review MCP Code**: MCP servers run with your user permissions
4. **Monitor Activity**: Track what MCP servers are doing
5. **Update Regularly**: Keep MCP servers updated for security patches

## Creating Custom MCP Servers

You can create custom MCP servers for specialized desktop tasks:

```typescript
// custom-desktop-mcp/src/index.ts
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

const server = new Server(
  {
    name: 'custom-desktop-tools',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Define custom tools
server.setRequestHandler('tools/list', async () => ({
  tools: [
    {
      name: 'organize_downloads',
      description: 'Organize files in Downloads folder',
      inputSchema: {
        type: 'object',
        properties: {
          strategy: {
            type: 'string',
            enum: ['by_type', 'by_date', 'by_project'],
          },
        },
      },
    },
  ],
}));

// Implement tool logic
server.setRequestHandler('tools/call', async (request) => {
  if (request.params.name === 'organize_downloads') {
    // Your custom logic here
    return {
      content: [
        {
          type: 'text',
          text: 'Downloads organized successfully',
        },
      ],
    };
  }
});

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

## Integration Examples

### Example 1: Data Analysis Pipeline

```
1. User: "Analyze the sales data in my database"

2. Claude invokes `data-analyst` subagent

3. Subagent uses:
   - SQLite MCP to query database
   - Filesystem MCP to save results
   - Memory MCP to remember preferences

4. Returns comprehensive analysis
```

### Example 2: Project Setup

```
1. User: "Set up a new Python project"

2. Claude invokes `code-workspace-manager` skill

3. Skill uses:
   - Filesystem MCP to create structure
   - Git MCP to initialize repository
   - Memory MCP to remember project preferences

4. Creates complete project structure
```

### Example 3: Automated Reporting

```
1. User: "Generate weekly report from logs"

2. Claude uses `system-automation` skill

3. Skill coordinates:
   - Filesystem MCP to find log files
   - `local-data-analyzer` skill to process logs
   - `document-generator` skill to create report
   - Memory MCP to track report history

4. Generates and saves comprehensive report
```

## Next Steps

1. **Install MCP servers** you need for your use cases
2. **Configure** Claude Code with MCP settings
3. **Test** MCP tools with simple commands
4. **Integrate** with your skills and subagents
5. **Monitor** performance and adjust as needed

## Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [MCP Server Registry](https://github.com/modelcontextprotocol/servers)
- [Creating Custom MCP Servers](https://modelcontextprotocol.io/docs/creating-servers)
- [Claude Code MCP Integration](https://docs.claude.com/en/docs/claude-code/mcp)
