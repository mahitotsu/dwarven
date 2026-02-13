# テスト計画書

## 目的
本ドキュメントは、Data Analysis Toolの品質を保証するためのテスト戦略を定義する。

## テスト範囲
### 単体テスト (Unit Testing)
各モジュールの関数・クラスレベルでの動作確認を行う。
- `loader.py`: CSV読み込み、型変換、バリデーション
- `analysis.py`: 統計計算ロジック
- `plotting.py`: グラフ生成（画像データの生成確認）
- `report.py`: HTML生成（ファイル出力確認）

### 結合テスト (Integration Testing)
- `main.py` を介した一連の処理フロー（読み込み→分析→グラフ→レポート）が正常に動作することを確認する。

## テストツール
- **Test Runner**: pytest
- **Coverage**: pytest-cov
- **Linting**: ruff, black
- **Type Checking**: mypy

## テストケース設計方針

### 1. Data Loader (`loader.py`)
- **正常系**:
    - 正しいフォーマットのCSVを読み込めること。
    - `date`列がdatetime型、`value`列がnumeric型に変換されること。
    - 日付順にソートされること。
- **異常系**:
    - ファイルが存在しない場合 (`FileNotFoundError`)。
    - 必須カラム (`date`, `value`) が欠けている場合 (`ValueError`)。
    - データ型変換に失敗する場合（日付不正、数値不正）。

### 2. Analyzer (`analysis.py`)
- **正常系**:
    - 平均、中央値、最大、最小が正しく計算されること。
    - データが空の場合のハンドリング（全て0またはNone等の規定値）。
- **境界値**:
    - データが1件のみの場合。

### 3. Plotter (`plotting.py`)
- **正常系**:
    - DataFrameを渡してBase64文字列が返ること。
    - 空のDataFrameの場合の挙動。

### 4. Report Generator (`report.py`)
- **正常系**:
    - 指定されたパスにHTMLファイルが生成されること。
    - 生成されたHTMLに必要な文字列（統計値など）が含まれていること。

### 5. Main (`main.py`)
- **正常系**:
    - 引数を受け取ってエラーなく終了すること（`SystemExit(0)` または例外なし）。
