"""
Analytics patterns and constants for commit analysis.
"""
from typing import Dict, List, Any
from data.enums.language import COMMENT_PATTERNS, FUNCTION_PATTERNS, CLASS_PATTERNS, IMPORT_PATTERNS, FILE_EXTENSIONS


# Comment symbols for different file types (legacy, now using COMMENT_PATTERNS)
COMMENT_SYMBOLS = {
    # Python
    'py': ['#', '"""', "'''"],
    
    # JavaScript/TypeScript
    'js': ['//', '/*', '*/'],
    'ts': ['//', '/*', '*/'],
    'jsx': ['//', '/*', '*/'],
    'tsx': ['//', '/*', '*/'],
    
    # Java/Kotlin
    'java': ['//', '/*', '*/'],
    'kt': ['//', '/*', '*/'],
    'kts': ['//', '/*', '*/'],
    
    # C/C++
    'c': ['//', '/*', '*/'],
    'cpp': ['//', '/*', '*/'],
    'h': ['//', '/*', '*/'],
    'hpp': ['//', '/*', '*/'],
    
    # Other languages
    'go': ['//', '/*', '*/'],
    'rs': ['//', '/*', '*/'],
    'rb': ['#'],
    'php': ['//', '#', '/*', '*/'],
    'swift': ['//', '/*', '*/'],
    'scala': ['//', '/*', '*/'],
    'hs': ['--', '{-', '-}'],
    'lua': ['--', '--[[', ']]'],
    'pl': ['#'],
    'r': ['#'],
    
    # Scripts
    'sh': ['#'],
    'bash': ['#'],
    'zsh': ['#'],
    'ps1': ['#'],
    
    # Configs
    'dockerfile': ['#'],
    'yaml': ['#'],
    'yml': ['#'],
    'toml': ['#'],
    'ini': ['#', ';'],
    'xml': ['<!--', '-->'],
    'html': ['<!--', '-->'],
    'css': ['/*', '*/'],
    'sql': ['--', '/*', '*/'],
    
    # Other
    'md': ['<!--', '-->'],
    'txt': [],
}


# File patterns for each commit type
COMMIT_TYPE_PATTERNS = {
    "feat": {
        "description": "A new feature",
        "file_patterns": {
            "src/": "Source code files",
            "lib/": "Library files",
            "*.py": "Python files",
            "*.js": "JavaScript files",
            "*.ts": "TypeScript files",
            "*.java": "Java files",
            "*.go": "Go files",
        }
    },
    "fix": {
        "description": "A bug fix",
        "file_patterns": {
            "src/": "Source code files",
            "test/": "Test files",
            "*.py": "Python files",
            "*.js": "JavaScript files",
            "*.ts": "TypeScript files",
            "*.java": "Java files",
            "*.go": "Go files",
        }
    },
    "docs": {
        "description": "Documentation only changes",
        "file_patterns": {
            "docs/": "Documentation directory",
            "*.md": "Markdown files",
            "README*": "README files",
            "*.rst": "reStructuredText files",
            "*.txt": "Text files",
        }
    },
    "style": {
        "description": "Changes that do not affect the meaning of the code",
        "file_patterns": {
            "*.py": "Python files",
            "*.js": "JavaScript files",
            "*.ts": "TypeScript files",
            "*.java": "Java files",
            "*.go": "Go files",
            "*.css": "CSS files",
        }
    },
    "refactor": {
        "description": "A code change that neither fixes a bug nor adds a feature",
        "file_patterns": {
            "src/": "Source code files",
            "lib/": "Library files",
            "*.py": "Python files",
            "*.js": "JavaScript files",
            "*.ts": "TypeScript files",
            "*.java": "Java files",
            "*.go": "Go files",
        }
    },
    "perf": {
        "description": "A code change that improves performance",
        "file_patterns": {
            "src/": "Source code files",
            "lib/": "Library files",
            "*.py": "Python files",
            "*.js": "JavaScript files",
            "*.ts": "TypeScript files",
            "*.java": "Java files",
            "*.go": "Go files",
        }
    },
    "test": {
        "description": "Adding missing tests or correcting existing tests",
        "file_patterns": {
            "test/": "Test directory",
            "tests/": "Tests directory",
            "*_test.py": "Python test files",
            "*_test.go": "Go test files",
            "*.test.js": "JavaScript test files",
            "*.spec.ts": "TypeScript test files",
        }
    },
    "build": {
        "description": "Changes that affect the build system or external dependencies",
        "file_patterns": {
            "Dockerfile*": "Docker files",
            "docker-compose*.yml": "Docker Compose files",
            "*.gradle": "Gradle files",
            "package.json": "Node.js package file",
            "requirements.txt": "Python requirements file",
            "go.mod": "Go module file",
            "Makefile": "Makefile",
        }
    },
    "ci": {
        "description": "Changes to CI configuration files and scripts",
        "file_patterns": {
            ".github/": "GitHub workflows",
            ".gitlab/": "GitLab CI",
            ".travis.yml": "Travis CI",
            "Jenkinsfile": "Jenkins",
            "*.yaml": "YAML config files",
            "*.yml": "YAML config files",
        }
    },
    "chore": {
        "description": "Other changes that don't modify src or test files",
        "file_patterns": {
            ".gitignore": "Git ignore file",
            ".editorconfig": "Editor config",
            ".prettierrc": "Prettier config",
            ".eslintrc": "ESLint config",
            "*.json": "JSON config files",
            "*.yml": "YAML config files",
            "*.yaml": "YAML config files",
        }
    }
}


# Role patterns based on commit types and file patterns
ROLE_PATTERNS = {
    "devops": {
        "commit_types": ["chore", "build", "ci", "deploy"],
        "file_patterns": [
            "Dockerfile*", "docker-compose*.yml", ".github/", ".gitlab/",
            ".travis.yml", "Jenkinsfile", "*.yaml", "*.yml"
        ],
        "description": "DevOps Engineer - focuses on infrastructure and deployment"
    },
    "tester": {
        "commit_types": ["test", "fix"],
        "file_patterns": [
            "test/", "tests/", "*_test.py", "*_test.go",
            "*.test.js", "*.spec.ts", "cypress/", "jest.config.*"
        ],
        "description": "QA Engineer - focuses on testing and bug fixes"
    },
    "frontend": {
        "commit_types": ["feat", "fix", "style", "perf"],
        "file_patterns": [
            "src/", "public/", "*.js", "*.ts", "*.jsx", "*.tsx",
            "*.css", "*.scss", "*.html", "*.vue", "*.svelte"
        ],
        "description": "Frontend Developer - focuses on UI/UX implementation"
    },
    "backend": {
        "commit_types": ["feat", "fix", "refactor", "perf"],
        "file_patterns": [
            "src/", "api/", "*.py", "*.java", "*.go", "*.rb",
            "*.php", "*.cs", "*.rs", "*.ts", "*.js"
        ],
        "description": "Backend Developer - focuses on server-side implementation"
    },
    "documentation": {
        "commit_types": ["docs"],
        "file_patterns": [
            "docs/", "*.md", "README*", "*.rst", "*.txt"
        ],
        "description": "Technical Writer - focuses on documentation"
    }
}


# Conventional commit pattern regex
CONVENTIONAL_COMMIT_PATTERN = r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([a-z0-9-]+\))?: .+$" 