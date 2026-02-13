# CSV Report Tool

Setup:

1. Create virtualenv: python -m venv .venv
2. Activate: source .venv/bin/activate
3. Install deps: uv sync --extra dev   # or pip install -r requirements.txt

Usage:

Run with bundled sample data:

  python -m src.analyze sample_data/sample_data.csv

Or via CLI wrapper:

  python -m src.cli sample_data/sample_data.csv -o report.html

Testing:

Run tests with coverage:

  .venv/bin/python -m pytest --cov=src --cov-report=term-missing

Formatting and type checks:

  .venv/bin/python -m pip install .  # ensure package is installable
  black .
  mypy src
