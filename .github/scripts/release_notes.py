"""Assemble ACAI release notes.

Layout: template, GitHub's generated "What's Changed" list, a data-change summary
(entities added/removed/modified per type, from a git diff between the previous
release tag and HEAD), then the Full Changelog line.

Standard library only.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

LIST_LIMIT = 25
CHANGELOG_MARKER = "**Full Changelog**"


def git(*args: str) -> str:
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout


def entity_id(path: str) -> str:
    type_dir, _, name = path.split("/", 2)
    return f"{type_dir}/{name.removesuffix('.json')}"


def data_changes(prev: str) -> str:
    diff = git("diff", "--name-status", "--no-renames", prev, "HEAD", "--", "*/json/*.json")
    changes: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    for line in diff.splitlines():
        status, path = line.split("\t", 1)
        kind = {"A": "added", "D": "removed", "M": "modified"}.get(status[0])
        if kind:
            changes[path.split("/", 1)[0]][kind].append(entity_id(path).split("/", 1)[1])

    if not changes:
        return "No entity records changed.\n"

    out = ["| Type | Added | Removed | Modified |", "|---|---|---|---|"]
    for type_dir in sorted(changes):
        c = changes[type_dir]
        out.append(f"| {type_dir} | {len(c['added'])} | {len(c['removed'])} | {len(c['modified'])} |")
    out.append("")
    for kind in ("added", "removed", "modified"):
        names = sorted(f"`{type_dir}/{n}`" for type_dir, c in changes.items() for n in c[kind])
        if not names:
            continue
        shown = ", ".join(names[:LIST_LIMIT])
        more = f", and {len(names) - LIST_LIMIT} more" if len(names) > LIST_LIMIT else ""
        out.append(f"<details><summary>{kind.capitalize()} ({len(names)})</summary>\n\n{shown}{more}\n\n</details>\n")
    return "\n".join(out)


def split_generated(text: str) -> tuple[str, str]:
    """Return (list part, Full Changelog line) from GitHub's generated notes."""
    head, marker, tail = text.partition(CHANGELOG_MARKER)
    return head.strip(), (marker + tail).strip() if marker else ""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prev", required=True, help="previous release tag")
    parser.add_argument("--template", required=True, type=Path)
    parser.add_argument("--generated", type=Path, help="file with GitHub generated notes")
    args = parser.parse_args()

    generated = args.generated.read_text(encoding="utf-8") if args.generated else ""
    pr_list, changelog = split_generated(generated)
    if not pr_list:
        pr_list = "## What's Changed\n\nNo merged pull requests since the previous release."

    parts = [
        args.template.read_text(encoding="utf-8").strip(),
        pr_list,
        "## Data Changes\n\n" + data_changes(args.prev).strip(),
    ]
    if changelog:
        parts.append(changelog)
    sys.stdout.write("\n\n".join(parts) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
