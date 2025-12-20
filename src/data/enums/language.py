"""
Language-specific patterns for code analysis.
"""
from typing import Dict, List, Any


# Comment patterns for different languages
COMMENT_PATTERNS = {
    # Python
    'py': {
        'single_line': ['#'],
        'multi_line_start': ['"""', "'''"],
        'multi_line_end': ['"""', "'''"],
        'docstring_start': ['"""', "'''"],
        'docstring_end': ['"""', "'''"],
        'todo_keywords': ['todo', 'fixme', 'hack', 'note', 'warning', 'important'],
        'api_keywords': ['@param', '@return', '@doc', '@type', '@raises']
    },
    
    # C++
    'cpp': {
        'single_line': ['//'],
        'multi_line_start': ['/*'],
        'multi_line_end': ['*/'],
        'docstring_start': ['/**', '///'],
        'docstring_end': ['*/'],
        'todo_keywords': ['todo', 'fixme', 'hack', 'note', 'warning', 'important'],
        'api_keywords': ['@param', '@return', '@brief', '@details', '@throws']
    },
    
    # Java
    'java': {
        'single_line': ['//'],
        'multi_line_start': ['/*'],
        'multi_line_end': ['*/'],
        'docstring_start': ['/**'],
        'docstring_end': ['*/'],
        'todo_keywords': ['todo', 'fixme', 'hack', 'note', 'warning', 'important'],
        'api_keywords': ['@param', '@return', '@throws', '@deprecated', '@since']
    },
    
    # C
    'c': {
        'single_line': ['//'],
        'multi_line_start': ['/*'],
        'multi_line_end': ['*/'],
        'docstring_start': ['/**'],
        'docstring_end': ['*/'],
        'todo_keywords': ['todo', 'fixme', 'hack', 'note', 'warning', 'important'],
        'api_keywords': ['@param', '@return', '@brief', '@details']
    },
    
    # C#
    'cs': {
        'single_line': ['//'],
        'multi_line_start': ['/*'],
        'multi_line_end': ['*/'],
        'docstring_start': ['///', '/**'],
        'docstring_end': ['*/'],
        'todo_keywords': ['todo', 'fixme', 'hack', 'note', 'warning', 'important'],
        'api_keywords': ['@param', '@return', '@throws', '@exception', '@summary']
    },
    
    # JavaScript
    'js': {
        'single_line': ['//'],
        'multi_line_start': ['/*'],
        'multi_line_end': ['*/'],
        'docstring_start': ['/**'],
        'docstring_end': ['*/'],
        'todo_keywords': ['todo', 'fixme', 'hack', 'note', 'warning', 'important'],
        'api_keywords': ['@param', '@return', '@throws', '@deprecated', '@since']
    },
    
    # SQL
    'sql': {
        'single_line': ['--'],
        'multi_line_start': ['/*'],
        'multi_line_end': ['*/'],
        'docstring_start': ['/*'],
        'docstring_end': ['*/'],
        'todo_keywords': ['todo', 'fixme', 'hack', 'note', 'warning', 'important'],
        'api_keywords': ['@param', '@return', '@description']
    },
    
    # Go
    'go': {
        'single_line': ['//'],
        'multi_line_start': ['/*'],
        'multi_line_end': ['*/'],
        'docstring_start': ['//'],
        'docstring_end': [],
        'todo_keywords': ['todo', 'fixme', 'hack', 'note', 'warning', 'important'],
        'api_keywords': ['@param', '@return', '@throws']
    },
    
    # Rust
    'rs': {
        'single_line': ['//'],
        'multi_line_start': ['/*'],
        'multi_line_end': ['*/'],
        'docstring_start': ['///', '//!'],
        'docstring_end': [],
        'todo_keywords': ['todo', 'fixme', 'hack', 'note', 'warning', 'important'],
        'api_keywords': ['@param', '@return', '@throws', '@deprecated']
    },
    
    # PHP
    'php': {
        'single_line': ['//', '#'],
        'multi_line_start': ['/*'],
        'multi_line_end': ['*/'],
        'docstring_start': ['/**'],
        'docstring_end': ['*/'],
        'todo_keywords': ['todo', 'fixme', 'hack', 'note', 'warning', 'important'],
        'api_keywords': ['@param', '@return', '@throws', '@deprecated', '@since']
    },
    
    # R
    'r': {
        'single_line': ['#'],
        'multi_line_start': [],
        'multi_line_end': [],
        'docstring_start': ['#'],
        'docstring_end': [],
        'todo_keywords': ['todo', 'fixme', 'hack', 'note', 'warning', 'important'],
        'api_keywords': ['@param', '@return', '@description']
    },
    
    # Assembly
    'asm': {
        'single_line': [';', '//', '#'],
        'multi_line_start': ['/*'],
        'multi_line_end': ['*/'],
        'docstring_start': [';', '/*'],
        'docstring_end': ['*/'],
        'todo_keywords': ['todo', 'fixme', 'hack', 'note', 'warning', 'important'],
        'api_keywords': ['@param', '@return', '@description']
    },
    
    # Ruby
    'rb': {
        'single_line': ['#'],
        'multi_line_start': ['=begin'],
        'multi_line_end': ['=end'],
        'docstring_start': ['=begin'],
        'docstring_end': ['=end'],
        'todo_keywords': ['todo', 'fixme', 'hack', 'note', 'warning', 'important'],
        'api_keywords': ['@param', '@return', '@throws', '@deprecated', '@since']
    },
    
    # Kotlin
    'kt': {
        'single_line': ['//'],
        'multi_line_start': ['/*'],
        'multi_line_end': ['*/'],
        'docstring_start': ['/**'],
        'docstring_end': ['*/'],
        'todo_keywords': ['todo', 'fixme', 'hack', 'note', 'warning', 'important'],
        'api_keywords': ['@param', '@return', '@throws', '@deprecated', '@since']
    },
    
    # CSS
    'css': {
        'single_line': ['/*'],
        'multi_line_start': ['/*'],
        'multi_line_end': ['*/'],
        'docstring_start': ['/*'],
        'docstring_end': ['*/'],
        'todo_keywords': ['todo', 'fixme', 'hack', 'note', 'warning', 'important'],
        'api_keywords': ['@param', '@return', '@description']
    }
}


# Function definition patterns
FUNCTION_PATTERNS = {
    'py': [
        r'^\s*def\s+\w+\s*\(',
        r'^\s*async\s+def\s+\w+\s*\(',
        r'^\s*@\w+.*\n\s*def\s+\w+\s*\('
    ],
    'cpp': [
        r'^\s*\w+\s+\w+\s*\([^)]*\)\s*\{?$',
        r'^\s*\w+\s+\w+::\w+\s*\([^)]*\)\s*\{?$',
        r'^\s*template\s*<[^>]*>\s*\w+\s+\w+\s*\([^)]*\)\s*\{?$'
    ],
    'java': [
        r'^\s*(public|private|protected|static|\s) +[\w\<\>\[\]]+\s+\w+\s*\([^)]*\)\s*\{?$',
        r'^\s*@\w+.*\n\s*(public|private|protected|static|\s) +[\w\<\>\[\]]+\s+\w+\s*\([^)]*\)\s*\{?$'
    ],
    'c': [
        r'^\s*\w+\s+\w+\s*\([^)]*\)\s*\{?$',
        r'^\s*static\s+\w+\s+\w+\s*\([^)]*\)\s*\{?$'
    ],
    'cs': [
        r'^\s*(public|private|protected|internal|\s) +[\w\<\>\[\]]+\s+\w+\s*\([^)]*\)\s*\{?$',
        r'^\s*\[.*\]\s*\n\s*(public|private|protected|internal|\s) +[\w\<\>\[\]]+\s+\w+\s*\([^)]*\)\s*\{?$'
    ],
    'js': [
        r'^\s*function\s+\w+\s*\(',
        r'^\s*const\s+\w+\s*=\s*\([^)]*\)\s*=>',
        r'^\s*let\s+\w+\s*=\s*\([^)]*\)\s*=>',
        r'^\s*var\s+\w+\s*=\s*\([^)]*\)\s*=>',
        r'^\s*\w+\s*\([^)]*\)\s*\{'
    ],
    'sql': [
        r'^\s*CREATE\s+(OR\s+REPLACE\s+)?(FUNCTION|PROCEDURE)\s+\w+',
        r'^\s*CREATE\s+(OR\s+REPLACE\s+)?TRIGGER\s+\w+'
    ],
    'go': [
        r'^\s*func\s+\w+\s*\(',
        r'^\s*func\s*\(\s*\w+\s+\w+\s*\)\s+\w+\s*\('
    ],
    'rs': [
        r'^\s*fn\s+\w+\s*\(',
        r'^\s*pub\s+fn\s+\w+\s*\(',
        r'^\s*impl\s+\w+\s*\{'
    ],
    'php': [
        r'^\s*function\s+\w+\s*\(',
        r'^\s*(public|private|protected)\s+function\s+\w+\s*\(',
        r'^\s*static\s+function\s+\w+\s*\('
    ],
    'r': [
        r'^\s*\w+\s*<-\s*function\s*\(',
        r'^\s*function\s*\('
    ],
    'asm': [
        r'^\s*\w+:\s*$',
        r'^\s*\.globl\s+\w+',
        r'^\s*\.type\s+\w+,\s*@function'
    ],
    'rb': [
        r'^\s*def\s+\w+',
        r'^\s*def\s+self\.\w+'
    ],
    'kt': [
        r'^\s*fun\s+\w+\s*\(',
        r'^\s*(public|private|protected|internal)\s+fun\s+\w+\s*\('
    ],
    'css': []  # CSS doesn't have functions in traditional sense
}


# Class definition patterns
CLASS_PATTERNS = {
    'py': [
        r'^\s*class\s+\w+',
        r'^\s*class\s+\w+\s*\([^)]*\):'
    ],
    'cpp': [
        r'^\s*class\s+\w+',
        r'^\s*struct\s+\w+',
        r'^\s*template\s*<[^>]*>\s*class\s+\w+'
    ],
    'java': [
        r'^\s*(public|private|protected)?\s*class\s+\w+',
        r'^\s*(public|private|protected)?\s*interface\s+\w+',
        r'^\s*(public|private|protected)?\s*enum\s+\w+'
    ],
    'c': [
        r'^\s*struct\s+\w+',
        r'^\s*typedef\s+struct\s+\w+'
    ],
    'cs': [
        r'^\s*(public|private|protected|internal)?\s*class\s+\w+',
        r'^\s*(public|private|protected|internal)?\s*interface\s+\w+',
        r'^\s*(public|private|protected|internal)?\s*enum\s+\w+'
    ],
    'js': [
        r'^\s*class\s+\w+',
        r'^\s*const\s+\w+\s*=\s*class\s+\w+'
    ],
    'sql': [],  # SQL doesn't have classes
    'go': [
        r'^\s*type\s+\w+\s+struct\s*\{',
        r'^\s*type\s+\w+\s+interface\s*\{'
    ],
    'rs': [
        r'^\s*struct\s+\w+',
        r'^\s*enum\s+\w+',
        r'^\s*trait\s+\w+'
    ],
    'php': [
        r'^\s*class\s+\w+',
        r'^\s*interface\s+\w+',
        r'^\s*trait\s+\w+'
    ],
    'r': [
        r'^\s*setClass\s*\(',
        r'^\s*setRefClass\s*\('
    ],
    'asm': [],  # Assembly doesn't have classes
    'rb': [
        r'^\s*class\s+\w+',
        r'^\s*module\s+\w+'
    ],
    'kt': [
        r'^\s*class\s+\w+',
        r'^\s*interface\s+\w+',
        r'^\s*object\s+\w+'
    ],
    'css': []  # CSS doesn't have classes in programming sense
}


# Import patterns
IMPORT_PATTERNS = {
    'py': [
        r'^\s*import\s+',
        r'^\s*from\s+\w+\s+import\s+'
    ],
    'cpp': [
        r'^\s*#include\s+',
        r'^\s*using\s+namespace\s+',
        r'^\s*using\s+\w+::'
    ],
    'java': [
        r'^\s*import\s+',
        r'^\s*package\s+'
    ],
    'c': [
        r'^\s*#include\s+',
        r'^\s*#import\s+'
    ],
    'cs': [
        r'^\s*using\s+',
        r'^\s*using\s+static\s+'
    ],
    'js': [
        r'^\s*import\s+',
        r'^\s*export\s+',
        r'^\s*require\s*\('
    ],
    'sql': [
        r'^\s*USE\s+',
        r'^\s*CREATE\s+DATABASE\s+'
    ],
    'go': [
        r'^\s*import\s+',
        r'^\s*import\s*\('
    ],
    'rs': [
        r'^\s*use\s+',
        r'^\s*extern\s+crate\s+'
    ],
    'php': [
        r'^\s*require\s+',
        r'^\s*require_once\s+',
        r'^\s*include\s+',
        r'^\s*include_once\s+',
        r'^\s*use\s+'
    ],
    'r': [
        r'^\s*library\s*\(',
        r'^\s*require\s*\('
    ],
    'asm': [
        r'^\s*\.include\s+',
        r'^\s*\.extern\s+'
    ],
    'rb': [
        r'^\s*require\s+',
        r'^\s*require_relative\s+',
        r'^\s*load\s+'
    ],
    'kt': [
        r'^\s*import\s+',
        r'^\s*package\s+'
    ],
    'css': [
        r'^\s*@import\s+',
        r'^\s*@use\s+'
    ]
}


# File extensions mapping
FILE_EXTENSIONS = {
    'py': 'py',
    'cpp': 'cpp',
    'cc': 'cpp',
    'cxx': 'cpp',
    'hpp': 'cpp',
    'h': 'cpp',
    'java': 'java',
    'c': 'c',
    'h': 'c',
    'cs': 'cs',
    'js': 'js',
    'jsx': 'js',
    'ts': 'js',
    'tsx': 'js',
    'sql': 'sql',
    'go': 'go',
    'rs': 'rs',
    'php': 'php',
    'r': 'r',
    'asm': 'asm',
    's': 'asm',
    'rb': 'rb',
    'kt': 'kt',
    'kts': 'kt',
    'css': 'css',
    'scss': 'css',
    'sass': 'css'
} 