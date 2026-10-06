from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from rembg import remove


# --------------------------------------------------
# Configuration
# --------------------------------------------------

INPUT = Path("assets/source-photo.jpg")
OUTPUT = Path("assets/source-prepped.png")

PADDING = 40


# --------------------------------------------------
# 1. Check input
# --------------------------------------------------

if not INPUT.exists():
    raise FileNotFoundError(
        f"Could not find {INPUT}. "
        "Place your original photo at assets/source-photo.jpg"
    )


# --------------------------------------------------
# 2. Remove background
# --------------------------------------------------

print("[1/4] Removing background...")

image = Image.open(INPUT).convert("RGBA")

foreground = remove(image)

foreground.save("assets/debug-foreground.png")


# --------------------------------------------------
# 3. Crop around the person
# --------------------------------------------------

print("[2/4] Cropping subject...")

rgba = np.array(foreground)

alpha = rgba[:, :, 3]

ys, xs = np.where(alpha > 20)

if len(xs) == 0:
    raise RuntimeError("No foreground subject detected.")

x1 = max(0, xs.min() - PADDING)
y1 = max(0, ys.min() - PADDING)
x2 = min(rgba.shape[1], xs.max() + PADDING)
y2 = min(rgba.shape[0], ys.max() + PADDING)

cropped = rgba[y1:y2, x1:x2]


# --------------------------------------------------
# 4. Composite onto white + improve contrast
# --------------------------------------------------

print("[3/4] Creating grayscale portrait...")

rgb = cropped[:, :, :3]
alpha = cropped[:, :, 3:4] / 255.0

white = np.full_like(rgb, 255)

composited = (
    rgb * alpha +
    white * (1 - alpha)
).astype(np.uint8)


gray = cv2.cvtColor(composited, cv2.COLOR_RGB2GRAY)


# Local contrast enhancement
clahe = cv2.createCLAHE(
    clipLimit=2.0,
    tileGridSize=(8, 8)
)

enhanced = clahe.apply(gray)


# --------------------------------------------------
# 5. Save result
# --------------------------------------------------

print("[4/4] Saving prepared image...")

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

cv2.imwrite(str(OUTPUT), enhanced)

print()
print(f"Done!")
print(f"Saved: {OUTPUT}")