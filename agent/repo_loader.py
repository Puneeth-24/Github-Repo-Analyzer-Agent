import os
import re
from git import Repo, GitCommandError


BASE_REPO_DIR = os.path.join("data", "repos")


class RepoLoaderError(Exception):
    """Custom exception for repo loading issues."""
    pass


def extract_repo_name(url: str) -> str:
    """
    Extract repository name from GitHub URL.

    Example:
    https://github.com/user/weather-app.git → weather-app
    """
    pattern = r"github\.com/[^/]+/([^/.]+)"
    match = re.search(pattern, url)

    if not match:
        raise RepoLoaderError("Invalid GitHub repository URL")

    return match.group(1)


def ensure_repo_directory() -> None:
    """Create base repo directory if it doesn't exist."""
    os.makedirs(BASE_REPO_DIR, exist_ok=True)


def clone_repo(url: str) -> str:
    """
    Clone a GitHub repository and return local path.

    If repo already exists locally, reuse it.
    """
    ensure_repo_directory()

    repo_name = extract_repo_name(url)
    local_path = os.path.join(BASE_REPO_DIR, repo_name)

    # If repo already exists, reuse it
    if os.path.exists(local_path):
        print(f"📦 Repo already exists locally: {local_path}")
        return local_path

    try:
        print(f"⬇️ Cloning repository: {url}")
        Repo.clone_from(url, local_path)
        print("✅ Clone successful")

        return local_path

    except GitCommandError as e:
        raise RepoLoaderError(f"Failed to clone repository: {e}")
