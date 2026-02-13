from __future__ import annotations

from pathlib import Path

from .analysis import compute_summary_stats
from .errors import OutputError
from .io import read_and_validate_csv
from .report import render_report
from .viz import build_timeseries_plot_html


def run(input_csv: Path, output_html: Path, *, title: str | None = None) -> str:
    """Run the analysis pipeline and write the report to disk.

    Returns the rendered HTML (useful for tests).
    """
    return run_with_options(input_csv, output_html, title=title, print_summary=False)


def run_with_options(
    input_csv: Path,
    output_html: Path,
    *,
    title: str | None = None,
    print_summary: bool = False,
) -> str:
    """Run the analysis pipeline with optional console summary output."""
    df = read_and_validate_csv(input_csv)
    report_title = title or f"Report: {input_csv.name}"
    stats = compute_summary_stats(df)
    plot_html = build_timeseries_plot_html(df, report_title)
    html = render_report(stats=stats, plot_html=plot_html, title=report_title)

    try:
        output_html.write_text(html, encoding="utf-8")
    except OSError as exc:
        raise OutputError(f"Failed to write report: {output_html}") from exc

    if print_summary:
        print(
            "Summary:",
            f"count={stats.count}",
            f"mean={stats.mean:.6g}",
            f"median={stats.median:.6g}",
            f"min={stats.min:.6g}",
            f"max={stats.max:.6g}",
            sep="\n  ",
        )
    return html
