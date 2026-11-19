"""Shared helpers for self-contained GitHub README SVGs."""
from __future__ import annotations

import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ICONS = json.loads((ASSETS / "icons" / "icons.json").read_text(encoding="utf-8"))

NAVY = "#070b16"
BLUE = "#247bff"
CRIMSON = "#ff354f"
OFFWHITE = "#eef2ff"
MUTED = "#9aa6c3"


def xml_esc(text: str) -> str:
    """Escape text for SVG/XML content and attributes."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


FONT_SYNE = b64(ASSETS / "fonts" / "Syne-Bold.woff2")
FONT_SYNE_SEMI = b64(ASSETS / "fonts" / "Syne-SemiBold.woff2")
FONT_MONO = b64(ASSETS / "fonts" / "JetBrainsMono-Regular.woff2")
FONT_MONO_MED = b64(ASSETS / "fonts" / "JetBrainsMono-Medium.woff2")
ID_PNG = b64(ASSETS / "id.png")
POINT_PNG = b64(ASSETS / "right_pointing.png")


def font_face_css(include_semi: bool = False, include_mono_med: bool = False) -> str:
    """Embed Syne + JetBrains Mono as base64 WOFF2 (minimal set per SVG)."""
    parts = [
        f"""@font-face {{
  font-family: 'SyneEmbed';
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url('data:font/woff2;base64,{FONT_SYNE}') format('woff2');
}}""",
        f"""@font-face {{
  font-family: 'JBMonoEmbed';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url('data:font/woff2;base64,{FONT_MONO}') format('woff2');
}}""",
    ]
    if include_semi:
        parts.insert(
            1,
            f"""@font-face {{
  font-family: 'SyneEmbed';
  font-style: normal;
  font-weight: 600;
  font-display: swap;
  src: url('data:font/woff2;base64,{FONT_SYNE_SEMI}') format('woff2');
}}""",
        )
    if include_mono_med:
        parts.append(
            f"""@font-face {{
  font-family: 'JBMonoEmbed';
  font-style: normal;
  font-weight: 500;
  font-display: swap;
  src: url('data:font/woff2;base64,{FONT_MONO_MED}') format('woff2');
}}"""
        )
    return "\n".join(parts)


def reduced_motion_css(selectors: str) -> str:
    return f"""
@media (prefers-reduced-motion: reduce) {{
  {selectors} {{
    animation: none !important;
    transition: none !important;
  }}
}}
""".strip()


def dot_pattern(uid: str, opacity: float = 0.18) -> str:
    return f"""
<defs>
  <pattern id="{uid}-dots" width="18" height="18" patternUnits="userSpaceOnUse">
    <circle cx="1.5" cy="1.5" r="1.1" fill="{OFFWHITE}" opacity="{opacity}"/>
  </pattern>
  <linearGradient id="{uid}-hair" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="{BLUE}" stop-opacity="0.85"/>
    <stop offset="50%" stop-color="{OFFWHITE}" stop-opacity="0.25"/>
    <stop offset="100%" stop-color="{CRIMSON}" stop-opacity="0.85"/>
  </linearGradient>
  <linearGradient id="{uid}-card" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#0c1428"/>
    <stop offset="100%" stop-color="#0a101f"/>
  </linearGradient>
</defs>
""".strip()


def icon_badge(slug: str, cx: float, cy: float, size: float = 36, uid: str = "") -> str:
    ic = ICONS[slug]
    scale = (size * 0.48) / 24
    x = cx - size / 2
    y = cy - size / 2
    fill = f"#{ic['hex']}"
    # Dark logos get a light fill for contrast on navy
    if ic["hex"].lower() in {"000000", "0f0f11", "181717"}:
        fill = OFFWHITE
    return f"""
<g id="{uid}-{slug}" transform="translate({x:.2f},{y:.2f})">
  <rect width="{size}" height="{size}" rx="{size*0.28:.2f}" fill="#0e162b" stroke="url(#{uid}-hair)" stroke-width="1.2"/>
  <g transform="translate({size*0.26:.2f},{size*0.26:.2f}) scale({scale:.4f})">
    <path d="{ic['path']}" fill="{fill}"/>
  </g>
</g>
""".strip()


def chip(label: str, x: float, y: float, w: float, uid: str, delay: float = 0) -> str:
    return f"""
<g class="{uid}-chip" style="animation-delay:{delay:.2f}s">
  <rect x="{x}" y="{y}" width="{w}" height="30" rx="15" fill="#101a31" stroke="url(#{uid}-hair)" stroke-width="1"/>
  <text x="{x + w/2:.1f}" y="{y + 19.5:.1f}" text-anchor="middle" fill="{OFFWHITE}" font-family="JBMonoEmbed, monospace" font-size="12">{label}</text>
</g>
""".strip()


PROFILE = {
    "name": "Chander Parkash",
    "github": "chanderparkash179",
    "role": "Senior Software Engineer",
    "company": "Systems Ltd.",
    "location": "Karachi",
    "pitch": "Engineering resilient banking & enterprise platforms — payments, teller systems, and MDM at global scale.",
    "roles": [
        "Senior Software Engineer",
        "Java & Spring Boot Specialist",
        "NestJS · Angular Builder",
        "Cloud & Containers Engineer",
    ],
    "capabilities": [
        "Enterprise banking & payments",
        "Spring Boot microservices",
        "NestJS & Angular apps",
        "Docker · Kubernetes delivery",
        "AWS & Azure cloud platforms",
        "Secure, scalable API design",
    ],
    # Note: builders must run xml_esc() on these strings when writing SVG text.
    "interests": [
        {
            "title": "Cricket",
            "lines": [
                "Fast bowling, weekend matches,",
                "and team energy.",
            ],
        },
        {
            "title": "Badminton",
            "lines": [
                "Sharp rallies, footwork,",
                "and competitive focus.",
            ],
        },
        {
            "title": "Coding",
            "lines": [
                "Side builds, clean architecture,",
                "continuous learning.",
            ],
        },
    ],
    "stack_orbit": [
        "java",
        "springboot",
        "nestjs",
        "angular",
        "docker",
        "kubernetes",
        "amazonaws",
        "microsoftazure",
    ],
    "stack_groups": {
        "Languages": ["Java", "JavaScript", "TypeScript", "Go"],
        "Backend": ["Spring Boot", "NestJS", "NodeJS"],
        "Frontend": ["Angular", "HTML5", "CSS3"],
        "Data": ["PostgreSQL", "MySQL", "IBM DB2", "Oracle DB", "MSSQL"],
        "Cloud": ["AWS", "Azure", "Docker", "Kubernetes"],
    },
    "stack_chip_slugs": {
        "Java": "java",
        "JavaScript": "javascript",
        "TypeScript": "typescript",
        "Go": "go",
        "Spring Boot": "springboot",
        "NestJS": "nestjs",
        "NodeJS": "nodejs",
        "Angular": "angular",
        "HTML5": "html5",
        "CSS3": "css3",
        "PostgreSQL": "postgresql",
        "MySQL": "mysql",
        "IBM DB2": "ibm",
        "Oracle DB": "oracle",
        "MSSQL": "mssql",
        "AWS": "amazonaws",
        "Azure": "microsoftazure",
        "Docker": "docker",
        "Kubernetes": "kubernetes",
    },
    "metrics": {
        "repos": 22,
        "followers": 7,
        "joined": "Nov 2019",
        "as_of": "Nov 2026",
    },
    "projects": [
        {
            "name": "Mashreq Bank",
            "focus": "Bill Payments",
            "blurb": "High-volume bill payment flows for retail banking.",
        },
        {
            "name": "Bank Al Habib",
            "focus": "Teller",
            "blurb": "Teller platform capabilities for branch operations.",
        },
        {
            "name": "Panasonic Europe",
            "focus": "MDM · Profile Center 2.0",
            "blurb": "Master data & profile center upgrades across Europe.",
        },
    ],
    "socials": [
        {
            "key": "portfolio",
            "label": "Portfolio",
            "handle": "ichanderparkash.web.app",
            "url": "https://ichanderparkash.web.app",
        },
        {
            "key": "linkedin",
            "label": "LinkedIn",
            "handle": "chanderparkash179",
            "url": "https://linkedin.com/in/chanderparkash179",
        },
        {
            "key": "stackoverflow",
            "label": "Stack Overflow",
            "handle": "chander-parkash",
            "url": "https://stackoverflow.com/users/22019464/chander-parkash",
        },
        {
            "key": "github",
            "label": "GitHub",
            "handle": "chanderparkash179",
            "url": "https://github.com/chanderparkash179",
        },
        {
            "key": "instagram",
            "label": "Instagram",
            "handle": "@chanderraaj179",
            "url": "https://www.instagram.com/chanderraaj179",
        },
        {
            "key": "facebook",
            "label": "Facebook",
            "handle": "chanderparkash179",
            "url": "https://facebook.com/chanderparkash179",
        },
        {
            "key": "gmail",
            "label": "Email",
            "handle": "chanderparkash179@",
            "url": "mailto:chanderparkash179@gmail.com",
        },
    ],
}
