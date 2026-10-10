#!/usr/bin/env python3
"""Validate the structure and basic consistency of the Persian calendar data."""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import jdatetime

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "events.json"
ALLOWED_CATEGORIES = {
    "official-holiday",
    "religious-observance",
    "iranian-observance",
    "international-day",
}
DATE_PATTERN = re.compile(r"^(\d{4})/(\d{2})/(\d{2})$")


def normalize_title(value: str) -> str:
    return " ".join(value.split()).casefold()


def main() -> int:
    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read valid JSON from {DATA_FILE}: {exc}")
        return 1

    errors: list[str] = []
    warnings: list[str] = []
    coverage = str(data.get("coverage", "")).strip()
    events = data.get("events")

    if not isinstance(events, list):
        print("ERROR: 'events' must be a JSON array.")
        return 1
    if not coverage.isdigit():
        errors.append("'coverage' must be a Persian calendar year, e.g. 1405.")

    seen: dict[tuple[str, str], int] = {}
    titles_by_date: dict[str, list[str]] = defaultdict(list)

    for index, event in enumerate(events, start=1):
        prefix = f"events[{index}]"
        if not isinstance(event, dict):
            errors.append(f"{prefix} must be an object.")
            continue

        date_text = event.get("date")
        title = event.get("title")
        category = event.get("category")

        if not isinstance(date_text, str) or not DATE_PATTERN.fullmatch(date_text):
            errors.append(f"{prefix}: date must use YYYY/MM/DD format.")
            continue

        year, month, day = map(int, date_text.split("/"))
        try:
            jdatetime.date(year, month, day)
        except ValueError:
            errors.append(f"{prefix}: invalid Persian date {date_text}.")
            continue

        if coverage.isdigit() and year != int(coverage):
            errors.append(f"{prefix}: {date_text} is outside declared coverage {coverage}.")

        if not isinstance(title, str) or not title.strip():
            errors.append(f"{prefix}: title must be a non-empty string.")
            continue
        if title != title.strip():
            warnings.append(f"{prefix}: title has leading/trailing whitespace.")
        if not isinstance(category, str) or category not in ALLOWED_CATEGORIES:
            errors.append(f"{prefix}: unsupported category {category!r}.")
            continue

        key = (date_text, normalize_title(title))
        if key in seen:
            errors.append(
                f"{prefix}: duplicate title/date also found in events[{seen[key]}] ({date_text}: {title})."
            )
        else:
            seen[key] = index
        titles_by_date[date_text].append(title)

    if not events:
        errors.append("No events found in the dataset.")

    # These are review hints, not hard failures: data needs human/source verification.
    for date_text, titles in sorted(titles_by_date.items()):
        if len(titles) >= 8:
            warnings.append(f"{date_text}: unusually many events ({len(titles)}); review source data.")

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(f"Validation failed: {len(errors)} error(s), {len(warnings)} warning(s), {len(events)} event(s).")
        return 1

    print(f"Validation passed: {len(events)} event(s), coverage {coverage}; {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
