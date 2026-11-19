"""Generate assets/id-dashboard.svg — hanging lanyard ID with pendulum motion."""
from __future__ import annotations

from svg_common import (
    BLUE,
    CRIMSON,
    ID_PNG,
    MUTED,
    NAVY,
    OFFWHITE,
    PROFILE,
    dot_pattern,
    font_face_css,
    reduced_motion_css,
    xml_esc,
)


def barcode(x: float, y: float, w: float = 200, h: float = 36) -> str:
    seed = "chanderparkash179"
    bars = []
    cx = x
    i = 0
    while cx < x + w - 2:
        bit = (ord(seed[i % len(seed)]) + i * 7) % 5
        bw = 1.2 + (bit % 3) * 1.1
        if bit != 2:
            bars.append(
                f'<rect x="{cx:.2f}" y="{y}" width="{bw:.2f}" height="{h}" fill="#0b1020"/>'
            )
        cx += bw + 0.9
        i += 1
    return "\n".join(bars)


def build() -> str:
    uid = "idcard"
    p = PROFILE
    m = p["metrics"]
    pivot_x, pivot_y = 560, 42

    # Wider card so role/handle stay inside bounds
    card_x, card_y, card_w, card_h = 360, 112, 400, 372
    photo_x, photo_y, photo_s = 384, 168, 108
    text_x = 508
    text_max = card_x + card_w - 24  # right padding

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="1100" height="520" viewBox="0 0 1100 520" role="img"
     aria-label="Employee ID dashboard for {xml_esc(p['name'])}">
  <title>ID Dashboard — {xml_esc(p['name'])}</title>
  {dot_pattern(uid)}
  <defs>
    <linearGradient id="{uid}-metal" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#d7deea"/>
      <stop offset="45%" stop-color="#8e9bb3"/>
      <stop offset="100%" stop-color="#e8eef8"/>
    </linearGradient>
    <linearGradient id="{uid}-foil" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{OFFWHITE}" stop-opacity="0"/>
      <stop offset="45%" stop-color="{OFFWHITE}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{OFFWHITE}" stop-opacity="0.35"/>
      <stop offset="55%" stop-color="{OFFWHITE}" stop-opacity="0"/>
      <stop offset="100%" stop-color="{OFFWHITE}" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="{uid}-card-clip">
      <rect x="{card_x}" y="{card_y}" width="{card_w}" height="{card_h}" rx="22"/>
    </clipPath>
    <clipPath id="{uid}-photo-clip">
      <rect x="{photo_x}" y="{photo_y}" width="{photo_s}" height="{photo_s}" rx="14"/>
    </clipPath>
  </defs>
  <style><![CDATA[
{font_face_css()}
.{uid}-stage {{
  transform-origin: {pivot_x}px {pivot_y}px;
  animation: {uid}-pendulum 5.6s cubic-bezier(.22,.9,.28,1) both,
             {uid}-swing 4.8s ease-in-out 5.6s infinite;
}}
@keyframes {uid}-pendulum {{
  0% {{ transform: translateY(-220px) rotate(-14deg); opacity: 0; }}
  18% {{ opacity: 1; }}
  42% {{ transform: translateY(8px) rotate(7deg); }}
  58% {{ transform: translateY(-2px) rotate(-3.2deg); }}
  72% {{ transform: translateY(2px) rotate(1.8deg); }}
  100% {{ transform: translateY(0) rotate(0deg); }}
}}
@keyframes {uid}-swing {{
  0% {{ transform: rotate(-1.7deg); }}
  50% {{ transform: rotate(1.7deg); }}
  100% {{ transform: rotate(-1.7deg); }}
}}
.{uid}-foil {{
  animation: {uid}-sweep 4.5s ease-in-out 1.2s infinite;
}}
@keyframes {uid}-sweep {{
  0% {{ transform: translateX(-220px); opacity: 0; }}
  12% {{ opacity: 1; }}
  45% {{ transform: translateX(280px); opacity: 1; }}
  55%, 100% {{ transform: translateX(340px); opacity: 0; }}
}}
.{uid}-meta {{ opacity: 0; animation: {uid}-fade 0.8s ease 0.9s both; }}
@keyframes {uid}-fade {{
  from {{ opacity: 0; transform: translateY(8px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}
{reduced_motion_css(f'.{uid}-stage, .{uid}-foil, .{uid}-meta')}
@media (prefers-reduced-motion: reduce) {{
  .{uid}-stage {{ transform: none !important; opacity: 1 !important; animation: none !important; }}
  .{uid}-meta {{ opacity: 1 !important; }}
}}
  ]]></style>

  <rect width="1100" height="520" rx="28" fill="{NAVY}"/>
  <rect width="1100" height="520" rx="28" fill="url(#{uid}-dots)" opacity="0.45"/>
  <rect x="1.5" y="1.5" width="1097" height="517" rx="26.5" fill="none" stroke="url(#{uid}-hair)" stroke-width="1.5"/>

  <text x="48" y="56" fill="{BLUE}" font-family="JBMonoEmbed, monospace" font-size="14" font-weight="500">CREDENTIALS</text>
  <text x="48" y="96" fill="{OFFWHITE}" font-family="SyneEmbed, sans-serif" font-weight="700" font-size="34">ID Dashboard</text>

  <g class="{uid}-meta">
    <text x="48" y="150" fill="{MUTED}" font-family="JBMonoEmbed, monospace" font-size="13">Verified public GitHub metrics only</text>
    <text x="48" y="188" fill="{OFFWHITE}" font-family="SyneEmbed, sans-serif" font-weight="600" font-size="22">Public repos</text>
    <text x="48" y="228" fill="{BLUE}" font-family="SyneEmbed, sans-serif" font-weight="700" font-size="48">{m['repos']}</text>
    <text x="48" y="278" fill="{OFFWHITE}" font-family="SyneEmbed, sans-serif" font-weight="600" font-size="22">Followers</text>
    <text x="48" y="318" fill="{CRIMSON}" font-family="SyneEmbed, sans-serif" font-weight="700" font-size="48">{m['followers']}</text>
    <text x="48" y="368" fill="{MUTED}" font-family="JBMonoEmbed, monospace" font-size="14">Joined GitHub {m['joined']}</text>
    <text x="48" y="394" fill="{MUTED}" font-family="JBMonoEmbed, monospace" font-size="14">Snapshot as of {m['as_of']}</text>
    <text x="48" y="430" fill="{MUTED}" font-family="JBMonoEmbed, monospace" font-size="12">Unknown private totals omitted.</text>
  </g>

  <rect x="480" y="28" width="160" height="10" rx="4" fill="#1a243c" stroke="url(#{uid}-hair)" stroke-width="1"/>

  <g class="{uid}-stage">
    <path d="M520 38 C530 70, 510 95, 500 112" fill="none" stroke="{CRIMSON}" stroke-width="6" stroke-linecap="round"/>
    <path d="M600 38 C590 70, 610 95, 620 112" fill="none" stroke="{BLUE}" stroke-width="6" stroke-linecap="round"/>

    <g transform="translate({pivot_x - 18},{pivot_y})">
      <rect x="0" y="0" width="36" height="22" rx="4" fill="url(#{uid}-metal)"/>
      <rect x="10" y="6" width="16" height="10" rx="2" fill="#6b768c"/>
      <circle cx="18" cy="26" r="5" fill="url(#{uid}-metal)" stroke="#9aa6c3" stroke-width="1"/>
    </g>

    <g id="{uid}-badge">
      <rect x="{card_x}" y="{card_y}" width="{card_w}" height="{card_h}" rx="22" fill="#f4f6fb"/>
      <rect x="{card_x}" y="{card_y}" width="{card_w}" height="48" rx="22" fill="#0c1428"/>
      <rect x="{card_x}" y="{card_y + 28}" width="{card_w}" height="20" fill="#0c1428"/>
      <text x="{card_x + card_w/2}" y="{card_y + 32}" text-anchor="middle" fill="{OFFWHITE}" font-family="JBMonoEmbed, monospace" font-size="11" font-weight="500">SYSTEMS LTD.  ·  EMPLOYEE ID</text>

      <image x="{photo_x}" y="{photo_y}" width="{photo_s}" height="{photo_s}" clip-path="url(#{uid}-photo-clip)"
             href="data:image/png;base64,{ID_PNG}" xlink:href="data:image/png;base64,{ID_PNG}" preserveAspectRatio="xMidYMid slice"/>

      <text x="{text_x}" y="188" fill="#0b1020" font-family="SyneEmbed, sans-serif" font-weight="700" font-size="17">{xml_esc(p['name'].split()[0])}</text>
      <text x="{text_x}" y="208" fill="#0b1020" font-family="SyneEmbed, sans-serif" font-weight="700" font-size="17">{xml_esc(p['name'].split()[1])}</text>
      <text x="{text_x}" y="232" fill="#3a4660" font-family="JBMonoEmbed, monospace" font-size="10">Senior Software</text>
      <text x="{text_x}" y="246" fill="#3a4660" font-family="JBMonoEmbed, monospace" font-size="10">Engineer</text>
      <text x="{text_x}" y="266" fill="#3a4660" font-family="JBMonoEmbed, monospace" font-size="10">{xml_esc(p['company'])}</text>
      <text x="{text_x}" y="284" fill="#5a6884" font-family="JBMonoEmbed, monospace" font-size="10">{xml_esc(p['location'])}</text>
      <text x="{text_x}" y="300" fill="#5a6884" font-family="JBMonoEmbed, monospace" font-size="10">@{xml_esc(p['github'])}</text>

      <rect x="{card_x + 24}" y="322" width="{card_w - 48}" height="1" fill="#d5dbe8"/>
      <text x="{card_x + 24}" y="346" fill="#3a4660" font-family="JBMonoEmbed, monospace" font-size="11">REPOS {m['repos']}   ·   FOLLOWERS {m['followers']}</text>
      <text x="{card_x + 24}" y="364" fill="#5a6884" font-family="JBMonoEmbed, monospace" font-size="11">MEMBER SINCE {m['joined'].upper()}</text>

      <g>{barcode(card_x + 24, 380, card_w - 48, 36)}</g>
      <text x="{card_x + 24}" y="440" fill="#5a6884" font-family="JBMonoEmbed, monospace" font-size="10">CP-{p['github'][:6].upper()}-179</text>
      <text x="{card_x + card_w - 24}" y="440" text-anchor="end" fill="#5a6884" font-family="JBMonoEmbed, monospace" font-size="10">{m['as_of']}</text>

      <g clip-path="url(#{uid}-card-clip)">
        <rect class="{uid}-foil" x="{card_x}" y="{card_y}" width="90" height="{card_h}" fill="url(#{uid}-foil)"/>
      </g>
    </g>

    <animateTransform attributeName="transform" type="rotate"
      values="-14 {pivot_x} {pivot_y}; 7 {pivot_x} {pivot_y}; -3.2 {pivot_x} {pivot_y}; 1.8 {pivot_x} {pivot_y}; 0 {pivot_x} {pivot_y}"
      keyTimes="0; 0.42; 0.58; 0.72; 1"
      dur="5.6s" begin="0s" fill="freeze"/>
  </g>

  <g>
    <animateTransform xlink:href="#{uid}-badge" attributeName="transform" type="rotate"
      values="-1.7 560 112; 1.7 560 112; -1.7 560 112"
      keyTimes="0; 0.5; 1" dur="4.8s" begin="5.6s" repeatCount="indefinite"
      additive="sum"/>
  </g>
</svg>
"""


if __name__ == "__main__":
    from pathlib import Path

    out = Path(__file__).resolve().parents[1] / "assets" / "id-dashboard.svg"
    out.write_text(build(), encoding="utf-8")
    print("wrote", out, out.stat().st_size)
