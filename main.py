from agent.repo_loader import clone_repo
from agent.file_scanner import scan_repo
from agent.context_builder import build_context
from agent.llm_reasoner import analyze_repo


url = input("Enter GitHub repo URL: ")

repo_path = clone_repo(url)
tree = scan_repo(repo_path)
context = build_context(repo_path, tree)

analysis = analyze_repo(context)

print("\n===== Gemini Analysis =====\n")
print(analysis)
