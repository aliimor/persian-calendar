#!/usr/bin/env python3
"""Generate one combined Persian calendar ICS feed."""
from __future__ import annotations

import json
from datetime import date, datetime, timezone
from pathlib import Path

import jdatetime

ROOT = Path(__file__).resolve().parents[1]
EVENTS_FILE = ROOT / "data" / "events.json"
OUTPUT_FILE = ROOT / "calendars" / "persian.ics"
START_YEAR = 1405
END_YEAR = 1410
DTSTAMP = "20261010T000000Z"
WEEKDAYS = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه", "شنبه", "یکشنبه"]
MONTHS = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
          "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]


def escape_ics(value: str) -> str:
    return value.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def fold_line(line: str) -> str:
    """Fold UTF-8 lines at the RFC 5545 75-octet limit."""
    chunks = []
    current = ""
    current_bytes = 0
    for char in line:
        encoded = char.encode("utf-8")
        if current_bytes + len(encoded) > 73:
            chunks.append(current)
            current = " " + char
            current_bytes = 1 + len(encoded)
        else:
            current += char
            current_bytes += len(encoded)
    chunks.append(current)
    return "\r\n".join(chunks)


def jalali_days(year: int):
    current = jdatetime.date(year, 1, 1)
    stop = jdatetime.date(year + 1, 1, 1)
    while current < stop:
        yield current
        current += jdatetime.timedelta(days=1)


def gregorian_to_jalali(gdate: date):
    return jdatetime.date.fromgregorian(date=gdate)


def main() -> None:
    data = json.loads(EVENTS_FILE.read_text(encoding="utf-8"))
    event_map = {}
    for event in data.get("events", []):
        event_map.setdefault(event["date"], []).append(event)

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//AliImor//Persian Calendar//FA",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:تقویم فارسی ایران",
        "X-WR-CALDESC:تاریخ شمسی روزانه همراه با تعطیلات و مناسبت‌های ثبت‌شده",
        "REFRESH-INTERVAL;VALUE=DURATION:PT12H",
    ]

    count = 0
    for year in range(START_YEAR, END_YEAR + 1):
        for jd in jalali_days(year):
            gdate = jd.togregorian()
            key = f"{jd.year:04d}/{jd.month:02d}/{jd.day:02d}"
            day_name = WEEKDAYS[gdate.weekday()]
            title = f"{day_name}، {jd.day} {MONTHS[jd.month - 1]}"
            description = f"تاریخ شمسی: {jd.year:04d}/{jd.month:02d}/{jd.day:02d}\nتاریخ میلادی: {gdate.isoformat()}"
            events = event_map.get(key, [])
            if events:
                labels = [e["title"] for e in events]
                title += " — " + " / ".join(labels)
                description += "\nمناسبت: " + " / ".join(labels)
                if any(e.get("category") == "official-holiday" for e in events):
                    description += "\nتعطیل رسمی طبق دادهٔ منبع"
            start = gdate.strftime("%Y%m%d")
            end = (gdate.fromordinal(gdate.toordinal() + 1)).strftime("%Y%m%d")
            uid = f"jalali-{jd.year}-{jd.month:02d}-{jd.day:02d}@persian-calendar.aliimor.github.io"
            lines.extend([
                "BEGIN:VEVENT",
                f"UID:{uid}",
                f"DTSTAMP:{DTSTAMP}",
                f"DTSTART;VALUE=DATE:{start}",
                f"DTEND;VALUE=DATE:{end}",
                f"SUMMARY:{escape_ics(title)}",
                f"DESCRIPTION:{escape_ics(description)}",
                "TRANSP:TRANSPARENT",
                "STATUS:CONFIRMED",
                "END:VEVENT",
            ])
            count += 1

    lines.append("END:VCALENDAR")
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text("\r\n".join(fold_line(line) for line in lines) + "\r\n", encoding="utf-8", newline="")
    print(f"Generated {count} all-day events in {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
