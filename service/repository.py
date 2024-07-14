import os
import shutil
from git import Repo

def pull(repo):
    try:
        origin = repo.remotes.origin
        origin.pull()
    except Exception as e:
        print(e)
        raise Exception(f"Error pulling repo: {e}")


def clone(repo_url, path):
    try:
        os.makedirs(path)
        Repo.clone_from(repo_url, path)
    except Exception as e:
        print(e)
        raise Exception(f"Error cloning repo: {e}")

def is_repo(path):
    return os.path.isdir(os.path.join(path, '.git'))

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
    try:
        repo = Repo(path)
        
        print("Repo path: ", repo.working_dir)

        if repo.is_dirty(untracked_files=True):
            print("Repo is dirty, resetting...")
            repo.git.reset('--hard')

        return repo
    except Exception as e:
        print(e)
        raise Exception(f"Error resetting repo: {e}")

# If local changes are present, this function will reset the repo and pull
def reset_and_pull(path):
    try:
        repo = reset(path)
        pull(repo)
    except Exception as e:
        print(e)
        raise Exception(f"Error resetting and pulling repo: {e}")