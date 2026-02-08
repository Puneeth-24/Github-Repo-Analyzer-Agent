import os
from config import IGNORE_DIRS, IGNORE_EXTENSIONS, MAX_FILE_SIZE


class FileScannerError(Exception):
    """Custom exception for scanning issues."""
    pass


def should_ignore(name: str, path: str) -> bool:
    """
    Decide whether to ignore a file or directory.
    """

    # Ignore directories
    if name in IGNORE_DIRS:
        return True

    # Ignore extensions
    _, ext = os.path.splitext(name)
    if ext in IGNORE_EXTENSIONS:
        return True

    # Ignore large files
    if os.path.isfile(path):
        size = os.path.getsize(path)
        if size > MAX_FILE_SIZE:
            return True

    return False


def build_tree(path: str) -> dict:
    """
    Recursively build directory tree.
    Files → None
    Folders → nested dict
    """

    tree = {}

    try:
        for item in sorted(os.listdir(path)):
            item_path = os.path.join(path, item)

            if should_ignore(item, item_path):
                continue

            if os.path.isdir(item_path):
                subtree = build_tree(item_path)

                # Skip empty directories
                if subtree:
                    tree[item] = subtree
            else:
                tree[item] = None

    except PermissionError:
        # Skip inaccessible folders
        pass

    return tree


def scan_repo(repo_path: str) -> dict:
    """
    Scan repository and return structured file tree.
    """

    if not os.path.exists(repo_path):
        raise FileScannerError("Repository path does not exist")

    print("🔍 Scanning repository files...")

    tree = build_tree(repo_path)

    print("✅ Scan complete")

    return tree
