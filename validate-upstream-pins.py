import json
import re
from pathlib import Path


SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")
containerfile = Path("Containerfile").read_text(encoding="utf-8")
match = re.search(r"^ARG FRAPPE_COMMIT=([0-9a-f]+)$", containerfile, re.MULTILINE)
if not match or not SHA_PATTERN.fullmatch(match.group(1)):
    raise ValueError("Containerfile must pin FRAPPE_COMMIT to an exact 40-character SHA")

apps = json.loads(Path("upstream-apps.json").read_text(encoding="utf-8"))
if not isinstance(apps, list) or not apps:
    raise ValueError("upstream-apps.json must contain a nonempty list")

seen_urls = set()
for app in apps:
    url = app.get("url", "")
    commit = app.get("commit", "")
    if not url.startswith("https://github.com/frappe/"):
        raise ValueError(f"Unexpected upstream URL: {url}")
    if url in seen_urls:
        raise ValueError(f"Duplicate upstream URL: {url}")
    if not SHA_PATTERN.fullmatch(commit):
        raise ValueError(f"{url} must pin an exact 40-character commit SHA")
    seen_urls.add(url)

print("All upstream application commits are pinned.")
