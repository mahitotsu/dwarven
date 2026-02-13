# Data Analyzer

A CLI tool to analyze CSV data and generate HTML reports.

## Installation

```bash
uv pip install -e .
```

## Usage

```bash
python -m data_analyzer.main sample_data.csv
```

## Development

### Running Tests

```bash
pytest
```

### Type Checking

```bash
mypy src/
```

### Formatting

```bash
black src/ tests/
```
