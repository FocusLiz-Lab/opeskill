#!/usr/bin/env python3
"""Manually synchronize one creator suite from a pinned GitHub main commit (stdlib only)."""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import tempfile
import urllib.request
import uuid
import zipfile


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "creator-skill-updater/1.0"})
    with urllib.request.urlopen(request, timeout=300) as response:
        return response.read()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_relative(name):
    path = PurePosixPath(name)
    if "\\" in name or path.is_absolute() or any(p in {"..", "."} or ":" in p for p in path.parts):
        raise ValueError(f"Unsafe archive path: {name}")
    return path


def build_plan(archive, config, skills_dir):
    """Read all payloads before touching installation; reject traversal and symlinks."""
    plan = {}
    for member in archive.infolist():
        if member.is_dir():
            continue
        if (member.external_attr >> 16) & 0o170000 == 0o120000:
            raise ValueError("Archive symlinks are not supported")
        path = safe_relative(member.filename)
        parts = path.parts[1:]
        if not parts:
            continue
        relative = Path(*parts)
        if config["main_skill"] != "commercial-case-library" and "商业案例库" in parts:
            continue
        if parts[0] == "skills" and len(parts) >= 3:
            target = skills_dir / Path(*parts[1:])
        elif parts[0] == "知识库" and len(parts) >= 3:
            # Legacy repository-root data belongs to the installed main router.
            if parts[1] == "商业案例库":
                continue  # separate shared dependency, never duplicate into creator suites
            target = skills_dir / config["main_skill"] / relative
        else:
            continue
        if any(p in {".git", "__pycache__"} for p in parts):
            continue
        data = archive.read(member)
        if target in plan and plan[target] != data:
            raise ValueError(f"Conflicting duplicate payload: {relative}")
        plan[target] = data
    main = skills_dir / config["main_skill"]
    if main / "SKILL.md" not in plan:
        raise ValueError("Archive does not contain the main skill")
    if config["main_skill"] == "commercial-case-library":
        shared = Path(os.environ.get("COMMERCIAL_CASE_LIBRARY_HOME", str(Path.home() / ".agents/shared/commercial-case-library"))).expanduser().absolute()
        bundled = main / "知识库/商业案例库"
        for path, data in list(plan.items()):
            if path.is_relative_to(bundled):
                plan[shared / "知识库/商业案例库" / path.relative_to(bundled)] = data
    for target in plan:
        if any(p.is_symlink() for p in [target, *target.parents]):
            raise ValueError(f"Refusing to overwrite a symlink: {target}")
    return plan


def apply_plan(plan, backup_dir):
    changed = {p: data for p, data in plan.items() if not p.is_file() or digest(p.read_bytes()) != digest(data)}
    if not changed:
        return 0
    backup_dir.mkdir(parents=True, exist_ok=False)
    journal = []
    try:
        for index, (target, data) in enumerate(changed.items()):
            old = backup_dir / str(index)
            existed = target.exists()
            if existed:
                shutil.copy2(target, old)
            journal.append((target, old, existed))
            target.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as stream:
                temp = Path(stream.name)
                stream.write(data)
            try:
                os.replace(temp, target)
            finally:
                temp.unlink(missing_ok=True)
        (backup_dir / "restore.json").write_text(json.dumps([
            {"target": str(p), "backup": str(old), "existed": existed} for p, old, existed in journal
        ], ensure_ascii=False, indent=2), encoding="utf-8")
    except BaseException:
        for target, old, existed in reversed(journal):
            if existed:
                shutil.copy2(old, target)
            else:
                target.unlink(missing_ok=True)
        raise
    return len(changed)


def run(config, skills_dir, check_only=False):
    repo = config["repository"]
    if not repo.startswith("FocusLiz-Lab/") or repo.count("/") != 1:
        raise ValueError("Unexpected update repository")
    info = json.loads(fetch(f"https://api.github.com/repos/{repo}/commits/main"))
    sha = info["sha"]
    if len(sha) != 40 or any(c not in "0123456789abcdef" for c in sha):
        raise ValueError("Invalid GitHub commit")
    state_path = skills_dir / config["main_skill"] / ".skill-update-state.json"
    state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {}
    current = state.get("commit") == sha and all(
        Path(p).is_file() and digest(Path(p).read_bytes()) == h for p, h in state.get("files", {}).items()
    ) and bool(state.get("files"))
    if check_only or current:
        return {"repository": repo, "commit": sha, "status": "current" if current else "update_available", "changed": 0}
    with zipfile.ZipFile(io.BytesIO(fetch(f"https://codeload.github.com/{repo}/zip/{sha}"))) as archive:
        plan = build_plan(archive, config, skills_dir)
    state_data = {"repository": repo, "commit": sha, "files": {str(p): digest(data) for p, data in plan.items()}}
    plan[state_path] = (json.dumps(state_data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    backup = skills_dir / ".creator-skill-backups" / config["main_skill"] / uuid.uuid4().hex
    changed = apply_plan(plan, backup)
    return {"repository": repo, "commit": sha, "status": "updated", "changed": changed, "backup": str(backup)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check without downloading or writing")
    parser.add_argument("--skills-dir", type=Path, help="Override the directory containing installed skill folders")
    args = parser.parse_args()
    script_dir = Path(__file__).resolve().parent
    config = json.loads((script_dir / "update-source.json").read_text(encoding="utf-8"))
    parent = script_dir.parent
    default = parent / "skills" if (parent / "skills").is_dir() else parent.parent
    try:
        result = run(config, (args.skills_dir or default).expanduser().absolute(), args.check)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(f"Update failed; installation was not completed: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
