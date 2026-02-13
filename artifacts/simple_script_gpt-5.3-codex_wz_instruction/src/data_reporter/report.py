from __future__ import annotations

from importlib import resources

from jinja2 import Environment

from .models import Report, SummaryStats


def render_report(stats: SummaryStats, plot_html: str, title: str) -> str:
    template_text = (
        resources.files("data_reporter")
        .joinpath("templates/report.html.j2")
        .read_text(encoding="utf-8")
    )
    env = Environment(autoescape=True)
    template = env.from_string(template_text)
    return template.render(report=Report(stats=stats, plot_html=plot_html, title=title))
