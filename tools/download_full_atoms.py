#!/usr/bin/env python3
"""Download and install the full opeskill atom libraries from GitHub Releases."""

from __future__ import annotations

import json
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

REPO = "FocusLiz-Lab/opeskill"
ASSET_NAME = "opes-local.zip"
INSTALL_PREFIXES = ("知识库/原子库/", "知识库/商业案例库/")


def package_root() -> Path:
    return Path(__file__).resolve().parents[1]


def fetch_latest_release() -> dict:
    url = f"https://api.github.com/repos/{REPO}/releases/latest"
    with urllib.request.urlopen(url, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def find_asset(release: dict) -> dict:
    for asset in release.get("assets", []):
        if asset.get("name") == ASSET_NAME:
            return asset
    raise RuntimeError(f"未在最新 Release 中找到 {ASSET_NAME}")


def download_asset(url: str, target: Path) -> None:
    with urllib.request.urlopen(url, timeout=300) as response:
        target.write_bytes(response.read())


def normalize_member(name: str) -> str:
    normalized = name.replace("\\", "/")
    return normalized.split("/", 1)[1] if normalized.startswith("opes/") else normalized


def install_from_zip(zip_path: Path, root: Path) -> int:
    count = 0
    with zipfile.ZipFile(zip_path) as archive:
        for member in archive.infolist():
            relative = normalize_member(member.filename)
            if member.is_dir() or not relative.startswith(INSTALL_PREFIXES):
                continue
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.read(member))
            count += 1
    return count


def main() -> int:
    root = package_root()
    print("读取 opeskill 最新 Release ...")
    release = fetch_latest_release()
    asset = find_asset(release)

    with tempfile.TemporaryDirectory() as tmp:
        zip_path = Path(tmp) / ASSET_NAME
        print(f"下载 {ASSET_NAME} ...")
        download_asset(asset["browser_download_url"], zip_path)
        print("解压安装 7 人原子库和商业案例库 ...")
        count = install_from_zip(zip_path, root)

    if count == 0:
        print("未解压到任何原子库文件，请检查 Release 包结构。", file=sys.stderr)
        return 1

    print(f"完成：已安装 {count} 个文件到 {root / '知识库'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
