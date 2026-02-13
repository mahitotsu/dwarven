"""Report generation using Jinja2 templates."""
from __future__ import annotations

from typing import Dict, Any
import importlib.resources
from jinja2 import Environment, FileSystemLoader, select_autoescape


def render_report(context: Dict[str, Any]) -> str:
    """Render HTML report from context dict.

    Expects templates/report.html.j2 inside the analyzer package.
    """
    # Locate templates directory inside the package
    try:
        templates_dir = importlib.resources.files("analyzer").joinpath("templates")
        loader = FileSystemLoader(str(templates_dir))
    except Exception:
        # Fallback: use current working dir './src/analyzer/templates'
        loader = FileSystemLoader("./src/analyzer/templates")

    env = Environment(loader=loader, autoescape=select_autoescape(["html", "xml"]))
    template = env.get_template("report.html.j2")
    return template.render(**context)
