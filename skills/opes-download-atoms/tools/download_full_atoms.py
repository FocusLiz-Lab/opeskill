#!/usr/bin/env python3
"""Download and install the full opeskill atom libraries from GitHub Releases."""

from __future__ import annotations

import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

REPO = "FocusLiz-Lab/opeskill"
ASSET_NAME = "opes-local.zip"
INSTALL_PREFIXES = ("知识库/原子库/",)


def package_root() -> Path:
    return Path(__file__).resolve().parents[1]


def asset_url() -> str:
    return f"https://github.com/{REPO}/releases/latest/download/{ASSET_NAME}"


def download_asset(target: Path) -> None:
    with urllib.request.urlopen(asset_url(), timeout=300) as response:
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
    with tempfile.TemporaryDirectory() as tmp:
        zip_path = Path(tmp) / ASSET_NAME
        print(f"下载 {ASSET_NAME} ...")
        download_asset(zip_path)
        print("解压安装 7 人专家原子库 ...")
        count = install_from_zip(zip_path, root)

    if count == 0:
        print("未解压到任何原子库文件，请检查 Release 包结构。", file=sys.stderr)
        return 1

    print(f"完成：已安装 {count} 个专家原子库文件到 {root / '知识库'}")
    print("商业案例库已抽离到 $commercial-case-library，不在 opeskill 内重复下载。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
