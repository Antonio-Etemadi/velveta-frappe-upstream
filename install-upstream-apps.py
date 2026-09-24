import json
import re
import subprocess
import sys
from pathlib import Path

apps_json_path = Path("/opt/frappe/upstream-apps.json")
if not apps_json_path.exists():
    print("No upstream apps json found at /opt/frappe/upstream-apps.json")
    sys.exit(0)

apps = json.loads(apps_json_path.read_text(encoding="utf-8"))
for app in apps:
    url = app["url"]
    branch = app.get("branch", "version-16")
    commit = (app.get("commit") or "").strip()
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError(f"{url} must have an exact 40-character commit pin")
    app_name = Path(url.rstrip("/").removesuffix(".git")).name
    app_path = Path(f"apps/{app_name}")
    if app_path.exists():
        subprocess.run(["rm", "-rf", str(app_path)], check=True)

    print(f"Cloning upstream app {app_name} ({branch})...")
    subprocess.run(["git", "clone", "--depth=50", "-b", branch, url, str(app_path)], check=True)
    print(f"Checking out pinned commit {commit} for {app_name}...")
    head = subprocess.check_output(["git", "-C", str(app_path), "rev-parse", "HEAD"], text=True).strip()
    if head != commit:
        subprocess.run(["git", "-C", str(app_path), "fetch", "--depth=1", "origin", commit], check=True)
    subprocess.run(["git", "-C", str(app_path), "checkout", "--detach", "--force", commit], check=True)
    checked_out = subprocess.check_output(
        ["git", "-C", str(app_path), "rev-parse", "HEAD"], text=True
    ).strip()
    if checked_out != commit:
        raise RuntimeError(f"{app_name} resolved to {checked_out}, expected {commit}")
    print(f"Installing {app_name} in editable mode...")
    subprocess.run(["./env/bin/pip", "install", "--no-cache-dir", "-e", str(app_path)], check=True)

    if (app_path / "package.json").exists():
        print(f"Installing node dependencies for {app_name}...")
        subprocess.run(["yarn", "--cwd", str(app_path), "install"], check=False)

print("Running bench setup requirements for node...")
subprocess.run(["bench", "setup", "requirements", "--node"], check=False)
print("All upstream apps and frontend dependencies installed successfully!")
