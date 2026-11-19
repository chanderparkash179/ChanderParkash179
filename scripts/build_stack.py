"""Generate assets/stack.svg — three tilted elliptical orbits + chips."""
from __future__ import annotations

import math

from svg_common import (
    BLUE,
    ICONS,
    MUTED,
    NAVY,
    OFFWHITE,
    PROFILE,
    chip,
    dot_pattern,
    font_face_css,
    reduced_motion_css,
    xml_esc,
)


def _orbit_icon(slug: str, angle_deg: float, rx: float, ry: float, size: float, uid: str, orbit_id: str) -> str:
    a = math.radians(angle_deg)
    x = rx * math.cos(a)
    y = ry * math.sin(a)
    ic = ICONS[slug]
    fill = f"#{ic['hex']}"
    if ic["hex"].lower() in {"000000", "0f0f11", "181717"}:
        fill = OFFWHITE
    scale = (size * 0.46) / 24
    label = {
        "java": "Java",
        "amazonaws": "AWS",
        "microsoftazure": "Azure",
        "springboot": "Spring Boot",
        "nodedotjs": "NodeJS",
        "nodejs": "NodeJS",
    }.get(slug, ic["title"])
    return f"""
    <g transform="translate({x:.2f},{y:.2f})">
      <g class="{uid}-counter" data-orbit="{orbit_id}">
        <rect x="{-size/2:.1f}" y="{-size/2:.1f}" width="{size}" height="{size}" rx="{size*0.28:.1f}"
              fill="#0e162b" stroke="url(#{uid}-hair)" stroke-width="1.2"/>
        <g transform="translate({-size*0.23:.2f},{-size*0.23:.2f}) scale({scale:.4f})">
          <path d="{ic['path']}" fill="{fill}"/>
        </g>
        <text y="{size/2 + 14:.1f}" text-anchor="middle" fill="{OFFWHITE}" font-family="JBMonoEmbed, monospace" font-size="10">{xml_esc(label)}</text>
      </g>
    </g>"""


def build() -> str:
    uid = "stack"
    cx, cy = 300, 250
    height = 560

    outer = [("java", -20), ("nestjs", 100), ("docker", 220)]
    mid = [("springboot", 40), ("angular", 160), ("kubernetes", 280)]
    inner = [("amazonaws", 90), ("microsoftazure", 270)]

    def make_orbit(items, rx, ry, tilt, dur, oid, size):
        icons_s = "\n".join(
            _orbit_icon(slug, ang, rx, ry, size, uid, oid) for slug, ang in items
        )
        stroke = BLUE if oid != "b" else "#ff354f"
        return f"""
  <g transform="translate({cx},{cy}) rotate({tilt})">
    <ellipse cx="0" cy="0" rx="{rx}" ry="{ry}" fill="none" stroke="{stroke}" stroke-opacity="0.25" stroke-width="1.25" stroke-dasharray="5 7"/>
    <g id="{uid}-spin-{oid}" class="{uid}-orbit {uid}-orbit-{oid}">
      {icons_s}
      <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="{dur}s" begin="0s" repeatCount="indefinite"/>
    </g>
  </g>"""

    # Dense chip grid on the right — 3 columns
    chips = []
    y_cursor = 78
    colors = [BLUE, "#ff354f", BLUE, "#ff354f", BLUE]
    col_w, chip_h, gap = 118, 26, 8
    for gi, (group, labels) in enumerate(PROFILE["stack_groups"].items()):
        chips.append(
            f'<text x="560" y="{y_cursor}" fill="{colors[gi % len(colors)]}" font-family="JBMonoEmbed, monospace" font-size="12" font-weight="500">{xml_esc(group.upper())}</text>'
        )
        y_cursor += 14
        for li, lab in enumerate(labels):
            col = li % 3
            row = li // 3
            x = 560 + col * (col_w + gap)
            y = y_cursor + row * (chip_h + 8)
            # narrower chips
            chips.append(
                f"""
<g class="{uid}-chip" style="animation-delay:{0.3 + gi * 0.12 + li * 0.04:.2f}s">
  <rect x="{x}" y="{y}" width="{col_w}" height="{chip_h}" rx="13" fill="#101a31" stroke="url(#{uid}-hair)" stroke-width="1"/>
  <text x="{x + col_w/2:.1f}" y="{y + 17.5:.1f}" text-anchor="middle" fill="{OFFWHITE}" font-family="JBMonoEmbed, monospace" font-size="11">{xml_esc(lab)}</text>
</g>"""
            )
        rows = (len(labels) + 2) // 3
        y_cursor += rows * (chip_h + 8) + 22

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="1100" height="{height}" viewBox="0 0 1100 {height}" role="img" aria-label="Technology stack orbits">
  <title>Stack — Orbits and Platforms</title>
  {dot_pattern(uid)}
  <style><![CDATA[
{font_face_css()}
.{uid}-chip {{ opacity: 0; animation: {uid}-in 0.7s ease both; }}
.{uid}-title {{ opacity: 0; animation: {uid}-in 0.7s ease 0.1s both; }}
.{uid}-orbit-a {{ animation: {uid}-spin 28s linear infinite; transform-origin: 0 0; }}
.{uid}-orbit-b {{ animation: {uid}-spin-rev 22s linear infinite; transform-origin: 0 0; }}
.{uid}-orbit-c {{ animation: {uid}-spin 16s linear infinite; transform-origin: 0 0; }}
@keyframes {uid}-in {{
  from {{ opacity: 0; transform: translateY(10px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes {uid}-spin {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
@keyframes {uid}-spin-rev {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(-360deg); }} }}
{reduced_motion_css(f'.{uid}-chip, .{uid}-title, .{uid}-orbit-a, .{uid}-orbit-b, .{uid}-orbit-c')}
@media (prefers-reduced-motion: reduce) {{
  .{uid}-chip, .{uid}-title {{ opacity: 1 !important; }}
}}
  ]]></style>

  <rect width="1100" height="{height}" rx="28" fill="{NAVY}"/>
  <rect width="1100" height="{height}" rx="28" fill="url(#{uid}-dots)" opacity="0.5"/>
  <rect x="1.5" y="1.5" width="1097" height="{height - 3}" rx="26.5" fill="none" stroke="url(#{uid}-hair)" stroke-width="1.5"/>

  <g class="{uid}-title">
    <text x="48" y="48" fill="{BLUE}" font-family="JBMonoEmbed, monospace" font-size="14" font-weight="500">STACK</text>
    <text x="48" y="82" fill="{OFFWHITE}" font-family="SyneEmbed, sans-serif" font-weight="700" font-size="32">Orbiting toolkit</text>
  </g>

  <circle cx="{cx}" cy="{cy}" r="26" fill="#101a31" stroke="url(#{uid}-hair)" stroke-width="1.4"/>
  <text x="{cx}" y="{cy + 5}" text-anchor="middle" fill="{OFFWHITE}" font-family="SyneEmbed, sans-serif" font-weight="700" font-size="11">CORE</text>

  {make_orbit(outer, 175, 108, -18, 28, 'a', 40)}
  {make_orbit(mid, 122, 74, 12, 22, 'b', 36)}
  {make_orbit(inner, 72, 44, -8, 16, 'c', 34)}

  <g>{''.join(chips)}</g>

  <text x="560" y="{height - 28}" fill="{MUTED}" font-family="JBMonoEmbed, monospace" font-size="11">Icons: Simple Icons (CC0) · AWS/Azure/LinkedIn from SI 9.19.0</text>
</svg>
"""


if __name__ == "__main__":
    from pathlib import Path

    out = Path(__file__).resolve().parents[1] / "assets" / "stack.svg"
    out.write_text(build(), encoding="utf-8")
    print("wrote", out, out.stat().st_size)
