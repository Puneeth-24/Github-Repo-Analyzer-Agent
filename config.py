IGNORE_DIRS = {
    ".git",
    "node_modules",
    "venv",
    "__pycache__",
    "dist",
    "build",
    ".idea",
    ".vscode",
}

IGNORE_EXTENSIONS = {
    ".log",
    ".lock",
    ".pyc",
    ".exe",
    ".dll",
}

MAX_FILE_SIZE = 1_000_000  # 1 MB

LANGUAGE_MAP = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".java": "Java",
    ".cpp": "C++",
    ".c": "C",
    ".go": "Go",
    ".rs": "Rust",
    ".rb": "Ruby",
}

IMPORTANT_FILES = {
    "README.md",
    "requirements.txt",
    "package.json",
    "Dockerfile",
    "main.py",
    "app.py",
    "index.js",
    "server.js",
}

FRAMEWORK_HINTS = {
    "Flask": ["templates", "static", "flask"],
    "FastAPI": ["fastapi"],
    "React": ["react", "vite.config.js"],
    "Django": ["manage.py"],
}

REPO_TYPE_HINTS = {
    "web_app": ["templates", "static", "server.py", "app.py"],
    "ml_project": [".ipynb", "model", "train"],
    "library": ["setup.py", "__init__.py"],
}
