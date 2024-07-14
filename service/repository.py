import os
import shutil
from git import Repo

# Main method of the program, it will clone the repo if it doesn't exist, or pull if it does
def clone_or_pull(repo_url, path):
    if not os.path.exists(path):
        print("Cloning repo...")
        clone(repo_url, path)
    elif not is_repo(path):
        print("Path is not a repo, cloning...")
        shutil.rmtree(path)
        clone(repo_url, path)
    else:
        print("Repo exists, resetting and pulling repo...")
        reset_and_pull(path)

def reset(path):
    repo = Repo(path)

    if repo.is_dirty(untracked_files=True):
        print("Repo is dirty, resetting...")
        repo.git.reset('--hard')

    return repo

def reset_and_pull(path):
    repo = reset(path)
    pull(repo)

def clone(repo_url, path):
    os.makedirs(path)
    Repo.clone_from(repo_url, path)

def pull(repo):
    origin = repo.remotes.origin
    origin.pull()

def is_repo(path):
    return os.path.isdir(os.path.join(path, '.git'))