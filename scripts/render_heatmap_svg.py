from pathlib import Path
import json
from datetime import datetime


INPUT = Path("data/contributions.json")
OUTPUT = Path("contrib-heatmap.svg")


# --------------------------------------------------
# Configuration
# --------------------------------------------------

CELL = 13
GAP = 4

LEFT = 45
TOP = 35

WIDTH = 860
HEIGHT = 190

RADIUS = 3


# GitHub-style dark contribution levels
PALETTE = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
]


# --------------------------------------------------
# Load contribution data
# --------------------------------------------------

if not INPUT.exists():
    raise FileNotFoundError(
        f"Could not find {INPUT}"
    )


data = json.loads(
    INPUT.read_text(
        encoding="utf-8"
    )
)


days = data["days"]
stats = data["stats"]


# --------------------------------------------------
# Convert dates into lookup table
# --------------------------------------------------

contributions = {}

for day in days:

    contributions[day["date"]] = day["level"]


# --------------------------------------------------
# Find calendar range
# --------------------------------------------------

dates = [
    datetime.strptime(
        day["date"],
        "%Y-%m-%d"
    )
    for day in days
]

start = min(dates)
end = max(dates)


# Move backwards to Monday
start = start.replace(
    day=start.day
)

while start.weekday() != 0:

    from datetime import timedelta

    start -= timedelta(days=1)


# --------------------------------------------------
# SVG header
# --------------------------------------------------

svg = f'''<svg
xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">

<style>

.cell {{
    opacity: 0;
    animation: reveal 0.45s ease-out forwards;
}}

@keyframes reveal {{

    from {{
        opacity: 0;
        transform: translateY(-8px);
    }}

    to {{
        opacity: 1;
        transform: translateY(0);
    }}

}}

.label {{
    font-family: Arial, sans-serif;
    font-size: 11px;
    fill: #8b949e;
}}

.stat {{
    font-family: Arial, sans-serif;
    font-size: 12px;
    fill: #c9d1d9;
}}

</style>
'''


# --------------------------------------------------
# Month labels
# --------------------------------------------------

months_seen = set()
last_month_label_x = -100

month_names = [
    "Jan", "Feb", "Mar", "Apr",
    "May", "Jun", "Jul", "Aug",
    "Sep", "Oct", "Nov", "Dec"
]


# --------------------------------------------------
# Draw contribution cells
# --------------------------------------------------

from datetime import timedelta


current = start

week = 0

while current <= end:

    for weekday in range(7):

        date = current + timedelta(
            days=weekday
        )

        if date > end:
            continue

        date_string = date.strftime(
            "%Y-%m-%d"
        )

        level = contributions.get(
            date_string,
            0
        )

        level = max(
            0,
            min(level, 4)
        )

        x = LEFT + week * (
            CELL + GAP
        )

        y = TOP + weekday * (
            CELL + GAP
        )

        delay = (
            week * 0.025
            + weekday * 0.01
        )

        svg += f'''
<rect
    class="cell"
    x="{x}"
    y="{y}"
    width="{CELL}"
    height="{CELL}"
    rx="{RADIUS}"
    fill="{PALETTE[level]}"
    style="animation-delay:{delay:.3f}s">
<title>{date_string}: level {level}</title>
</rect>
'''

    # Month label
    month_key = (
        current.year,
        current.month
    )

    if month_key not in months_seen:

        months_seen.add(month_key)

        x = LEFT + week * (
            CELL + GAP
        )
        if x - last_month_label_x >= 45:
         svg += f'''
<text
    class="label"
    x="{x}"
    y="20">
    {month_names[current.month - 1]}
</text>
'''

    current += timedelta(days=7)

    week += 1


# --------------------------------------------------
# Legend
# --------------------------------------------------

legend_y = TOP + 7 * (
    CELL + GAP
) + 18

svg += f'''
<text
    class="label"
    x="{WIDTH - 160}"
    y="{legend_y + 11}">
    Less
</text>
'''


for i, color in enumerate(PALETTE):

    x = WIDTH - 125 + i * (
        CELL + 3
    )

    svg += f'''
<rect
    x="{x}"
    y="{legend_y}"
    width="{CELL}"
    height="{CELL}"
    rx="{RADIUS}"
    fill="{color}"/>
'''


svg += f'''
<text
    class="label"
    x="{WIDTH - 30}"
    y="{legend_y + 11}">
    More
</text>
'''


# --------------------------------------------------
# Statistics
# --------------------------------------------------

svg += f'''
<text
    class="stat"
    x="{LEFT}"
    y="{HEIGHT - 10}">
    {stats["active_days"]} active contribution days ·
    current streak: {stats["current_streak"]} ·
    longest streak: {stats["longest_streak"]}
</text>
'''


svg += "</svg>"


# --------------------------------------------------
# Save
# --------------------------------------------------

OUTPUT.write_text(
    svg,
    encoding="utf-8"
)


print("Heatmap generated!")
print(f"Saved: {OUTPUT}")