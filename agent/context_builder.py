import os
from collections import Counter
from config import LANGUAGE_MAP, IMPORTANT_FILES,FRAMEWORK_HINTS,REPO_TYPE_HINTS

class ContextBuilderError(Exception):
    """Custom exception for context building issues."""
    pass


def flatten_tree(tree: dict, base_path=""):
    """
    Convert nested tree into list of file paths.
    """
    files = []

    for name, subtree in tree.items():
        current_path = os.path.join(base_path, name)

        if subtree is None:
            files.append(current_path)
        else:
            files.extend(flatten_tree(subtree, current_path))

    return files


def detect_languages(file_paths):
    """
    Detect programming languages from file extensions.
    """
    counter = Counter()

    for path in file_paths:
        _, ext = os.path.splitext(path)
        if ext in LANGUAGE_MAP:
            counter[LANGUAGE_MAP[ext]] += 1

    return dict(counter)


def find_important_files(file_paths):
    """
    Identify important files in repo.
    """
    return [
        path for path in file_paths
        if os.path.basename(path) in IMPORTANT_FILES
    ]


def guess_entry_points(file_paths):
    """
    Guess likely entry point files.
    """
    candidates = {"main.py", "app.py", "index.js", "server.js"}

    return [
        path for path in file_paths
        if os.path.basename(path) in candidates
    ]


def compute_stats(tree: dict, file_paths):
    """
    Compute repository statistics.
    """

    def count_dirs(subtree):
        total = 0
        for value in subtree.values():
            if isinstance(value, dict):
                total += 1 + count_dirs(value)
        return total

    return {
        "total_files": len(file_paths),
        "total_directories": count_dirs(tree),
    }


def build_context(repo_path: str, tree: dict) -> dict:
    """
    Build structured metadata context for repo.
    """

    if not os.path.exists(repo_path):
        raise ContextBuilderError("Repository path does not exist")

    print("🧠 Building repository context...")

    file_paths = flatten_tree(tree)

    languages = detect_languages(file_paths)
    primary_language = get_primary_language(languages)
    frameworks = detect_frameworks(file_paths, tree)
    repo_type = classify_repo_type(file_paths)
    important_files = find_important_files(file_paths)
    entry_points = guess_entry_points(file_paths)
    stats = compute_stats(tree, file_paths)

    context = {
    "repo_name": os.path.basename(repo_path),
    "languages": languages,
    "primary_language": primary_language,
    "frameworks": frameworks,
    "repo_type": repo_type,
    "important_files": important_files,
    "entry_points": entry_points,
    "stats": stats,
    "directory_tree": tree,
}


    print("✅ Context built successfully")

    return context

def detect_frameworks(file_paths, tree):
    """
    Detect frameworks based on file and folder hints.
    """
    detected = set()

    all_names = set()

    # collect all file/folder names
    def collect_names(subtree):
        for name, value in subtree.items():
            all_names.add(name.lower())
            if isinstance(value, dict):
                collect_names(value)

    collect_names(tree)

    for framework, hints in FRAMEWORK_HINTS.items():
        for hint in hints:
            if hint.lower() in all_names:
                detected.add(framework)

    return list(detected)


def classify_repo_type(file_paths):
    """
    Classify repository type.
    """
    joined = " ".join(file_paths).lower()

    for repo_type, hints in REPO_TYPE_HINTS.items():
        for hint in hints:
            if hint.lower() in joined:
                return repo_type

    return "unknown"


def get_primary_language(language_counts):
    """
    Determine dominant language.
    """
    if not language_counts:
        return None

    return max(language_counts, key=language_counts.get)
