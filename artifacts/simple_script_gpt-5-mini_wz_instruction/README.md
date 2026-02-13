# Analyzer

Simple CSV analysis tool that produces an HTML report.

Usage:

python -m analyze <input.csv> -o report.html

Development:

Install dev dependencies with uv (see project pyproject.toml) or use requirements.txt for a fallback.

Setup (venv + pip)

1. Create virtualenv:

```bash
python3 -m venv .venv
```

2. Activate and install dependencies:

```bash
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt pytest pytest-cov black mypy pandas-stubs
```

Run the tool:

```bash
.venv/bin/python -m analyze sample_data.csv -o report.html
```

Run tests and quality checks:

```bash
.venv/bin/python -m pytest --cov=src --cov-report=term-missing
.venv/bin/python -m black . --check
.venv/bin/python -m mypy .
```
