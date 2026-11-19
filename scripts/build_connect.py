"""Generate assets/connect.svg — pointing character + social cards."""
from __future__ import annotations

from svg_common import (
    BLUE,
    CRIMSON,
    ICONS,
    MUTED,
    NAVY,
    OFFWHITE,
    POINT_PNG,
    PROFILE,
    dot_pattern,
    font_face_css,
    reduced_motion_css,
    xml_esc,
)


def social_card(i: int, s: dict, uid: str) -> str:
    y = 96 + i * 54
    delay = 0.35 + i * 0.08
    ic = ICONS[s["key"]]
    fill = f"#{ic['hex']}"
    if ic["hex"].lower() in {"000000", "0f0f11", "181717"}:
        fill = OFFWHITE
    return f"""
  <g class="{uid}-card" style="animation-delay:{delay:.2f}s">
    <rect x="500" y="{y}" width="548" height="48" rx="14" fill="#101a31" stroke="url(#{uid}-hair)" stroke-width="1.2"/>
    <rect x="512" y="{y + 6}" width="36" height="36" rx="10" fill="#0a1224"/>
    <g transform="translate(518 {y + 12}) scale(0.85)">
      <path d="{ic['path']}" fill="{fill}"/>
    </g>
    <text x="564" y="{y + 20}" fill="{OFFWHITE}" font-family="SyneEmbed, sans-serif" font-weight="700" font-size="15">{xml_esc(s['label'])}</text>
    <text x="564" y="{y + 36}" fill="{MUTED}" font-family="JBMonoEmbed, monospace" font-size="11">{xml_esc(s['handle'])}</text>
    <g class="{uid}-nudge" style="animation-delay:{delay + 0.15:.2f}s">
      <path d="M1000 {y + 24} h14" stroke="{BLUE}" stroke-width="2" stroke-linecap="round"/>
      <path d="M1008 {y + 16} l10 8 -10 8" fill="none" stroke="{CRIMSON}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </g>
  </g>"""


def build() -> str:
    uid = "connect"
    n = len(PROFILE["socials"])
    height = max(520, 96 + n * 54 + 36)
    cards = "\n".join(social_card(i, s, uid) for i, s in enumerate(PROFILE["socials"]))

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="1100" height="{height}" viewBox="0 0 1100 {height}" role="img"
     aria-label="Connect with Chander Parkash">
  <title>Connect — Social</title>
  {dot_pattern(uid)}
  <style><![CDATA[
{font_face_css()}
.{uid}-char {{ opacity: 0; animation: {uid}-in 0.9s cubic-bezier(.2,.8,.2,1) 0.15s both; }}
.{uid}-title {{ opacity: 0; animation: {uid}-in 0.7s ease 0.05s both; }}
.{uid}-card {{ opacity: 0; animation: {uid}-slide 0.75s cubic-bezier(.2,.8,.2,1) both; }}
.{uid}-nudge {{ animation: {uid}-nudge 1.4s ease-in-out infinite; }}
@keyframes {uid}-in {{
  from {{ opacity: 0; transform: translateX(-16px); }}
  to {{ opacity: 1; transform: translateX(0); }}
}}
@keyframes {uid}-slide {{
  from {{ opacity: 0; transform: translateX(24px); }}
  to {{ opacity: 1; transform: translateX(0); }}
}}
@keyframes {uid}-nudge {{
  0%, 100% {{ transform: translateX(0); }}
  50% {{ transform: translateX(6px); }}
}}
{reduced_motion_css(f'.{uid}-char, .{uid}-title, .{uid}-card, .{uid}-nudge')}
@media (prefers-reduced-motion: reduce) {{
  .{uid}-char, .{uid}-title, .{uid}-card {{ opacity: 1 !important; transform: none !important; }}
}}
  ]]></style>

  <rect width="1100" height="{height}" rx="28" fill="{NAVY}"/>
  <rect width="1100" height="{height}" rx="28" fill="url(#{uid}-dots)" opacity="0.5"/>
  <rect x="1.5" y="1.5" width="1097" height="{height - 3}" rx="26.5" fill="none" stroke="url(#{uid}-hair)" stroke-width="1.5"/>

  <g class="{uid}-title">
    <text x="500" y="42" fill="{BLUE}" font-family="JBMonoEmbed, monospace" font-size="14" font-weight="500">CONNECT</text>
    <text x="500" y="74" fill="{OFFWHITE}" font-family="SyneEmbed, sans-serif" font-weight="700" font-size="26">Let's talk systems</text>
  </g>

  <g class="{uid}-char">
    <image x="16" y="90" width="460" height="256"
           href="data:image/png;base64,{POINT_PNG}" xlink:href="data:image/png;base64,{POINT_PNG}"
           preserveAspectRatio="xMidYMid meet"/>
    <text x="40" y="{height - 48}" fill="{MUTED}" font-family="JBMonoEmbed, monospace" font-size="13">Pointing you to the right places →</text>
    <text x="40" y="{height - 26}" fill="{MUTED}" font-family="JBMonoEmbed, monospace" font-size="12">Links are clickable below this image on GitHub.</text>
  </g>

  {cards}

  <circle cx="1040" cy="36" r="26" fill="{BLUE}" opacity="0.1">
    <animate attributeName="opacity" values="0.06;0.16;0.06" keyTimes="0;0.5;1" dur="3.2s" begin="0s" repeatCount="indefinite"/>
  </circle>
</svg>
"""


if __name__ == "__main__":
    from pathlib import Path

    out = Path(__file__).resolve().parents[1] / "assets" / "connect.svg"
    out.write_text(build(), encoding="utf-8")
    print("wrote", out, out.stat().st_size)
