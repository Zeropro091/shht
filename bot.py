import os
import subprocess
from datetime import datetime

# Path to the file
file_path = "contributions.txt"

# 1. Check if this is a git repository
if not os.path.exists(".git"):
    print("Error: Not a git repository. Please run: git init")
    exit(1)

# 2. Check git configuration
try:
    result = subprocess.run(
        ["git", "config", "user.name"],
        capture_output=True,
        text=True,
        check=True
    )
    if not result.stdout.strip():
        print("Error: Git user.name not set. Please run: git config --global user.name \"Your Name\"")
        exit(1)
except subprocess.CalledProcessError:
    print("Error: Git not configured properly.")
    exit(1)

# 3. Update the file with current timestamp
with open(file_path, "w") as f:
    f.write(f"Last contribution: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# 4. Git operations
def run_git(args):
    subprocess.run(["git"] + args, check=True, capture_output=True, text=True)

try:
    print(f"Adding '{file_path}' to git...")
    run_git(["add", file_path])

    commit_msg = f"Contribution update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    print(f"Committing with message: {commit_msg}")
    run_git(["commit", "-m", commit_msg])

    print("Pushing to GitHub...")
    run_git(["push"])
    print(f"Successfully updated '{file_path}' and pushed to GitHub!")

except subprocess.CalledProcessError as e:
    print(f"Git command failed: {e}")
    if e.stderr:
        print(f"Error details: {e.stderr}")
except Exception as e:
    print(f"Unexpected error: {e}")
