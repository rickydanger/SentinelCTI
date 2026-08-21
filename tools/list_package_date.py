#!/usr/bin/env python3
"""
Helper tool: List installed Python packages sorted by install date (newest first).
This is a development/utility script, not part of the main application.
"""

import time
import site
from pathlib import Path

def main():
    sp = Path(site.getsitepackages()[0]) / "Lib" / "site-packages"
    if not sp.exists():
        sp = Path(site.getsitepackages()[0])

    print(f"Looking in: {sp}\n")

    packages = []
    for item in sp.iterdir():
        if item.is_dir() and not item.name.endswith((".dist-info", "__pycache__")):
            timestamp = item.stat().st_ctime
            date = time.strftime("%Y-%m-%d %H:%M", time.localtime(timestamp))
            packages.append((timestamp, date, item.name))

    # Newest first
    for _, date, name in sorted(packages, reverse=True):
        print(f"{date}  {name}")


if __name__ == "__main__":
    main()