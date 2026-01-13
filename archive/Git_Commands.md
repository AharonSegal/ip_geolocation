# ╔══════════════════════════════════════════════════════╗
# ║   GIT BASH ENVIRONMENT SETUP (WINDOWS)               ║
# ╚══════════════════════════════════════════════════════╝

git clone <url>                 # Clone from remote

git init
python -m venv venv
source venv/Scripts/activate
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
pip freeze > requirements.txt
git add .  
git commit -m "initial commit"
git push -u origin main

# ╔══════════════════════════════════════════════════════╗
# ║   BASIC GIT COMMANDS                                 ║
# ╚══════════════════════════════════════════════════════╝
"""
git add .                    
git commit -m " "      
git push                     

# ╔══════════════════════════════════════════════════════╗
# ║   GIT BRANCH WORKFLOW                                ║
# ╚══════════════════════════════════════════════════════╝
"""
# Check current branch
git branch

# Create a new branch
git checkout -b title/branch_purpose
git checkout -b final/k8

# Stage changes
git add .

# Commit changes
git commit -m "Descriptive commit message"

# Push branch to remote
git push -u origin title/branch_purpose
git push -u origin combine_servers/compose

# Switch between branches
git checkout main
git checkout title/branch_purpose

# Merge branch into main
git checkout main
git pull                  # ensure main is up-to-date
git merge route/update

# Delete branch (optional)
git branch -d title/branch_purpose        # local
git push origin --delete title/branch_purpose  # remote

# Useful commands
git status                      # View changes
git log --oneline               # Condensed history
git remote -v                   # Show remote URL
"""
# ╔══════════════════════════════════════════════════════╗
# ║   TEAM WORKFLOW – REMOTE BRANCHES                    ║
# ╚══════════════════════════════════════════════════════╝

# Fetch latest data from remote (does NOT change your code)
git fetch origin

# View all remote branches
git branch -r

# View both local + remote branches
git branch -a

# View remote branches with last commit info
git branch -r -v

# ------------------------------------------------------

# Check out a teammate’s remote branch locally
git checkout -b feature/login origin/feature/login

# (Shortcut – Git creates the local branch automatically)
git checkout feature/login
git checkout aharon/server-b
# ------------------------------------------------------

# Pull latest changes for your current branch
git pull

# Pull a specific remote branch into your current branch
git pull origin feature/login

# ------------------------------------------------------

# Review changes BEFORE merging
git log origin/feature/login --oneline
git diff main..origin/feature/login

# ------------------------------------------------------

# Merge teammate’s branch into your branch
git merge origin/feature/login

# ------------------------------------------------------

# Standard merge flow into main
git checkout main
git pull origin main
git merge feature/login

# Resolve conflicts if needed
git status
# edit files → fix conflicts
git add .
git commit

# ------------------------------------------------------

# Push updated main to remote
git push origin main

# ------------------------------------------------------

# Clean up branches after merge
git branch -d feature/login                # delete local
git push origin --delete feature/login     # delete remote

# ------------------------------------------------------

# Useful team commands
git show origin/feature/login              # inspect last commit
git log --graph --oneline --all            # visualize branch graph
git blame file.py                          # see who changed what

# ╔══════════════════════════════════════════════════════╗
# ║   GIT: GO BACK TO OLD VERSIONS & PUSH TO GITHUB      ║
# ╚══════════════════════════════════════════════════════╝
"""
# Save current work
git status
git add .
git commit -m "Current working version"

# View commit history
git log --oneline

## ✅ Option A — Revert (Keep History, Create New Commit)
git revert <old_commit_hash>..HEAD
# Example:
git revert 8a61c0c8360841b8ef1a5f47f41854adc48f12d3..HEAD
git push

# Abort if stuck
git revert --abort

## 🔴 Option B — Reset (Full Move Back, No Conflicts)
git reset --hard <old_commit_hash>
git push --force

## Push project to GitHub
git init
git remote add origin https://github.com/AharonSegal/..
git add .
git commit -m "Initial Push"
git branch -M main          # Rename master → main
git push -u origin main

# If push fails due to remote changes
git pull origin main --rebase
git push -u origin main


# ╔══════════════════════════════════════════════════════╗
# ║   GIT LOGGING & VIEWING HISTORY                       ║
# ╚══════════════════════════════════════════════════════╝
"""
# View current branch status
git status

# View full commit history
git log

# View condensed history (one line per commit)
git log --oneline

# Show commits with graph
git log --oneline --graph --decorate --all

# View last N commits
git log -n 5

# View changes in a commit
git show <commit-hash>

# View differences in working directory
git diff

# View staged changes
git diff --cached

# Show remote repositories
git remote -v

# View detailed commit history for a file
git log -- <file-path>
"""
