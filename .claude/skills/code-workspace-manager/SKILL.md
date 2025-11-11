---
name: code-workspace-manager
description: Manage code workspaces, development environments, and project setup. Use when setting up new projects, managing dependencies, configuring dev environments, or organizing code repositories. Supports multiple languages and frameworks.
---

# Code Workspace Manager

Efficiently manage development workspaces, environments, and project configurations.

## Core Capabilities

1. **Project Initialization**: Set up new projects with proper structure
2. **Dependency Management**: Manage packages and dependencies
3. **Environment Configuration**: Configure development environments
4. **Workspace Organization**: Organize multi-project workspaces
5. **Tool Integration**: Set up linters, formatters, and dev tools
6. **Version Control**: Git configuration and workflow setup

## Instructions

### Project Setup Workflow

1. **Initialize Project**
   - Create directory structure
   - Initialize version control
   - Set up package management
   - Create basic configuration files

2. **Configure Environment**
   - Set up virtual environments
   - Install dependencies
   - Configure IDE/editor
   - Set up development tools

3. **Organize Workspace**
   - Structure source code
   - Set up test directories
   - Create documentation structure
   - Configure build tools

4. **Verify Setup**
   - Test build process
   - Run initial tests
   - Verify tool integration
   - Document setup process

## Project Templates

### Python Project Structure

```
project-name/
├── .git/
├── .gitignore
├── README.md
├── requirements.txt
├── setup.py
├── pyproject.toml
├── .env.example
├── src/
│   └── project_name/
│       ├── __init__.py
│       ├── main.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── docs/
│   └── README.md
└── scripts/
    └── setup.sh
```

### Node.js Project Structure

```
project-name/
├── .git/
├── .gitignore
├── README.md
├── package.json
├── package-lock.json
├── .env.example
├── .eslintrc.js
├── .prettierrc
├── tsconfig.json
├── src/
│   ├── index.ts
│   ├── types/
│   └── utils/
├── tests/
│   └── index.test.ts
├── dist/
└── docs/
```

### Full-Stack Project Structure

```
project-name/
├── .git/
├── .gitignore
├── README.md
├── docker-compose.yml
├── .env.example
├── frontend/
│   ├── package.json
│   ├── src/
│   ├── public/
│   └── tests/
├── backend/
│   ├── requirements.txt
│   ├── src/
│   ├── tests/
│   └── migrations/
├── database/
│   └── schema.sql
└── docs/
    ├── API.md
    └── SETUP.md
```

## Project Initialization Scripts

### Python Project Setup

```bash
#!/bin/bash

PROJECT_NAME=$1

if [ -z "$PROJECT_NAME" ]; then
    echo "Usage: $0 <project-name>"
    exit 1
fi

echo "Creating Python project: $PROJECT_NAME"

# Create directory structure
mkdir -p "$PROJECT_NAME"/{src/"${PROJECT_NAME//-/_}",tests,docs,scripts}
cd "$PROJECT_NAME"

# Initialize git
git init
echo "*.pyc
__pycache__/
*.egg-info/
dist/
build/
.env
venv/
.pytest_cache/" > .gitignore

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Create requirements.txt
echo "pytest>=7.0.0
pytest-cov>=3.0.0
black>=22.0.0
flake8>=4.0.0
mypy>=0.950" > requirements.txt

# Install dependencies
pip install -r requirements.txt

# Create setup.py
cat > setup.py << EOL
from setuptools import setup, find_packages

setup(
    name="${PROJECT_NAME}",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ]
    },
)
EOL

# Create pyproject.toml
cat > pyproject.toml << EOL
[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[tool.black]
line-length = 88
target-version = ['py39']

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
EOL

# Create basic source file
cat > "src/${PROJECT_NAME//-/_}/__init__.py" << EOL
"""${PROJECT_NAME} package."""

__version__ = "0.1.0"
EOL

cat > "src/${PROJECT_NAME//-/_}/main.py" << EOL
"""Main module for ${PROJECT_NAME}."""

def main():
    """Main entry point."""
    print("Hello from ${PROJECT_NAME}!")

if __name__ == "__main__":
    main()
EOL

# Create basic test
cat > tests/test_main.py << EOL
"""Tests for main module."""

from ${PROJECT_NAME//-/_}.main import main

def test_main():
    """Test main function."""
    # TODO: Add actual tests
    main()
EOL

# Create README
cat > README.md << EOL
# ${PROJECT_NAME}

Project description goes here.

## Installation

\`\`\`bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
pip install -r requirements.txt
\`\`\`

## Usage

\`\`\`python
from ${PROJECT_NAME//-/_}.main import main

main()
\`\`\`

## Development

\`\`\`bash
# Run tests
pytest

# Run with coverage
pytest --cov=${PROJECT_NAME//-/_}

# Format code
black src tests

# Lint code
flake8 src tests
\`\`\`

## License

MIT
EOL

echo "✓ Project created successfully!"
echo ""
echo "Next steps:"
echo "  cd $PROJECT_NAME"
echo "  source venv/bin/activate"
echo "  python -m ${PROJECT_NAME//-/_}.main"
```

### Node.js/TypeScript Project Setup

```bash
#!/bin/bash

PROJECT_NAME=$1

if [ -z "$PROJECT_NAME" ]; then
    echo "Usage: $0 <project-name>"
    exit 1
fi

echo "Creating Node.js/TypeScript project: $PROJECT_NAME"

# Create directory
mkdir -p "$PROJECT_NAME"
cd "$PROJECT_NAME"

# Initialize npm
npm init -y

# Update package.json
node << EOL
const fs = require('fs');
const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));

pkg.main = 'dist/index.js';
pkg.types = 'dist/index.d.ts';
pkg.scripts = {
  "build": "tsc",
  "dev": "ts-node src/index.ts",
  "test": "jest",
  "lint": "eslint src/**/*.ts",
  "format": "prettier --write \"src/**/*.ts\""
};

fs.writeFileSync('package.json', JSON.stringify(pkg, null, 2));
EOL

# Install dependencies
npm install --save-dev \
  typescript \
  @types/node \
  ts-node \
  jest \
  @types/jest \
  ts-jest \
  eslint \
  @typescript-eslint/parser \
  @typescript-eslint/eslint-plugin \
  prettier

# Create tsconfig.json
cat > tsconfig.json << EOL
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
EOL

# Create directory structure
mkdir -p src tests

# Create main file
cat > src/index.ts << EOL
export function main(): void {
  console.log('Hello from $PROJECT_NAME!');
}

if (require.main === module) {
  main();
}
EOL

# Create test file
cat > tests/index.test.ts << EOL
import { main } from '../src/index';

describe('main', () => {
  it('should run without errors', () => {
    expect(() => main()).not.toThrow();
  });
});
EOL

# Create Jest config
cat > jest.config.js << EOL
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/tests'],
  testMatch: ['**/*.test.ts'],
  collectCoverageFrom: ['src/**/*.ts'],
};
EOL

# Create ESLint config
cat > .eslintrc.js << EOL
module.exports = {
  parser: '@typescript-eslint/parser',
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
  ],
  parserOptions: {
    ecmaVersion: 2020,
    sourceType: 'module',
  },
  rules: {
    // Add custom rules here
  },
};
EOL

# Create Prettier config
cat > .prettierrc << EOL
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2
}
EOL

# Create .gitignore
cat > .gitignore << EOL
node_modules/
dist/
*.log
.env
.DS_Store
coverage/
EOL

# Initialize git
git init

# Create README
cat > README.md << EOL
# $PROJECT_NAME

Project description goes here.

## Installation

\`\`\`bash
npm install
\`\`\`

## Usage

\`\`\`typescript
import { main } from '$PROJECT_NAME';

main();
\`\`\`

## Development

\`\`\`bash
# Build
npm run build

# Run in development
npm run dev

# Run tests
npm test

# Lint
npm run lint

# Format
npm run format
\`\`\`

## License

MIT
EOL

echo "✓ Project created successfully!"
echo ""
echo "Next steps:"
echo "  cd $PROJECT_NAME"
echo "  npm install"
echo "  npm run dev"
```

## Dependency Management

### Python Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Freeze dependencies
pip freeze > requirements.txt

# Install in editable mode
pip install -e .

# Update all packages
pip list --outdated
pip install --upgrade package-name
```

### Node.js Dependencies

```bash
# Install dependencies
npm install

# Install specific package
npm install package-name

# Install dev dependency
npm install --save-dev package-name

# Update packages
npm update

# Check for outdated packages
npm outdated

# Audit for security issues
npm audit
npm audit fix
```

## Environment Configuration

### Environment Variables

```bash
# .env.example
DATABASE_URL=postgresql://localhost/dbname
API_KEY=your-api-key-here
DEBUG=true
PORT=3000
```

### Docker Development Environment

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
    depends_on:
      - db
      - redis

  db:
    image: postgres:14
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - db-data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  db-data:
```

## Tool Integration

### VSCode Settings

```json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "typescript.preferences.importModuleSpecifier": "relative"
}
```

### Pre-commit Hooks

```bash
# .git/hooks/pre-commit
#!/bin/bash

echo "Running pre-commit checks..."

# Python
if [ -f "requirements.txt" ]; then
    black --check src tests
    flake8 src tests
    pytest
fi

# Node.js
if [ -f "package.json" ]; then
    npm run lint
    npm run test
fi

echo "✓ All checks passed"
```

## Best Practices

1. **Version Control**: Always use git from the start
2. **Documentation**: Keep README updated
3. **Dependencies**: Pin versions for stability
4. **Environment**: Use .env for configuration
5. **Testing**: Set up tests early
6. **Linting**: Configure linters and formatters
7. **CI/CD**: Set up automated checks

## Integration with Other Skills

- Use with **document-generator** to create project documentation
- Combine with **system-automation** for automated builds
- Work with **desktop-file-organizer** to maintain clean workspace
