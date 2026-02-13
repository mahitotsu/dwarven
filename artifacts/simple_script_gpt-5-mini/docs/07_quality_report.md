# Quality Report

## pytest

3 passed in 3.06s

### Coverage

Overall coverage: 74%

Per-file:
- src/__init__.py: 100%
- src/analyze.py: 68% (missing main/CLI branches)
- src/cli.py: 0% (not executed by tests)
- src/io.py: 90% (one branch not covered)
- src/processing.py: 100%
- src/report.py: 100%
- src/viz.py: 100%

Missing lines are primarily CLI entrypoints and error branches.

## black

black reported 3 files that would be reformatted (src/report.py, src/cli.py, src/analyze.py). Run `black .` to apply formatting.

## mypy

mypy reported errors due to missing library stubs for pandas in multiple files. Suggested remediations:
- install pandas-stubs in dev dependencies, or
- configure mypy to ignore missing imports for pandas in mypy.ini or pyproject.toml.

## 総合評価

- テスト: 合格（3 tests passed）
- カバレッジ: 74%（CLIと例外パスのカバレッジ追加が望ましい）
- 品質ツール: black の自動整形を推奨。mypy は pandas のスタブ未インストールのためエラーが出ている。
