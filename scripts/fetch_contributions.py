from pathlib import Path
import json
import re

import requests
from bs4 import BeautifulSoup


USERNAME = "AdityaKr6562"

URL = f"https://github.com/users/{USERNAME}/contributions"

OUTPUT = Path("data/contributions.json")


print(f"Fetching contributions for {USERNAME}...")

response = requests.get(
    URL,
    headers={
        "User-Agent": "Mozilla/5.0"
    },
    timeout=30,
)

response.raise_for_status()

print("GitHub response received.")


soup = BeautifulSoup(
    response.text,
    "html.parser"
)


days = []

for cell in soup.select("td.ContributionCalendar-day"):

    date = cell.get("data-date")
    count_text = cell.get("data-level")

    if not date:
        continue

    try:
        level = int(count_text or 0)
    except ValueError:
        level = 0

    days.append({
        "date": date,
        "level": level,
    })


if not days:
    raise RuntimeError(
        "No contribution cells found. "
        "GitHub's contribution HTML structure may have changed."
    )


# --------------------------------------------------
# Statistics
# --------------------------------------------------

total = len(days)

active_days = [
    day for day in days
    if day["level"] > 0
]


total_active = len(active_days)


# Current streak
current_streak = 0

for day in reversed(days):

    if day["level"] > 0:
        current_streak += 1
    else:
        break


# Longest streak
longest_streak = 0
streak = 0

for day in days:

    if day["level"] > 0:
        streak += 1
        longest_streak = max(
            longest_streak,
            streak
        )
    else:
        streak = 0


data = {
    "username": USERNAME,
    "days": days,
    "stats": {
        "calendar_days": total,
        "active_days": total_active,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
    },
}


OUTPUT.parent.mkdir(
    parents=True,
    exist_ok=True
)


OUTPUT.write_text(
    json.dumps(
        data,
        indent=2
    ),
    encoding="utf-8"
)


print()
print("Done!")
print(f"Days collected: {len(days)}")
print(f"Active days: {total_active}")
print(f"Current streak: {current_streak}")
print(f"Longest streak: {longest_streak}")
print(f"Saved: {OUTPUT}")
