"""Build all profile README assets, README.md, preview.html, and ZIP."""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_about
import build_connect
import build_hero
import build_id_dashboard
import build_stack
from svg_common import PROFILE


def write_readme() -> None:
    p = PROFILE
    projects_rows = "\n".join(
        f"| **{proj['name']}** | {proj['focus']} | {proj['blurb']} |"
        for proj in p["projects"]
    )
    social_links = " · ".join(f"[{s['label']}]({s['url']})" for s in p["socials"])

    md = f"""# {p['name']}

<p align="center">
  <img src="assets/hero.svg?v=2" alt="Hi, I'm {p['name']} — {p['role']} at {p['company']}" width="100%"/>
</p>

<p align="center">
  <img src="assets/about-life.svg?v=3" alt="Capabilities and interests" width="100%"/>
</p>

<p align="center">
  <img src="assets/stack.svg?v=2" alt="Technology stack" width="100%"/>
</p>

<p align="center">
  <img src="assets/id-dashboard.svg?v=2" alt="ID dashboard with verified GitHub metrics" width="100%"/>
</p>

<p align="center">
  <img src="assets/connect.svg?v=2" alt="Connect socially" width="100%"/>
</p>

### Connect

{social_links}

### Featured work

| Project | Focus | Notes |
| --- | --- | --- |
{projects_rows}

### Snapshot

- **Role:** {p['role']} @ {p['company']}
- **Location:** {p['location']}
- **GitHub:** [{p['github']}](https://github.com/{p['github']})
- **Public repos:** {p['metrics']['repos']} · **Followers:** {p['metrics']['followers']} · **Joined:** {p['metrics']['joined']}
"""
    (ROOT / "README.md").write_text(md, encoding="utf-8")


def write_preview() -> None:
    svgs = [
        "hero.svg",
        "about-life.svg",
        "stack.svg",
        "id-dashboard.svg",
        "connect.svg",
    ]
    blocks = []
    for name in svgs:
        blocks.append(
            f"""
<section>
  <h2>{name}</h2>
  <div class="row">
    <figure><figcaption>as &lt;img&gt;</figcaption><img src="assets/{name}?v=1" alt="{name}"/></figure>
    <figure><figcaption>inline object</figcaption><object data="assets/{name}?v=1" type="image/svg+xml"></object></figure>
  </div>
</section>"""
        )
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Profile README Preview — {PROFILE['name']}</title>
  <style>
    :root {{ color-scheme: dark; }}
    body {{ margin: 0; font-family: ui-sans-serif, system-ui, sans-serif; background: #05070f; color: #eef2ff; }}
    header {{ padding: 28px 20px 8px; max-width: 1100px; margin: 0 auto; }}
    h1 {{ font-size: 1.4rem; margin: 0 0 8px; }}
    p {{ color: #9aa6c3; }}
    section {{ max-width: 1100px; margin: 0 auto 36px; padding: 0 16px; }}
    h2 {{ font-size: 0.95rem; letter-spacing: 0.04em; color: #247bff; }}
    .row {{ display: grid; gap: 16px; }}
    figure {{ margin: 0; background: #0a1020; border: 1px solid #1c2740; border-radius: 16px; padding: 12px; }}
    figcaption {{ font-size: 12px; color: #9aa6c3; margin-bottom: 8px; }}
    img, object {{ width: 100%; height: auto; display: block; background: transparent; }}
    .links a {{ color: #247bff; margin-right: 12px; }}
    @media (min-width: 960px) {{ .row {{ grid-template-columns: 1fr 1fr; }} }}
  </style>
</head>
<body>
  <header>
    <h1>{PROFILE['name']} — animated README preview</h1>
    <p>Open this file locally to verify SVG animation, transparency, and layout at README width.</p>
    <p class="links">{" ".join(f'<a href="{s["url"]}">{s["label"]}</a>' for s in PROFILE["socials"])}</p>
  </header>
  {''.join(blocks)}
</body>
</html>
"""
    (ROOT / "preview.html").write_text(html, encoding="utf-8")


def write_icon_sources() -> None:
    text = """# Icon sources

Most brand marks use [Simple Icons](https://simpleicons.org/) (CC0).

These marks were removed from current Simple Icons releases for trademark policy reasons,
so the build embeds paths from Simple Icons **9.19.0** (still CC0) via jsDelivr:

- LinkedIn — `assets/icons/linkedin.svg`
- Amazon AWS — `assets/icons/amazonaws-si.svg`
- Microsoft Azure — `assets/icons/microsoftazure-si.svg`

Java uses the Simple Icons **OpenJDK** glyph (CC0), labeled as Java in the UI,
because an Oracle Java mark is not available in current Simple Icons.

Wikimedia SVG wordmarks for AWS/Azure/Java were also downloaded for reference under
`assets/icons/*.svg` but the orbit UI uses the Simple Icons-compatible 24×24 paths.
"""
    (ROOT / "licenses" / "ICON-SOURCES.md").write_text(text, encoding="utf-8")


def write_zip() -> None:
    zip_path = ROOT / "github-profile-readme.zip"
    include = [
        "README.md",
        "preview.html",
        "LICENSE",
        "assets/hero.svg",
        "assets/about-life.svg",
        "assets/stack.svg",
        "assets/id-dashboard.svg",
        "assets/connect.svg",
        "assets/id.png",
        "assets/right_pointing.png",
        "licenses/Syne-OFL.txt",
        "licenses/JetBrainsMono-OFL.txt",
        "licenses/FONTS.md",
        "licenses/ICON-SOURCES.md",
    ]
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for rel in include:
            path = ROOT / rel
            if path.exists():
                zf.write(path, rel)
    print("zip", zip_path, zip_path.stat().st_size)


def main() -> None:
    assets = ROOT / "assets"
    (assets / "hero.svg").write_text(build_hero.build(), encoding="utf-8")
    (assets / "about-life.svg").write_text(build_about.build(), encoding="utf-8")
    (assets / "stack.svg").write_text(build_stack.build(), encoding="utf-8")
    (assets / "id-dashboard.svg").write_text(build_id_dashboard.build(), encoding="utf-8")
    (assets / "connect.svg").write_text(build_connect.build(), encoding="utf-8")
    write_readme()
    write_preview()
    write_icon_sources()
    write_zip()
    for name in [
        "hero.svg",
        "about-life.svg",
        "stack.svg",
        "id-dashboard.svg",
        "connect.svg",
    ]:
        p = assets / name
        print(f"{name:20s} {p.stat().st_size:9d} bytes")


if __name__ == "__main__":
    main()
