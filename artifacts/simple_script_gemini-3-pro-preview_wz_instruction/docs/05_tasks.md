# タスク分解 (Tasks)

## Phase 1: Project Setup
- [ ] Initialize project with `pyproject.toml` using `uv` (or manual creation).
- [ ] Configure `dependencies` (pandas, matplotlib) and `dev-dependencies` (pytest, ruff, mypy).
- [ ] Create directory structure (`src/`, `tests/`).
- [ ] Create `.gitignore`.

## Phase 2: Core Implementation
- [ ] **Data Loader**: Implement `loader.py` to read CSV and validate schema.
- [ ] **Analyzer**: Implement `analysis.py` to calculate stats.
- [ ] **Plotter**: Implement `plotting.py` to generate plots as base64 strings.
- [ ] **Report**: Implement `report.py` to generate HTML content.
- [ ] **CLI**: Implement `main.py` using `argparse` to wire everything together.

## Phase 3: Testing & Quality
- [ ] Create unit tests for `analysis.py` (verify stats calc).
- [ ] Create unit tests for `loader.py` (verify CSV parsing).
- [ ] Run `ruff` for linting/formatting.
- [ ] Run `mypy` for type checking.

## Phase 4: Documentation & Finalize
- [ ] Create `README.md` with usage instructions.
- [ ] Create `sample_data.csv` for demonstration.
- [ ] Verify `report.html` output manually.
