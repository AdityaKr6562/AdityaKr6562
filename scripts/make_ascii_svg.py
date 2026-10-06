from pathlib import Path
from PIL import Image


# --------------------------------------------------
# Configuration
# --------------------------------------------------

INPUT = Path("assets/source-prepped.png")
OUTPUT = Path("aditya-ascii.svg")

# Number of ASCII characters horizontally
WIDTH = 80

# ASCII ramp:
# bright pixels -> sparse characters
# dark pixels   -> dense characters
RAMP = "@%#sc*+=-:`. "

# Visual settings
FONT_SIZE = 10
CHAR_WIDTH = 6.0
LINE_HEIGHT = 11

# Animation
ROW_DELAY = 0.025
ROW_DURATION = 0.35


# --------------------------------------------------
# Check input
# --------------------------------------------------

if not INPUT.exists():
    raise FileNotFoundError(
        f"Could not find {INPUT}"
    )


# --------------------------------------------------
# Load image
# --------------------------------------------------

print("[1/4] Loading image...")

image = Image.open(INPUT).convert("L")

original_width, original_height = image.size

# Characters are taller than they are wide.
# This correction prevents the portrait from looking stretched.
aspect_ratio = original_height / original_width

height = max(
    1,
    int(WIDTH * aspect_ratio * 0.50)
)

image = image.resize(
    (WIDTH, height)
)


# --------------------------------------------------
# Convert pixels to ASCII
# --------------------------------------------------

print("[2/4] Converting pixels to ASCII...")

pixels = list(image.getdata())

rows = []

for y in range(height):

    row = ""

    for x in range(WIDTH):

        brightness = pixels[y * WIDTH + x]

        # Convert 0-255 brightness into
        # an index in our ASCII ramp.
        index = int(
            brightness / 255 * (len(RAMP) - 1)
        )

        row += RAMP[index]

    rows.append(row)


# --------------------------------------------------
# Build SVG
# --------------------------------------------------

print("[3/4] Building SVG...")

svg_width = WIDTH * CHAR_WIDTH
svg_height = height * LINE_HEIGHT


svg = f'''<svg
xmlns="http://www.w3.org/2000/svg"
width="{svg_width}"
height="{svg_height}"
viewBox="0 0 {svg_width} {svg_height}">

<style>
.ascii {{
    font-family: "Courier New", monospace;
    font-size: {FONT_SIZE}px;
    font-weight: bold;
    fill: #c9d1d9;
}}

.row {{
    opacity: 0;
    clip-path: inset(0 100% 0 0);
    animation:
        typeRow {ROW_DURATION}s
        cubic-bezier(.2,.8,.2,1)
        forwards;
}}

@keyframes typeRow {{
    0% {{
        opacity: 0;
        clip-path: inset(0 100% 0 0);
    }}

    10% {{
        opacity: 1;
    }}

    100% {{
        opacity: 1;
        clip-path: inset(0 0 0 0);
    }}
}}
</style>
'''


# --------------------------------------------------
# Add rows
# --------------------------------------------------

for row_number, row in enumerate(rows):

    y = (row_number + 1) * LINE_HEIGHT

    delay = row_number * ROW_DELAY

    # Escape XML-sensitive characters
    row = (
        row
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )

    svg += f'''
<text
    xml:space="preserve"
    class="ascii row"
    x="0"
    y="{y}"
    style="animation-delay:{delay:.3f}s">
    {row}
</text>
'''


# --------------------------------------------------
# Finish SVG
# --------------------------------------------------

svg += "</svg>"


OUTPUT.write_text(
    svg,
    encoding="utf-8"
)


print("[4/4] Done!")
print(f"Saved: {OUTPUT}")
print(f"ASCII size: {WIDTH} x {height}")