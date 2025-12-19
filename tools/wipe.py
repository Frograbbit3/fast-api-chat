import shutil
import os
import sys

full = "--full" in sys.argv or "-f" in sys.argv
print("wiping...")
print("Full mode enabled:", full)

def nuke(path, recursive=False):
    if recursive:
        for root, dirs, files in os.walk(path):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                shutil.rmtree(os.path.join(root, name))
                nuke(name, recursive=True)
            return
    if os.path.isdir(path):
        shutil.rmtree(path)
    elif os.path.isfile(path):
        os.remove(path)
    else:
        print(f"Path does not exist: {path}")
        return
    print(f"Deleted {path}")

nuke("saves")
nuke("logins.json")
nuke("config.ini")
nuke("static/uploads")

if full:
    nuke("__pycache__", recursive=True)
    nuke(".venv", recursive=True)
    nuke("default-lobbies")