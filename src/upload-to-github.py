import os
from github import Github
from dotenv import load_dotenv

# Load token dan repo info dari .env
load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = os.getenv("GITHUB_REPO")
BRANCH = os.getenv("GITHUB_BRANCH", "main")

if not TOKEN or not REPO_NAME:
    raise ValueError("Pastikan GITHUB_TOKEN dan GITHUB_REPO ada di file .env")

# Koneksi ke GitHub
g = Github(TOKEN)
repo = g.get_repo(REPO_NAME)

# Path lokal folder cleaned
local_dir = os.path.join("output", "cleaned")

# Loop semua file .txt di cleaned
for filename in os.listdir(local_dir):
    if filename.endswith(".txt"):
        file_path = os.path.join(local_dir, filename)
        
        # Path di GitHub (misal: logs/cleaned_xxx.txt)
        github_path = f"logs/{filename}"
        
        # Cek apakah file sudah ada di repo
        try:
            contents = repo.get_contents(github_path, ref=BRANCH)
            # Jika sudah ada → update
            with open(file_path, "rb") as f:
                repo.update_file(contents.path, f"update {filename}", f.read(), contents.sha, branch=BRANCH)
            print(f"[UPDATED] {filename}")
        except:
            # Jika belum ada → create
            with open(file_path, "rb") as f:
                repo.create_file(github_path, f"add {filename}", f.read(), branch=BRANCH)
            print(f"[ADDED] {filename}")

print("✅ Upload selesai.")
