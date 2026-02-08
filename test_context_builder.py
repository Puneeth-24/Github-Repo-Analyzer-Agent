from agent.repo_loader import clone_repo
from agent.file_scanner import scan_repo
from agent.context_builder import build_context
import json

url = "https://github.com/numpy/numpy.git"

repo_path = clone_repo(url)
tree = scan_repo(repo_path)
context = build_context(repo_path, tree)

print(json.dumps(context, indent=2))
