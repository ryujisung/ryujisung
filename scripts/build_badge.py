#!/usr/bin/env python3
"""solved.ac 요약 카드를 정적 SVG로 만든다. 외부 폰트나 애니메이션이 없어서 GitHub에서도 그대로 보인다.

data/show.json : https://solved.ac/api/v3/user/show?handle=<핸들>
data/grass.json: https://solved.ac/api/v3/user/grass?handle=<핸들>&topic=default
두 파일을 새로 받은 뒤 이 스크립트를 실행하면 badges/solved.svg, badges/solved-dark.svg가 갱신된다.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
show = json.loads((ROOT / "data/show.json").read_text())
grass = json.loads((ROOT / "data/grass.json").read_text())

TIERS = [("Unrated", "#2d2d2d")] + [(n, c) for n, c in
         [("Bronze", "#ad5600"), ("Silver", "#435f7a"), ("Gold", "#ec9a00"),
          ("Platinum", "#27e2a4"), ("Diamond", "#00b4fc"), ("Ruby", "#ff0062")] for _ in range(5)]
ROMAN = ["", "V", "IV", "III", "II", "I"]
t = show["tier"]
tier_name = TIERS[t][0] + (" " + ROMAN[(t - 1) % 5 + 1] if t else "")
tier_color = TIERS[t][1]
longest = max(show.get("maxStreak", 0), grass.get("longestStreak", 0))

FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Apple SD Gothic Neo', 'Malgun Gothic', 'Noto Sans KR', Helvetica, Arial, sans-serif"
THEMES = {
    "solved.svg": dict(bg="#ffffff", line="#d0d7de", title="#1f2328", sub="#57606a", mute="#8c959f"),
    "solved-dark.svg": dict(bg="#0d1117", line="#30363d", title="#e6edf3", sub="#8b949e", mute="#6e7681"),
}
W, H = 460, 104
STATS = [("레이팅", f'{show["rating"]:,}'), ("푼 문제", f'{show["solvedCount"]:,}'),
         ("클래스", str(show["class"])), ("최장 스트릭", f"{longest}일")]

for name, c in THEMES.items():
    cols = []
    for i, (label, value) in enumerate(STATS):
        x = 24 + i * 108
        cols.append(f'<text x="{x}" y="66" font-size="11" fill="{c["sub"]}">{label}</text>'
                    f'<text x="{x}" y="86" font-size="16" font-weight="700" fill="{c["title"]}">{value}</text>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}" role="img" aria-label="solved.ac {tier_name}">
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10" fill="{c["bg"]}" stroke="{c["line"]}"/>
<rect x="24" y="19" width="4" height="18" rx="2" fill="{tier_color}"/>
<text x="36" y="34" font-size="16" font-weight="800" fill="{tier_color}">{tier_name}</text>
<text x="{W-24}" y="33" font-size="12" fill="{c["mute"]}" text-anchor="end">solved.ac · {show["handle"]}</text>
{"".join(cols)}
</svg>
'''
    (ROOT / "badges" / name).write_text(svg)
    print(f"wrote badges/{name} ({W}x{H}) tier={tier_name}")
