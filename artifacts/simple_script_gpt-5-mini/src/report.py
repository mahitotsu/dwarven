from jinja2 import Template
from typing import Dict


TEMPLATE = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>{{ title }}</title>
    <style>
      body { font-family: Arial, sans-serif; margin: 2rem; }
      .stats { margin-bottom: 1rem; }
      .stats table { border-collapse: collapse; }
      .stats td, .stats th { border: 1px solid #ddd; padding: 8px; }
    </style>
  </head>
  <body>
    <h1>{{ title }}</h1>
    <div class="stats">
      <h2>Summary</h2>
      <table>
        <tr><th>metric</th><th>value</th></tr>
        <tr><td>count</td><td>{{ stats.count }}</td></tr>
        <tr><td>mean</td><td>{{ stats.mean }}</td></tr>
        <tr><td>median</td><td>{{ stats.median }}</td></tr>
        <tr><td>min</td><td>{{ stats.min }}</td></tr>
        <tr><td>max</td><td>{{ stats.max }}</td></tr>
      </table>
    </div>
    <div class="plot">
      <h2>Time Series</h2>
      <img src="data:image/png;base64,{{ plot_b64 }}" alt="time series" />
    </div>
  </body>
</html>
"""


def render_report(title: str, stats: Dict, plot_b64: str) -> str:
    tpl = Template(TEMPLATE)
    return tpl.render(title=title, stats=stats, plot_b64=plot_b64)
