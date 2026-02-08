from agent.repo_loader import clone_repo
from agent.file_scanner import scan_repo
import json

url = "https://github.com/Puneeth-24/Portfolio.git"

repo_path = clone_repo(url)

tree = scan_repo(repo_path)

print(json.dumps(tree, indent=2))
