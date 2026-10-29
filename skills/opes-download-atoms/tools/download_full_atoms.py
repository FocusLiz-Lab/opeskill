#!/usr/bin/env python3
"""Compatibility entry: update the suite and current atoms from GitHub main."""
from pathlib import Path
import runpy

if __name__ == "__main__":
    runpy.run_path(str(Path(__file__).with_name("update_skill.py")), run_name="__main__")
