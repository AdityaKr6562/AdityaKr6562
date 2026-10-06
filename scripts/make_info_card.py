from pathlib import Path


OUTPUT = Path("info-card.svg")

WIDTH = 490
HEIGHT = 450

BG = "#0d1117"
BORDER = "#30363d"
TEXT = "#c9d1d9"
MUTED = "#8b949e"
ACCENT = "#58a6ff"
GREEN = "#3fb950"


lines = [
    ("header", "ADITYA@GITHUB", ACCENT),

    ("label", "LANGUAGES", MUTED),
    ("value", "Python · Java · C · C++", TEXT),

    ("label", "ML / AI", MUTED),
    ("value", "ML · DL · CV · NLP · CNNs", TEXT),

    ("label", "AI TECHNIQUES", MUTED),
    ("value", "TF-IDF · OCR · RAG · LLM Eval", TEXT),

    ("label", "FRAMEWORKS", MUTED),
    ("value", "PyTorch · TensorFlow · Keras", TEXT),

    ("label", "LIBRARIES", MUTED),
    ("value", "Scikit-learn · OpenCV · Pandas", TEXT),

    ("label", "WEB / DATABASE", MUTED),
    ("value", "HTML · CSS · JS · React · SQL", TEXT),

    ("label", "TOOLS", MUTED),
    ("value", "Git · GitHub · Linux · Ollama", TEXT),
]


svg = f'''<svg
xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">

<style>

.card {{
    fill: {BG};
    stroke: {BORDER};
    stroke-width: 1.5;
}}

.text {{
    font-family: "Courier New", monospace;
}}

.header {{
    font-size: 20px;
    font-weight: bold;
}}

.label {{
    font-size: 12px;
    font-weight: bold;
    letter-spacing: 1px;
}}

.value {{
    font-size: 15px;
}}

.line {{
    opacity: 0;
    animation: appear 0.45s ease-out forwards;
}}

@keyframes appear {{
    from {{
        opacity: 0;
        transform: translateX(-12px);
    }}

    to {{
        opacity: 1;
        transform: translateX(0);
    }}
}}

</style>

<rect
    class="card"
    x="1"
    y="1"
    width="{WIDTH - 2}"
    height="{HEIGHT - 2}"
    rx="10"/>

<circle cx="22" cy="24" r="5" fill="{GREEN}"/>

<text
    class="text header line"
    x="38"
    y="31"
    fill="{ACCENT}"
    style="animation-delay:0s">
    ADITYA@GITHUB
</text>

<line
    x1="20"
    y1="48"
    x2="470"
    y2="48"
    stroke="{BORDER}"/>

'''


y = 80
delay = 0.15

for kind, text, color in lines[1:]:

    if kind == "label":

        svg += f'''
<text
    class="text label line"
    x="25"
    y="{y}"
    fill="{color}"
    style="animation-delay:{delay:.2f}s">
    {text}
</text>
'''

        y += 22

    else:

        svg += f'''
<text
    class="text value line"
    x="25"
    y="{y}"
    fill="{color}"
    style="animation-delay:{delay:.2f}s">
    {text}
</text>
'''

        y += 34

    delay += 0.12


svg += """
</svg>
"""


OUTPUT.write_text(svg, encoding="utf-8")

print(f"Created {OUTPUT}")