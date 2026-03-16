from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API_DIR = ROOT / "api"
sys.path.insert(0, str(API_DIR))

from github_stats import generate_custom_badge

SAMPLES = {
    "sample_build.svg": dict(label="build", value="passing", icon="check", theme="terminal", style="flat", size="md"),
    "sample_release.svg": dict(label="release", value="v2.1.0", icon="rocket", theme="sunset", style="for-the-badge", size="lg"),
    "sample_coverage.svg": dict(label="coverage", value="98%", icon="bolt", theme="dark", style="plastic", gradient=True, size="md"),
    "sample_docs.svg": dict(label="docs", value="stable", icon="docs", theme="light", style="outline", size="sm"),
    "sample_quality.svg": dict(label="quality", value="A+", icon="star", theme="neon", style="pill", size="xl", scale=1.1),
}


def main():
    output_dir = ROOT / "sample_svgs"
    output_dir.mkdir(exist_ok=True)
    for file_name, params in SAMPLES.items():
        svg = generate_custom_badge(**params)
        (output_dir / file_name).write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
