import os
import sys
import shutil
import zipfile
import tempfile
import subprocess
import urllib.request
import urllib.error

REPO_URL = "https://github.com/IamElite/AFB/archive/refs/heads/main.zip"
ZIP_NAME = "AFB-main"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REQ_FILE = "requirements.txt"


def download_zip(url: str, dest: str):
    print(f"[UPDATE] Downloading update from {url}...")
    urllib.request.urlretrieve(url, dest)
    print("[UPDATE] Download complete.")


def extract_zip(zip_path: str, extract_to: str):
    print(f"[UPDATE] Extracting update...")
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(extract_to)
    print("[UPDATE] Extraction complete.")


def get_requirements(path: str) -> set:
    req_file = os.path.join(path, REQ_FILE)
    if not os.path.exists(req_file):
        return set()
    with open(req_file, "r") as f:
        return {line.strip() for line in f if line.strip() and not line.startswith("#") and not line.startswith("git+")}


def install_requirements(requirements: set):
    if not requirements:
        return
    req_list = list(requirements)
    print(f"[UPDATE] Installing {len(req_list)} new requirement(s)...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install"] + req_list
        )
        print("[UPDATE] Requirements installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[UPDATE] Failed to install requirements: {e}")


def copy_new_files(src: str, dst: str):
    print("[UPDATE] Applying update...")
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            if os.path.exists(d):
                shutil.rmtree(d)
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)
    print("[UPDATE] Files updated.")


def main():
    if not os.path.isdir(BASE_DIR):
        print("[UPDATE] Error: cannot find base directory.")
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, "update.zip")
        extract_path = os.path.join(tmpdir, "extracted")

        try:
            download_zip(REPO_URL, zip_path)
        except urllib.error.HTTPError as e:
            print(f"[UPDATE] Download failed: {e}")
            sys.exit(1)

        os.makedirs(extract_path, exist_ok=True)
        extract_zip(zip_path, extract_path)

        new_source = os.path.join(extract_path, ZIP_NAME)
        if not os.path.isdir(new_source):
            print(f"[UPDATE] Error: extracted folder '{ZIP_NAME}' not found.")
            sys.exit(1)

        old_reqs = get_requirements(BASE_DIR)
        new_reqs = get_requirements(new_source)

        new_packages = new_reqs - old_reqs
        if new_packages:
            install_requirements(new_packages)
        else:
            print("[UPDATE] No new requirements to install.")

        copy_new_files(new_source, BASE_DIR)

    print("[UPDATE] Update complete! Restart the bot to apply changes.")


if __name__ == "__main__":
    main()
