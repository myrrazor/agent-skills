#!/usr/bin/env python3
"""Summarize a local Fable fallback calibration CSV without external packages."""

from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path
from typing import Iterable

REQUIRED = {
    "predicted_likelihood",
    "context_profile",
    "fallback",
    "category",
}


def truthy(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y", "fallback", "opus"}


def pct(n: int, d: int) -> str:
    return "—" if d == 0 else f"{100.0 * n / d:.1f}%"


def table(rows: Iterable[tuple[str, int, int]]) -> str:
    out = ["| Group | Samples | Fallbacks | Rate |", "|---|---:|---:|---:|"]
    for name, total, falls in rows:
        out.append(f"| {name or '(blank)'} | {total} | {falls} | {pct(falls, total)} |")
    return "\n".join(out)


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {Path(sys.argv[0]).name} path/to/calibration-log.csv", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"File not found: {path}", file=sys.stderr)
        return 2

    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        fields = set(reader.fieldnames or [])
        missing = REQUIRED - fields
        if missing:
            print(f"Missing required columns: {', '.join(sorted(missing))}", file=sys.stderr)
            return 2
        records = list(reader)

    if not records:
        print("No calibration records yet.")
        return 0

    def aggregate(key: str):
        groups: dict[str, list[int]] = defaultdict(lambda: [0, 0])
        for row in records:
            name = (row.get(key) or "").strip()
            groups[name][0] += 1
            groups[name][1] += int(truthy(row.get("fallback", "")))
        return [(name, values[0], values[1]) for name, values in sorted(groups.items())]

    print("# Fable fallback calibration summary\n")
    total_fallbacks = sum(truthy(row.get("fallback", "")) for row in records)
    print(f"Overall: {total_fallbacks}/{len(records)} fallbacks ({pct(total_fallbacks, len(records))}).\n")

    print("## By predicted likelihood\n")
    print(table(aggregate("predicted_likelihood")))
    print("\n## By context profile\n")
    print(table(aggregate("context_profile")))
    print("\n## By reported category\n")
    print(table(aggregate("category")))
    print("\nTreat small samples cautiously. Recalibrate after Claude Code or safeguard changes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
