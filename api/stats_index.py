from __future__ import annotations

import json
import os
import sys

from flask import Flask, Response, request

sys.path.insert(0, os.path.dirname(__file__))

from data_fetchers import get_catalog, resolve_preset
from github_stats import generate_custom_badge

app = Flask(__name__)


def _param(name: str, default: str = "") -> str:
    if request.method == "POST":
        return (request.form.get(name) or request.args.get(name, default)).strip()
    return request.args.get(name, default).strip()


def _param_bool(name: str, default: bool = False) -> bool:
    if request.method == "POST":
        value = (request.form.get(name) or request.args.get(name, "")).strip().lower()
    else:
        value = request.args.get(name, "").strip().lower()
    if value in ("1", "true", "yes", "on"):
        return True
    if value in ("0", "false", "no", "off"):
        return False
    return default


def _param_int(name: str, default: int, lo: int, hi: int) -> int:
    try:
        raw = request.form.get(name, request.args.get(name, default)) if request.method == "POST" else request.args.get(name, default)
        return min(max(int(raw), lo), hi)
    except (TypeError, ValueError):
        return default


def _param_float(name: str, default: float, lo: float, hi: float) -> float:
    try:
        raw = request.form.get(name, request.args.get(name, default)) if request.method == "POST" else request.args.get(name, default)
        return min(max(float(raw), lo), hi)
    except (TypeError, ValueError):
        return default


def _svg_response(svg: str) -> Response:
    return Response(
        svg,
        mimetype="image/svg+xml",
        headers={
            "Cache-Control": "public, max-age=300, s-maxage=300",
            "Access-Control-Allow-Origin": "*",
        },
    )


@app.route("/")
def index():
    html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "stats_index.html"))
    with open(html_path, "r", encoding="utf-8") as file:
        return Response(file.read(), mimetype="text/html")


def _form_or_arg(name: str, default: str = "") -> str:
    """Read a parameter from POST form data first, then fall back to query string."""
    val = request.form.get(name, "").strip()
    if val:
        return val
    return request.args.get(name, default).strip()


def _form_or_arg_bool(name: str, default: bool = False) -> bool:
    value = _form_or_arg(name).lower()
    if value in ("1", "true", "yes", "on"):
        return True
    if value in ("0", "false", "no", "off"):
        return False
    return default


def _form_or_arg_int(name: str, default: int, lo: int, hi: int) -> int:
    try:
        return min(max(int(_form_or_arg(name, str(default))), lo), hi)
    except (TypeError, ValueError):
        return default


def _form_or_arg_float(name: str, default: float, lo: float, hi: float) -> float:
    try:
        return min(max(float(_form_or_arg(name, str(default))), lo), hi)
    except (TypeError, ValueError):
        return default


@app.route("/badge", methods=["GET", "POST"])
def badge():
    preset_name = _form_or_arg("preset")
    preset = resolve_preset(preset_name)

    icon_data = _param("icon_data") or None

    svg = generate_custom_badge(
        label=_form_or_arg("label", preset["label"]),
        value=_form_or_arg("value", preset["value"]),
        icon=_form_or_arg("icon", preset["icon"]),
        style=_form_or_arg("style", preset["style"]),
        theme=_form_or_arg("theme", preset["theme"]),
        label_bg=_form_or_arg("label_bg") or None,
        value_bg=_form_or_arg("value_bg") or None,
        label_color=_form_or_arg("label_color") or None,
        value_color=_form_or_arg("value_color") or None,
        border_color=_form_or_arg("border_color") or None,
        border_radius=_form_or_arg_int("border_radius", 4, 0, 999),
        gradient=_form_or_arg_bool("gradient", False),
        uppercase=_form_or_arg_bool("uppercase", False),
        compact=_form_or_arg_bool("compact", False),
        size=_form_or_arg("size", preset.get("size", "md")),
        scale=_form_or_arg_float("scale", 1.0, 0.7, 2.0),
        icon_data=_form_or_arg("icon_data") or None,
    )
    return _svg_response(svg)


@app.route("/catalog")
def catalog():
    return Response(json.dumps(get_catalog()), mimetype="application/json", headers={"Access-Control-Allow-Origin": "*"})


@app.route("/health")
def health():
    return Response(json.dumps({"ok": True, "service": "custom-badge-generator"}), mimetype="application/json")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
