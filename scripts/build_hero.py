"""Generate assets/hero.svg"""
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


def build() -> str:
    p = PROFILE
    uid = "hero"
    roles = p["roles"]
    role_frames = []
    # 4 roles × 3s = 12s cycle
    for i, role in enumerate(roles):
        role_frames.append(
            f"""
  <text class="{uid}-role {uid}-role-{i}" x="48" y="268" fill="{OFFWHITE}"
        font-family="SyneEmbed, sans-serif" font-weight="600" font-size="26">{xml_esc(role)}</text>
"""
        )

    pitch_lines = _wrap(p["pitch"], 62)
    pitch_tspans = "\n".join(
        f'<tspan x="48" dy="{0 if i == 0 else 20}">{xml_esc(line)}</tspan>'
        for i, line in enumerate(pitch_lines)
    )

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="1100" height="420" viewBox="0 0 1100 420" role="img"
     aria-label="Hi, I'm {xml_esc(p['name'])} — {xml_esc(p['role'])} at {xml_esc(p['company'])}">
  <title>{xml_esc(p['name'])} — GitHub Profile Hero</title>
  <desc>{xml_esc(p['pitch'])}</desc>
  {dot_pattern(uid)}
  <style><![CDATA[
{font_face_css(include_semi=True, include_mono_med=True)}
.{uid}-root {{ font-family: SyneEmbed, sans-serif; }}
.{uid}-fade {{ opacity: 0; animation: {uid}-in 0.9s ease both; }}
.{uid}-greet {{ opacity: 0; animation: {uid}-in 0.6s ease 0.15s both; }}
.{uid}-name-mask {{ animation: {uid}-rise 1.1s cubic-bezier(.2,.8,.2,1) 0.55s both; }}
.{uid}-pitch {{ opacity: 0; animation: {uid}-in 0.8s ease 1.2s both; }}
.{uid}-meta {{ opacity: 0; animation: {uid}-in 0.8s ease 1.45s both; }}
.{uid}-portrait {{ opacity: 0; transform: translateY(18px); animation: {uid}-portrait 1s cubic-bezier(.2,.8,.2,1) 0.7s both; }}
.{uid}-role {{ opacity: 0; animation: {uid}-rolecycle 12s linear infinite; }}
.{uid}-role-0 {{ animation-delay: 0s; }}
.{uid}-role-1 {{ animation-delay: -3s; }}
.{uid}-role-2 {{ animation-delay: -6s; }}
.{uid}-role-3 {{ animation-delay: -9s; }}
@keyframes {uid}-in {{
  from {{ opacity: 0; transform: translateY(10px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes {uid}-rise {{
  from {{ transform: translateY(110%); }}
  to {{ transform: translateY(0); }}
}}
@keyframes {uid}-portrait {{
  from {{ opacity: 0; transform: translateY(18px) scale(0.96); }}
  to {{ opacity: 1; transform: translateY(0) scale(1); }}
}}
@keyframes {uid}-rolecycle {{
  0%, 3% {{ opacity: 0; transform: translateY(12px); }}
  8%, 22% {{ opacity: 1; transform: translateY(0); }}
  28%, 100% {{ opacity: 0; transform: translateY(-10px); }}
}}
{reduced_motion_css(f'.{uid}-fade, .{uid}-greet, .{uid}-name-mask, .{uid}-pitch, .{uid}-meta, .{uid}-portrait, .{uid}-role')}
@media (prefers-reduced-motion: reduce) {{
  .{uid}-role-0 {{ opacity: 1 !important; }}
  .{uid}-greet, .{uid}-name-mask, .{uid}-pitch, .{uid}-meta, .{uid}-portrait {{ opacity: 1 !important; transform: none !important; }}
}}
  ]]></style>

  <!-- Final readable base (no animation / reduced motion fallbacks via CSS) -->
  <rect width="1100" height="420" rx="28" fill="{NAVY}"/>
  <rect width="1100" height="420" rx="28" fill="url(#{uid}-dots)" opacity="0.55"/>
  <rect x="1.5" y="1.5" width="1097" height="417" rx="26.5" fill="none" stroke="url(#{uid}-hair)" stroke-width="1.5"/>

  <g class="{uid}-root">
    <!-- Left copy -->
    <g>
      <clipPath id="{uid}-greet-clip">
        <!-- Base width is final/readable if SMIL unsupported -->
        <rect id="{uid}-greet-rect" x="48" y="48" width="120" height="36">
          <animate attributeName="width" values="0;0;120" keyTimes="0;0.08;1" dur="1.1s" begin="0s" fill="freeze"/>
        </rect>
      </clipPath>
      <g clip-path="url(#{uid}-greet-clip)">
        <text class="{uid}-greet" x="48" y="74" fill="{BLUE}" font-family="JBMonoEmbed, monospace" font-size="18" font-weight="500">Hi, I'm</text>
      </g>

      <clipPath id="{uid}-name-clip">
        <rect x="40" y="78" width="720" height="140"/>
      </clipPath>
      <g clip-path="url(#{uid}-name-clip)">
        <g class="{uid}-name-mask">
          <text x="48" y="136" fill="{OFFWHITE}" font-family="SyneEmbed, sans-serif" font-weight="700" font-size="50">
            <tspan x="48" dy="0">{xml_esc(p['name'].split()[0])}</tspan>
            <tspan x="48" dy="56">{xml_esc(p['name'].split()[1])}</tspan>
          </text>
        </g>
      </g>

      <!-- Static base role (visible if CSS animations unsupported) -->
      <text x="48" y="268" fill="{OFFWHITE}" font-family="SyneEmbed, sans-serif" font-weight="600" font-size="26" opacity="0.22">{xml_esc(roles[0])}</text>
      {''.join(role_frames)}

      <text class="{uid}-pitch" x="48" y="318" fill="{MUTED}" font-family="JBMonoEmbed, monospace" font-size="14">
        {pitch_tspans}
      </text>

      <g class="{uid}-meta">
        <circle cx="56" cy="372" r="4" fill="{CRIMSON}"/>
        <text x="72" y="377" fill="{OFFWHITE}" font-family="JBMonoEmbed, monospace" font-size="14">{xml_esc(p['location'])}  ·  {xml_esc(p['role'])} @ {xml_esc(p['company'])}</text>
      </g>
    </g>

    <!-- Portrait card -->
    <g class="{uid}-portrait">
      <rect x="760" y="48" width="292" height="324" rx="24" fill="url(#{uid}-card)" stroke="url(#{uid}-hair)" stroke-width="1.4"/>
      <clipPath id="{uid}-photo-clip">
        <rect x="780" y="68" width="252" height="252" rx="18"/>
      </clipPath>
      <image x="780" y="68" width="252" height="252" clip-path="url(#{uid}-photo-clip)"
             href="data:image/png;base64,{ID_PNG}" xlink:href="data:image/png;base64,{ID_PNG}" preserveAspectRatio="xMidYMid slice"/>
      <text x="906" y="348" text-anchor="middle" fill="{MUTED}" font-family="JBMonoEmbed, monospace" font-size="12">@{p['github']}</text>
    </g>
  </g>

  <!-- SMIL: soft blue glow pulse from 0s (decorative; CSS handles main entrances) -->
  <circle cx="980" cy="90" r="48" fill="{BLUE}" opacity="0.12">
    <animate attributeName="opacity" values="0.08;0.16;0.08" keyTimes="0;0.5;1" dur="6s" begin="0s" repeatCount="indefinite"/>
  </circle>
  <circle cx="120" cy="360" r="36" fill="{CRIMSON}" opacity="0.08">
    <animate attributeName="opacity" values="0.05;0.12;0.05" keyTimes="0;0.5;1" dur="7s" begin="0s" repeatCount="indefinite"/>
  </circle>
</svg>
"""


def _wrap(text: str, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if len(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [""]


if __name__ == "__main__":
    from pathlib import Path

    out = Path(__file__).resolve().parents[1] / "assets" / "hero.svg"
    out.write_text(build(), encoding="utf-8")
    print("wrote", out, out.stat().st_size)
