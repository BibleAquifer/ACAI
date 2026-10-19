"""Validate ACAI JSON/Markdown records.

Errors (exit 1): unparseable JSON, id/filename/type mismatches, duplicate ids,
missing primary_id, JSON without a Markdown twin.

Warnings (exit 0): Aquifer article links that look wrong (see lint_links). Warnings are
reported only for content_ids not listed in lint-baseline.json, so findings that were
reviewed and accepted stay quiet and new ones stand out. Regenerate the baseline with
``--write-baseline`` after a deliberate review.

Standard library only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASELINE = Path(__file__).resolve().parent.parent / "lint-baseline.json"
TYPE_DIRS = ["people", "places", "groups", "deities", "fauna", "flora", "realia", "keyterms"]


def strip_disambig(label: str) -> str:
    return re.sub(r"\s*\([^)]*\)\s*$", "", label).strip()


def tokens(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-z]+", text.lower()) if len(t) > 2}


def eng_labels(record: dict) -> list[str]:
    eng = record.get("localizations", {}).get("eng", {})
    labels = [eng.get("preferred_label", "")] + list(eng.get("alternate_labels") or [])
    return [strip_disambig(x) for x in labels if x]


def load_records(errors: list[str]) -> dict[str, dict]:
    records: dict[str, dict] = {}
    for type_dir in TYPE_DIRS:
        for path in sorted((ROOT / type_dir / "json").glob("*.json")):
            rel = path.relative_to(ROOT)
            try:
                record = json.loads(path.read_text(encoding="utf-8"))
            except ValueError as exc:
                errors.append(f"{rel}: invalid JSON ({exc})")
                continue
            rid = record.get("id")
            if not rid:
                errors.append(f"{rel}: missing id")
                continue
            if rid.split(":", 1)[-1] != path.stem:
                errors.append(f"{rel}: id {rid!r} does not match file name")
            if record.get("type") and not rid.startswith(f"{record['type']}:"):
                errors.append(f"{rel}: id {rid!r} does not start with type {record['type']!r}")
            if not record.get("primary_id"):
                errors.append(f"{rel}: missing primary_id")
            if rid in records:
                errors.append(f"{rel}: duplicate id {rid!r}")
            if not (ROOT / type_dir / "md" / f"{path.stem}.md").exists():
                errors.append(f"{rel}: no Markdown file {type_dir}/md/{path.stem}.md")
            record["_path"] = str(rel)
            records[rid] = record
    for rid, record in records.items():
        if record.get("primary_id") and record["primary_id"] not in records:
            errors.append(f"{record['_path']}: primary_id {record['primary_id']!r} not found")
    return records


def lint_links(records: dict[str, dict]) -> dict[str, str]:
    """Return {content_id: reason} for Aquifer links that look wrong.

    * ``multi``: several primaries claim the article and the article title is not
      covered by every claimant's English labels (Simon Magus pattern).
    * ``secondary``: a secondary record carries a link whose title shares no word
      with any label of its primary or the primary's secondaries.
    """
    pool: dict[str, set[str]] = defaultdict(set)
    for record in records.values():
        for label in eng_labels(record):
            pool[record["primary_id"]] |= tokens(label)

    claims: dict[str, list[tuple[str, str]]] = defaultdict(list)  # content_id -> [(rid, title)]
    for rid, record in records.items():
        for entry in record.get("alternate_sources", {}).get("aquifer", []):
            parts = entry.split("|")
            if len(parts) >= 3:
                claims[parts[0]].append((rid, parts[1]))

    findings: dict[str, str] = {}
    for content_id, claimants in claims.items():
        title = tokens(strip_disambig(claimants[0][1]))
        if not title:
            continue
        primaries = {records[rid]["primary_id"] for rid, _ in claimants}
        if len(primaries) > 1:
            uncovered = [rid for rid, _ in claimants
                         if not title <= tokens(" ".join(eng_labels(records[rid])))]
            if uncovered:
                findings[content_id] = f"multi: {claimants[0][1]!r} claimed by {len(primaries)} " \
                                       f"primaries; {len(uncovered)} do not cover the title"
                continue
        for rid, link_title in claimants:
            record = records[rid]
            if record["id"] != record["primary_id"] and not tokens(link_title) & pool[record["primary_id"]]:
                findings[content_id] = f"secondary: {rid} links {link_title!r}, which shares no " \
                                       f"word with {record['primary_id']}"
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-baseline", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    records = load_records(errors)
    findings = lint_links(records)

    if args.write_baseline:
        BASELINE.write_text(json.dumps(sorted(findings), indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {len(findings)} content_ids to {BASELINE.relative_to(ROOT)}")
        return 0

    baseline = set(json.loads(BASELINE.read_text(encoding="utf-8"))) if BASELINE.exists() else set()
    new = {cid: why for cid, why in findings.items() if cid not in baseline}

    print(f"{len(records)} records checked; {len(errors)} errors; "
          f"{len(new)} new link warnings ({len(findings) - len(new)} baselined)")
    for message in errors:
        print(f"::error::{message}")
    for cid, why in sorted(new.items()):
        print(f"::warning::content_id {cid} {why}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
