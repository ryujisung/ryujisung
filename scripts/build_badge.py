#!/usr/bin/env python3
"""solved.ac 티어·스트릭 배지를 정적 SVG로 생성. 외부 폰트·애니메이션 없음 (GitHub camo에서도 렌더됨)."""
import json, sys, datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
show = json.loads((ROOT / "data/show.json").read_text())
grass = json.loads((ROOT / "data/grass.json").read_text())
today = dt.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else dt.date.today()

TIERS = [("Unrated", "#2d2d2d")] + [(n, c) for n, c in
         [("Bronze", "#ad5600"), ("Silver", "#435f7a"), ("Gold", "#ec9a00"),
          ("Platinum", "#27e2a4"), ("Diamond", "#00b4fc"), ("Ruby", "#ff0062")] for _ in range(5)]
ROMAN = ["", "V", "IV", "III", "II", "I"]
t = show["tier"]
tier_name, tier_color = (TIERS[t][0] + (" " + ROMAN[(t - 1) % 5 + 1] if t else ""), TIERS[t][1])

# grass: 날짜 -> 강도
vals = {}
for g in grass["grass"]:
    v = g["value"]
    vals[g["date"]] = v if isinstance(v, int) else 1
WEEKS, CELL, GAP = 17, 13, 3
start = today - dt.timedelta(days=today.weekday() + 1 + (WEEKS - 1) * 7)  # 일요일 시작
start -= dt.timedelta(days=(start.weekday() + 1) % 7)
def color(v):
    if v == 0: return "#ebedf0"
    return ["#9be9a8", "#40c463", "#30a14e", "#216e39"][min(3, (v - 1) // 2)]
cells = []
gx, gy = 22, 62
d = start
while d <= today:
    w = (d - start).days // 7
    r = (d - start).days % 7
    v = vals.get(d.isoformat(), 0)
    cells.append(f'<rect x="{gx + w*(CELL+GAP)}" y="{gy + r*(CELL+GAP)}" width="{CELL}" height="{CELL}" rx="3" fill="{color(v)}"><title>{d} · {v}</title></rect>')
    d += dt.timedelta(days=1)
W = gx*2 + WEEKS*(CELL+GAP) - GAP
H = gy + 7*(CELL+GAP) - GAP + 34
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Apple SD Gothic Neo', 'Malgun Gothic', 'Noto Sans KR', Helvetica, Arial, sans-serif"
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="#ffffff" stroke="#d0d7de"/>
<text x="{gx}" y="30" font-size="15" font-weight="700" fill="#1f2328">{show["handle"]}</text>
<text x="{W-gx}" y="30" font-size="14" font-weight="800" fill="{tier_color}" text-anchor="end">{tier_name}</text>
<text x="{gx}" y="49" font-size="11.5" fill="#57606a">rating <tspan font-weight="700" fill="#1f2328">{show["rating"]:,}</tspan>   solved <tspan font-weight="700" fill="#1f2328">{show["solvedCount"]:,}</tspan>   class <tspan font-weight="700" fill="#1f2328">{show["class"]}</tspan></text>
{"".join(cells)}
<text x="{gx}" y="{H-12}" font-size="11.5" fill="#57606a">current streak <tspan font-weight="700" fill="#1f2328">{grass["currentStreak"]}</tspan>   longest <tspan font-weight="700" fill="#1f2328">{grass["longestStreak"]}</tspan> days</text>
<text x="{W-gx}" y="{H-12}" font-size="10" fill="#8c959f" text-anchor="end">solved.ac · {today}</text>
</svg>
'''
out = ROOT / "badges/solved.svg"
out.write_text(svg)
print(f"wrote {out} ({W}x{H}) tier={tier_name}")
