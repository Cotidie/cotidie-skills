#!/usr/bin/env python3
"""Copy the bundled CRA-style scaffold template into a new project directory."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path


NPM_NAME_RE = re.compile(r"^(?:@[a-z0-9][a-z0-9._-]*/)?[a-z0-9][a-z0-9._-]*$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", required=True, help="npm package name")
    parser.add_argument("--dest", required=True, help="new project directory")
    parser.add_argument(
        "--force",
        action="store_true",
        help="allow copying into an existing empty directory",
    )
    return parser.parse_args()


def validate_name(name: str) -> None:
    if not NPM_NAME_RE.match(name):
        raise ValueError(
            "--name must be a valid lowercase npm package name, optionally scoped"
        )


def copy_template(template_dir: Path, dest: Path, force: bool) -> None:
    if not template_dir.is_dir():
        raise FileNotFoundError(f"Template directory not found: {template_dir}")

    if dest.exists():
        if not dest.is_dir():
            raise FileExistsError(f"Destination exists and is not a directory: {dest}")
        if any(dest.iterdir()):
            raise FileExistsError(f"Destination is not empty: {dest}")
        if not force:
            raise FileExistsError(
                f"Destination exists: {dest}. Use --force if it is intentionally empty."
            )
        shutil.copytree(template_dir, dest, dirs_exist_ok=True)
    else:
        shutil.copytree(template_dir, dest)


def rewrite_package_name(dest: Path, name: str) -> None:
    package_file = dest / "package.json"
    data = json.loads(package_file.read_text(encoding="utf-8"))
    data["name"] = name
    package_file.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    try:
        validate_name(args.name)
        script_dir = Path(__file__).resolve().parent
        template_dir = script_dir.parent / "assets" / "cra-template"
        dest = Path(args.dest).expanduser().resolve()
        copy_template(template_dir, dest, args.force)
        rewrite_package_name(dest, args.name)
    except Exception as exc:  # noqa: BLE001 - script should print concise CLI errors.
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"status": "created", "name": args.name, "dest": str(dest)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
