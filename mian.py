#!/usr/bin/env python3
"""
Auto Git Commit Script
Automatically commits and pushes all changes in the current Git repository.
"""

import subprocess
import sys
from datetime import datetime
import os

def run_command(command, check=True):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            check=check
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{command}': {e}")
        print(f"Error output: {e.stderr}")
        return None

def check_git_repo():
    """Check if current directory is a Git repository."""
    result = run_command("git rev-parse --is-inside-work-tree", check=False)
    return result and result.returncode == 0

def get_repo_status():
    """Get the status of the repository."""
    result = run_command("git status --porcelain")
    return result.stdout if result else ""

def commit_changes(message=None):
    """Stage, commit, and push all changes."""
    
    # Check if we're in a Git repository
    if not check_git_repo():
        print("❌ Error: Not in a Git repository!")
        return False
    
    # Check if there are any changes
    status = get_repo_status()
    if not status.strip():
        print("✅ No changes to commit.")
        return True
    
    print("📁 Changes detected:")
    print(status)
    
    # Stage all changes
    print("📤 Staging all changes...")
    result = run_command("git add .")
    if not result:
        return False
    
    # Create commit message
    if not message:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"Auto-commit: {timestamp}"
    
    # Commit changes
    print(f"💾 Committing with message: '{message}'")
    result = run_command(f'git commit -m "{message}"')
    if not result:
        return False
    
    # Get current branch
    branch_result = run_command("git branch --show-current")
    if not branch_result:
        print("⚠️  Warning: Could not determine current branch")
        branch = "main"  # fallback
    else:
        branch = branch_result.stdout.strip()
    
    # Push changes
    print(f"🚀 Pushing to remote repository (branch: {branch})...")
    result = run_command(f"git push origin {branch}")
    if not result:
        print("❌ Failed to push changes")
        return False
    
    print("✅ Successfully committed and pushed all changes!")
    return True

def main():
    """Main function."""
    print("🔄 Auto Git Commit Script")
    print("=" * 30)
    
    # Check if custom message provided
    custom_message = None
    if len(sys.argv) > 1:
        custom_message = " ".join(sys.argv[1:])
        print(f"📝 Using custom commit message: '{custom_message}'")
    
    # Commit changes
    success = commit_changes(custom_message)
    
    if success:
        print("\n🎉 All done!")
        sys.exit(0)
    else:
        print("\n❌ Script completed with errors.")
        sys.exit(1)

if __name__ == "__main__":
    main()