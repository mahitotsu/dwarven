# テスト計画

## テスト概要

### 目的
CSV Data Analyzerの機能が要件通りに実装されていることを検証し、コード品質を保証する。

### テスト方針
- **単体テスト**: 各モジュールの独立した動作を検証
- **統合テスト**: モジュール間の連携を検証
- **エンドツーエンドテスト**: CLI経由での全体フローを検証
- **品質チェック**: 型安全性、コードフォーマット、Lintingを確認

## テスト範囲

### 1. データモデル層（models.py）
**テストファイル**: `tests/test_models.py`

#### DataRecord
- ✅ 有効なレコードの作成
- ✅ 不正な日付型のバリデーション
- ✅ 不正な数値型のバリデーション

#### Statistics
- ✅ 辞書への変換（to_dict）
- ✅ 文字列表現（__str__）

#### PlotData
- ✅ インスタンスの作成

#### AnalysisResult
- ✅ レポートコンテキストへの変換（to_report_context）

### 2. データ読み込み層（data_loader.py）
**テストファイル**: `tests/test_data_loader.py`

#### load_csv
- ✅ 有効なCSVの読み込み
- ✅ ファイルが存在しない場合のエラー
- ✅ カラムが不足している場合のエラー
- ✅ 不正な日付形式のエラー
- ✅ NaN値のエラー

#### validate_data
- ✅ 有効なDataFrameの検証
- ✅ 必須カラムの不足検出
- ✅ 空のDataFrameの検出
- ✅ 不正な日付形式の検出
- ✅ 数値でない値の検出

### 3. 統計計算層（statistics.py）
**テストファイル**: `tests/test_statistics.py`

#### calculate_statistics
- ✅ 基本的な統計計算（平均、中央値、最大値、最小値、標準偏差）
- ✅ 単一値の統計計算
- ✅ valueカラムが存在しない場合のエラー
- ✅ 統計値の型チェック

### 4. 可視化層（visualizer.py）
**テストファイル**: `tests/test_visualizer.py`

#### create_timeseries_plot
- ✅ Figureオブジェクトの生成
- ✅ dateカラムが存在しない場合のエラー
- ✅ valueカラムが存在しない場合のエラー

#### create_histogram
- ✅ Figureオブジェクトの生成
- ✅ valueカラムが存在しない場合のエラー
- ✅ 単一値でもグラフ生成可能

### 5. レポート生成層（reporter.py）
**テストファイル**: `tests/test_reporter.py`

#### generate_html_report
- ✅ HTMLファイルの生成
- ✅ HTMLに統計情報が含まれる

#### print_summary
- ✅ サマリーの出力

### 6. アプリケーション層（analyzer.py）
**テストファイル**: `tests/test_analyzer.py`

#### analyze_csv
- ✅ 正常な分析処理
- ✅ 存在しないファイルのエラー
- ✅ 不正なCSVファイルのエラー

### 7. CLI層（main.py）
**テストファイル**: `tests/test_main.py`

#### main
- ✅ デフォルト出力ファイル名での実行
- ✅ カスタム出力ファイル名での実行
- ✅ 存在しないファイルでのエラー終了
- ✅ サマリーの出力確認

## テストカバレッジ目標

| カテゴリ | 目標カバレッジ | 備考 |
|---------|--------------|------|
| 全体 | 80%以上 | - |
| models.py | 90%以上 | コアモデル |
| data_loader.py | 90%以上 | 重要な入力処理 |
| statistics.py | 90%以上 | 計算ロジック |
| visualizer.py | 80%以上 | 可視化 |
| reporter.py | 80%以上 | レポート生成 |
| analyzer.py | 90%以上 | メインロジック |
| main.py | 80%以上 | CLI |

## 品質チェック項目

### 1. pytest実行
```bash
source .venv/bin/activate
pytest --cov=csv_analyzer --cov-report=html --cov-report=term-missing
```

**確認項目**:
- すべてのテストがパス
- カバレッジが目標値以上
- カバーされていない重要な行の特定

### 2. コードフォーマット（black）
```bash
black src/ tests/
```

**確認項目**:
- PEP 8準拠のフォーマット
- 一貫したコードスタイル
- 自動修正されたファイル数

### 3. 型チェック（mypy）
```bash
mypy src/
```

**確認項目**:
- 型エラーの有無
- strictモードでのチェック
- 型ヒントの網羅性

### 4. Linting（ruff）
```bash
ruff check src/ tests/
```

**確認項目**:
- コーディング規約違反の有無
- 未使用のインポート
- 潜在的なバグの検出

## テスト実行環境

- Python: 3.11.2
- OS: Linux
- 仮想環境: uv venv

## テスト実行手順

### 1. 環境準備
```bash
cd /workspace
source .venv/bin/activate
```

### 2. テスト実行
```bash
pytest --cov=csv_analyzer --cov-report=html --cov-report=term-missing -v
```

### 3. 品質チェック実行
```bash
# フォーマット
black src/ tests/ --check

# 型チェック
mypy src/

# Linting
ruff check src/ tests/
```

### 4. 統合テスト（実際のCSV処理）
```bash
python -m csv_analyzer data/sample_data.csv -o test_report.html
```

## 成功基準

### テスト
- ✅ すべてのテストケースがパス
- ✅ 全体カバレッジ80%以上
- ✅ 重要モジュール（models, data_loader, statistics, analyzer）は90%以上

### 品質
- ✅ black実行でフォーマット違反なし
- ✅ mypy実行で型エラーなし
- ✅ ruff実行でLintエラーなし

### 機能
- ✅ サンプルデータで正常にHTMLレポート生成
- ✅ 生成されたHTMLレポートが正しく表示される
- ✅ エラーケースで適切なエラーメッセージが表示される

## テスト実施スケジュール

1. **単体テスト実行** - python-run-testsスキル使用
2. **品質チェック実行** - python-run-quality-checksスキル使用
3. **結果の記録** - docs/07_quality_report.md作成
4. **要件充足性確認** - docs/08_acceptance_report.md作成

## 既知の制限事項

- 大規模なCSVファイル（メモリに収まらないサイズ）は対象外
- 日付形式はYYYY-MM-DDのみサポート
- UTF-8エンコーディングのCSVのみサポート

## テスト対象外

- パフォーマンステスト
- セキュリティテスト
- ブラウザでのHTMLレポート表示テスト（手動確認のみ）
- 複数プラットフォームでの動作テスト（Linux環境のみ）
