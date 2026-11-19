"""Generate assets/about-life.svg"""
from __future__ import annotations

from svg_common import (
    BLUE,
    CRIMSON,
    MUTED,
    NAVY,
    OFFWHITE,
    PROFILE,
    dot_pattern,
    font_face_css,
    reduced_motion_css,
    xml_esc,
)


def build() -> str:
    uid = "about"
    p = PROFILE
    caps = p["capabilities"]
    interests = p["interests"]

    cap_rows = []
    for i, c in enumerate(caps):
        y = 118 + i * 38
        delay = 0.35 + i * 0.08
        cap_rows.append(
            f"""
      <g class="{uid}-cap" style="animation-delay:{delay:.2f}s">
        <rect x="48" y="{y}" width="420" height="32" rx="10" fill="#101a31" stroke="url(#{uid}-hair)" stroke-width="1"/>
        <circle cx="68" cy="{y+16}" r="5" fill="{BLUE if i % 2 == 0 else CRIMSON}"/>
        <text x="86" y="{y+21}" fill="{OFFWHITE}" font-family="JBMonoEmbed, monospace" font-size="14">{xml_esc(c)}</text>
      </g>"""
        )

    slides = []
    for i, it in enumerate(interests):
        desc = "\n".join(
            f'<tspan x="580" dy="{0 if li == 0 else 20}">{xml_esc(line)}</tspan>'
            for li, line in enumerate(it["lines"])
        )
        slides.append(
            f"""
      <g class="{uid}-slide {uid}-slide-{i}" clip-path="url(#{uid}-interest-clip)">
        <text x="580" y="186" fill="{OFFWHITE}" font-family="SyneEmbed, sans-serif" font-weight="700" font-size="40">{xml_esc(it['title'])}</text>
        <text x="580" y="228" fill="{MUTED}" font-family="JBMonoEmbed, monospace" font-size="14">
          {desc}
        </text>
      </g>"""
        )

    # 3 segments, 4s each = 12s
    bars = []
    for i in range(3):
        x = 580 + i * 118
        bars.append(
            f"""
      <g>
        <rect x="{x}" y="280" width="104" height="6" rx="3" fill="#1a243c"/>
        <rect class="{uid}-bar {uid}-bar-{i}" x="{x}" y="280" width="104" height="6" rx="3" fill="{BLUE if i != 1 else CRIMSON}"/>
      </g>"""
        )

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="380" viewBox="0 0 1100 380" role="img"
     aria-label="Capabilities and interests">
  <title>About — Capabilities and Life</title>
  {dot_pattern(uid)}
  <style><![CDATA[
{font_face_css()}
.{uid}-cap {{ opacity: 0; animation: {uid}-in 0.7s ease both; }}
.{uid}-panel {{ opacity: 0; animation: {uid}-in 0.8s ease 0.25s both; }}
.{uid}-slide {{ opacity: 0; animation: {uid}-carousel 12s linear infinite; }}
.{uid}-slide-0 {{ animation-delay: 0s; }}
.{uid}-slide-1 {{ animation-delay: -4s; }}
.{uid}-slide-2 {{ animation-delay: -8s; }}
.{uid}-bar {{
  transform-box: fill-box;
  transform-origin: left center;
  animation: {uid}-progress 12s linear infinite;
}}
.{uid}-bar-0 {{ animation-delay: 0s; }}
.{uid}-bar-1 {{ animation-delay: -4s; }}
.{uid}-bar-2 {{ animation-delay: -8s; }}
@keyframes {uid}-in {{
  from {{ opacity: 0; transform: translateY(12px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes {uid}-carousel {{
  0%, 1% {{ opacity: 0; transform: translateY(14px); }}
  4%, 31% {{ opacity: 1; transform: translateY(0); }}
  33.3%, 100% {{ opacity: 0; transform: translateY(-12px); }}
}}
@keyframes {uid}-progress {{
  0% {{ transform: scaleX(0); opacity: 1; }}
  33.3% {{ transform: scaleX(1); opacity: 1; }}
  33.31%, 100% {{ transform: scaleX(0); opacity: 0.35; }}
}}
{reduced_motion_css(f'.{uid}-cap, .{uid}-panel, .{uid}-slide, .{uid}-bar')}
@media (prefers-reduced-motion: reduce) {{
  .{uid}-slide-0, .{uid}-cap, .{uid}-panel {{ opacity: 1 !important; transform: none !important; }}
  .{uid}-bar {{ transform: scaleX(1) !important; opacity: 0.5 !important; animation: none !important; }}
}}
  ]]></style>

  <rect width="1100" height="380" rx="28" fill="{NAVY}"/>
  <rect width="1100" height="380" rx="28" fill="url(#{uid}-dots)" opacity="0.5"/>
  <rect x="1.5" y="1.5" width="1097" height="377" rx="26.5" fill="none" stroke="url(#{uid}-hair)" stroke-width="1.5"/>

  <text x="48" y="64" fill="{BLUE}" font-family="JBMonoEmbed, monospace" font-size="14" font-weight="500">CAPABILITIES</text>
  <text x="48" y="96" fill="{OFFWHITE}" font-family="SyneEmbed, sans-serif" font-weight="700" font-size="34">What I ship</text>
  {''.join(cap_rows)}

  <g class="{uid}-panel">
    <defs>
      <clipPath id="{uid}-interest-clip">
        <rect x="560" y="148" width="468" height="120" rx="8"/>
      </clipPath>
    </defs>
    <rect x="540" y="56" width="512" height="268" rx="22" fill="url(#{uid}-card)" stroke="url(#{uid}-hair)" stroke-width="1.3"/>
    <text x="580" y="100" fill="{CRIMSON}" font-family="JBMonoEmbed, monospace" font-size="14" font-weight="500">INTERESTS</text>
    <text x="580" y="132" fill="{MUTED}" font-family="JBMonoEmbed, monospace" font-size="13">Rotates every 4 seconds</text>
    <!-- Base slide for no-CSS fallback -->
    <text x="580" y="186" fill="{OFFWHITE}" font-family="SyneEmbed, sans-serif" font-weight="700" font-size="40" opacity="0.18">{xml_esc(interests[0]['title'])}</text>
    {''.join(slides)}
    {''.join(bars)}
    <text x="580" y="312" fill="{MUTED}" font-family="JBMonoEmbed, monospace" font-size="12">01 Cricket   ·   02 Badminton   ·   03 Coding</text>
  </g>

  <!-- SMIL progress sync from 0s -->
  <rect x="580" y="280" width="0" height="6" rx="3" fill="{BLUE}" opacity="0">
    <animate attributeName="width" values="0;104;104;0;0" keyTimes="0;0.333;0.333;0.334;1" dur="12s" begin="0s" repeatCount="indefinite"/>
  </rect>
</svg>
"""


if __name__ == "__main__":
    from pathlib import Path

    out = Path(__file__).resolve().parents[1] / "assets" / "about-life.svg"
    out.write_text(build(), encoding="utf-8")
    print("wrote", out, out.stat().st_size)
