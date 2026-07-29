"""
build_site.py
--------------
Converts Plotly figures into finished HTML pages using a shared Jinja2
template (templates/base.html) + shared stylesheet (assets/style.css).

Usage pattern:
    1. Build your Plotly figures as usual (fig = go.Figure(...))
    2. Wrap each figure in a `ContentBlock`
    3. Call `render_page(...)` to write a finished HTML file

Output goes into ../docs/ which is the folder GitHub Pages will serve.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Literal

import plotly.graph_objects as go
from jinja2 import Environment, FileSystemLoader

# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------
SITE_DIR = Path(__file__).parent
TEMPLATE_DIR = SITE_DIR / "templates"
ASSETS_DIR = SITE_DIR / "assets"
OUTPUT_DIR = SITE_DIR.parent / "docs"          # <- GitHub Pages source

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


# ---------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------
@dataclass
class ContentBlock:
    """
    One chart card on the page. Provide EXACTLY ONE of:
      - fig       : a live plotly.graph_objects.Figure (normal case)
      - raw_html  : a pre-made HTML fragment string (e.g. extracted from an
                    already-exported file, or a placeholder message)
    """
    fig: go.Figure | None = None
    raw_html: str | None = None
    card_title: str | None = None
    size: Literal["full", "half", "third"] = "full"

    def to_html_fragment(self) -> str:
        if self.raw_html is not None:
            return self.raw_html
        # full_html=False -> just a <div> + <script>, not a whole page
        # include_plotlyjs=False -> Plotly.js is already loaded once in base.html
        return self.fig.to_html(
            full_html=False,
            include_plotlyjs=False,
            config={"responsive": True, "displaylogo": False},
        )


# ---------------------------------------------------------------------
# Helper 1: reuse a chart you already exported with fig.write_html()
# ---------------------------------------------------------------------
def load_exported_fragment(html_path: str | Path) -> str:
    """
    Takes a FULL standalone HTML file produced by fig.write_html() (default
    settings: full_html=True, include_plotlyjs='cdn') and extracts just the
    reusable <div>+<script> fragment, stripping:
      - <html>/<head>/<body> wrapper tags
      - the duplicate Plotly.js <script src="cdn.plot.ly/..."> tag
        (base.html already loads Plotly.js once, so a second copy would
        just waste bandwidth, not break anything -- but better to remove it)

    Use this so you don't have to re-run the original Python analysis just
    to bring an already-made chart into the site.
    """
    import re

    html = Path(html_path).read_text(encoding="utf-8")

    # keep only what's inside <body>...</body>
    body_match = re.search(r"<body>(.*)</body>", html, re.DOTALL)
    fragment = body_match.group(1) if body_match else html

    # drop the CDN <script src="...plot.ly...">...</script> tag (already loaded once in base.html)
    fragment = re.sub(
        r'<script[^>]*src="[^"]*cdn\.plot\.ly[^"]*"[^>]*></script>',
        "",
        fragment,
    )
    return fragment.strip()


# ---------------------------------------------------------------------
# Helper 2: a labeled "empty slot" for data/pages not ready yet
# ---------------------------------------------------------------------
def placeholder_block(
    card_title: str,
    note: str = "Modul ini sedang dalam pengembangan. Data akan tersedia segera.",
    size: Literal["full", "half", "third"] = "full",
) -> ContentBlock:
    """
    Renders a clearly-labeled empty state instead of a chart. The page and
    its URL exist NOW; later you just swap this call for a real
    ContentBlock(fig=...) -- nothing else about the site changes.
    """
    fragment = f"""
    <div class="placeholder-block">
      <div class="placeholder-badge">Dalam Pengembangan</div>
      <p>{note}</p>
    </div>
    """
    return ContentBlock(raw_html=fragment, card_title=card_title, size=size)


# ---------------------------------------------------------------------
# Core render function
# ---------------------------------------------------------------------
def render_page(
    output_path: str,
    title: str,
    blocks: list[ContentBlock],
    subtitle: str | None = None,
    section: str | None = None,
) -> None:
    """
    output_path : relative path under docs/, e.g. "rainfall/daily.html"
    title       : page <h1> and <title>
    blocks      : list of ContentBlock (one per chart/card)
    section     : "rainfall" | "fews" | "streamflow" -> highlights nav item
    """
    out_file = OUTPUT_DIR / output_path
    out_file.parent.mkdir(parents=True, exist_ok=True)

    # depth of this page relative to docs/ root, to build correct relative links
    depth = len(out_file.relative_to(OUTPUT_DIR).parts) - 1
    root_prefix = "../" * depth
    asset_prefix = root_prefix

    template = env.get_template("base.html")
    html = template.render(
        title=title,
        subtitle=subtitle,
        section=section,
        content_blocks=[
            {"html": b.to_html_fragment(), "card_title": b.card_title, "size": b.size}
            for b in blocks
        ],
        last_updated=datetime.now().strftime("%Y-%m-%d %H:%M WIB"),
        root_prefix=root_prefix,
        asset_prefix=asset_prefix,
    )

    out_file.write_text(html, encoding="utf-8")
    print(f"Built: {out_file}")


def copy_assets() -> None:
    import shutil
    dest = OUTPUT_DIR / "assets"
    dest.mkdir(parents=True, exist_ok=True)
    for f in ASSETS_DIR.glob("*"):
        shutil.copy(f, dest / f.name)


# =======================================================================
# SITEMAP -- every planned page lives here as ONE ENTRY.
#
# This is the "slot" system: every page in the whole future portal is
# declared once below, each with a `blocks` function. Today, most of those
# functions just return placeholder_block(...). Later, updating a page
# means editing ONLY that one function -- the sitemap, nav, URLs, and every
# other page stay untouched.
# =======================================================================

def blocks_homepage() -> list[ContentBlock]:
    return [
        placeholder_block(
            "Today's Hydrological Briefing",
            "Ringkasan otomatis (kondisi hujan nasional, wilayah terbasah/"
            "terkering, jumlah DAS Waspada/Siaga/Awas) akan tampil di sini "
            "setelah pipeline data harian aktif.",
        ),
    ]


def blocks_rainfall_daily() -> list[ContentBlock]:
    return [placeholder_block("Curah Hujan Harian — Peta Nasional")]

def blocks_rainfall_weekly() -> list[ContentBlock]:
    return [placeholder_block("Curah Hujan Mingguan")]

def blocks_rainfall_monthly() -> list[ContentBlock]:
    return [placeholder_block("Curah Hujan Bulanan")]

def blocks_rainfall_annual() -> list[ContentBlock]:
    return [placeholder_block("Curah Hujan Tahunan")]

def blocks_rainfall_spi() -> list[ContentBlock]:
    return [placeholder_block("Standardized Precipitation Index (SPI)")]

def blocks_rainfall_anomaly() -> list[ContentBlock]:
    return [placeholder_block("Anomali Curah Hujan")]

def blocks_rainfall_ranking() -> list[ContentBlock]:
    return [
        placeholder_block("Ranking Wilayah Terbasah", size="half"),
        placeholder_block("Ranking Wilayah Terkering", size="half"),
    ]


def make_fews_region_blocks(region_name: str):
    """One placeholder generator reused for all 10 FEWS regions."""
    def _blocks() -> list[ContentBlock]:
        return [
            placeholder_block(f"Status Kondisi — {region_name}", size="half"),
            placeholder_block(f"Status Sungai & Peringatan — {region_name}", size="half"),
        ]
    return _blocks


def blocks_streamflow_example() -> list[ContentBlock]:
    # REAL chart, reused from a file you already exported with fig.write_html()
    fragment = load_exported_fragment(
        SITE_DIR / "imports" / "FEWS_Forecast_Hydrograph_Dashboard.html"
    )
    return [ContentBlock(raw_html=fragment, card_title="Forecast Hydrograph")]

def blocks_streamflow_index() -> list[ContentBlock]:
    return [
        placeholder_block(
            "Daftar DAS",
            "Pilih DAS untuk melihat forecast hydrograph 1/3/6 bulan. "
            "Contoh hasil forecast yang sudah tersedia: lihat halaman "
            '"Contoh: Forecast Hydrograph" pada menu di atas.',
        )
    ]


# Sitemap: (output_path, title, section, subtitle, blocks_function)
PAGES = [
    ("index.html", "HESLab Portal", None,
     "Hydrological Monitoring, Forecasting and Early Warning Platform for Indonesia",
     blocks_homepage),

    ("rainfall/index.html", "Rainfall Monitoring Indonesia", "rainfall", None, blocks_rainfall_daily),
    ("rainfall/daily.html", "Rainfall Monitoring — Harian", "rainfall", None, blocks_rainfall_daily),
    ("rainfall/weekly.html", "Rainfall Monitoring — Mingguan", "rainfall", None, blocks_rainfall_weekly),
    ("rainfall/monthly.html", "Rainfall Monitoring — Bulanan", "rainfall", None, blocks_rainfall_monthly),
    ("rainfall/annual.html", "Rainfall Monitoring — Tahunan", "rainfall", None, blocks_rainfall_annual),
    ("rainfall/spi.html", "Rainfall Monitoring — SPI", "rainfall", None, blocks_rainfall_spi),
    ("rainfall/anomaly.html", "Rainfall Monitoring — Anomali", "rainfall", None, blocks_rainfall_anomaly),
    ("rainfall/ranking.html", "Rainfall Monitoring — Ranking Wilayah", "rainfall", None, blocks_rainfall_ranking),

    ("fews/index.html", "FEWS Indonesia", "fews", None, make_fews_region_blocks("Jawa I")),
    ("fews/jawa-1.html", "FEWS Indonesia — Jawa I", "fews", None, make_fews_region_blocks("Jawa I")),
    ("fews/jawa-2.html", "FEWS Indonesia — Jawa II", "fews", None, make_fews_region_blocks("Jawa II")),
    ("fews/jawa-3.html", "FEWS Indonesia — Jawa III", "fews", None, make_fews_region_blocks("Jawa III")),
    ("fews/sumatera-1.html", "FEWS Indonesia — Sumatera I", "fews", None, make_fews_region_blocks("Sumatera I")),
    ("fews/sumatera-2.html", "FEWS Indonesia — Sumatera II", "fews", None, make_fews_region_blocks("Sumatera II")),
    ("fews/sumatera-3.html", "FEWS Indonesia — Sumatera III", "fews", None, make_fews_region_blocks("Sumatera III")),
    ("fews/kalimantan.html", "FEWS Indonesia — Kalimantan", "fews", None, make_fews_region_blocks("Kalimantan")),
    ("fews/sulawesi.html", "FEWS Indonesia — Sulawesi", "fews", None, make_fews_region_blocks("Sulawesi")),
    ("fews/papua.html", "FEWS Indonesia — Papua", "fews", None, make_fews_region_blocks("Papua")),
    ("fews/bali-nusra.html", "FEWS Indonesia — Bali Nusa Tenggara", "fews", None, make_fews_region_blocks("Bali Nusa Tenggara")),

    ("streamflow/index.html", "Streamflow Forecast Indonesia", "streamflow", None, blocks_streamflow_index),
    ("streamflow/contoh-forecast.html", "Contoh: Forecast Hydrograph", "streamflow", None, blocks_streamflow_example),
]


if __name__ == "__main__":
    copy_assets()
    for output_path, title, section, subtitle, blocks_fn in PAGES:
        render_page(
            output_path=output_path,
            title=title,
            subtitle=subtitle,
            section=section,
            blocks=blocks_fn(),
        )
    print(f"\nSelesai: {len(PAGES)} halaman dibangun ke {OUTPUT_DIR}/")
