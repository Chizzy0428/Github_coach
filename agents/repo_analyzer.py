from git import Repo
import shutil, os, stat

REPO_DIR = "temp_repo"

def _handle_remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def repo_analyzer(state):
    repo_url = state["repo_url"]

    # clean out old clone
    if os.path.exists(REPO_DIR):
        shutil.rmtree(REPO_DIR, onerror=_handle_remove_readonly)

    Repo.clone_from(repo_url, REPO_DIR)

    readme_path = os.path.join(REPO_DIR, "README.md")
    readme = open(readme_path, encoding="utf-8").read() if os.path.exists(readme_path) else "No README found"
    structure = "\n".join(os.path.relpath(r, REPO_DIR) for r, _, _ in os.walk(REPO_DIR))

    # IMPORTANT: return only what this step adds
    return {
        "repo_url": repo_url,
        "readme": readme,
        "structure": structure,
    }
