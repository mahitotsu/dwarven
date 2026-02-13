# アーキテクチャ設計

## システム構成

### レイヤー構造
```
┌─────────────────────────────────────┐
│      CLI Layer (main.py)            │  ← コマンドライン引数処理
├─────────────────────────────────────┤
│   Application Layer (analyzer.py)   │  ← ビジネスロジック
├─────────────────────────────────────┤
│   Service Layer                      │
│   ├─ data_loader.py                 │  ← データ読み込み
│   ├─ statistics.py                  │  ← 統計計算
│   ├─ visualizer.py                  │  ← グラフ生成
│   └─ reporter.py                    │  ← レポート生成
├─────────────────────────────────────┤
│   Model Layer (models.py)           │  ← データモデル定義
└─────────────────────────────────────┘
```

## ディレクトリ構造

```
csv-data-analyzer/
├── pyproject.toml           # プロジェクト設定
├── README.md                # 使用方法
├── .gitignore              # Git除外設定
├── src/
│   └── csv_analyzer/       # メインパッケージ
│       ├── __init__.py
│       ├── main.py         # エントリポイント
│       ├── analyzer.py     # メインロジック
│       ├── models.py       # データモデル
│       ├── services/
│       │   ├── __init__.py
│       │   ├── data_loader.py
│       │   ├── statistics.py
│       │   ├── visualizer.py
│       │   └── reporter.py
│       └── templates/
│           └── report.html # HTMLテンプレート
├── tests/
│   ├── __init__.py
│   ├── test_analyzer.py
│   ├── test_data_loader.py
│   ├── test_statistics.py
│   ├── test_visualizer.py
│   └── test_reporter.py
├── data/
│   └── sample_data.csv     # サンプルデータ
└── docs/                   # 設計ドキュメント
    ├── 00_requirements.md
    ├── 01_overview.md
    ├── 02_architecture.md
    ├── 03_data_model.md
    ├── 04_adr.md
    └── 05_tasks.md
```

## コンポーネント詳細

### 1. CLI Layer (main.py)
- **責務**: コマンドライン引数のパース、エントリポイント提供
- **依存**: argparse, analyzer.py
- **公開インターフェース**: `main()` 関数

### 2. Application Layer (analyzer.py)
- **責務**: 全体のワークフロー制御、各サービスの調整
- **依存**: すべてのserviceモジュール
- **主要メソッド**: 
  - `analyze_csv(filepath: Path, output: Path) -> AnalysisResult`

### 3. Service Layer

#### data_loader.py
- **責務**: CSVファイルの読み込み、バリデーション
- **依存**: pandas, models.py
- **主要メソッド**:
  - `load_csv(filepath: Path) -> DataFrame`
  - `validate_data(df: DataFrame) -> bool`

#### statistics.py
- **責務**: 統計情報の計算
- **依存**: pandas, numpy, models.py
- **主要メソッド**:
  - `calculate_statistics(df: DataFrame) -> Statistics`

#### visualizer.py
- **責務**: グラフの生成
- **依存**: matplotlib, models.py
- **主要メソッド**:
  - `create_timeseries_plot(df: DataFrame) -> Figure`
  - `create_histogram(df: DataFrame) -> Figure`

#### reporter.py
- **責務**: HTMLレポートの生成、コンソール出力
- **依存**: jinja2, models.py
- **主要メソッド**:
  - `generate_html_report(result: AnalysisResult, output: Path) -> None`
  - `print_summary(stats: Statistics) -> None`

### 4. Model Layer (models.py)
- **責務**: データ構造の定義
- **依存**: dataclasses, datetime
- **定義クラス**:
  - `DataRecord`: 単一のデータレコード
  - `Statistics`: 統計情報
  - `AnalysisResult`: 分析結果全体

## データフロー

```
1. CLI → main()
2. main() → analyzer.analyze_csv()
3. analyze_csv() → data_loader.load_csv()
4. analyze_csv() → statistics.calculate_statistics()
5. analyze_csv() → visualizer.create_plots()
6. analyze_csv() → reporter.generate_html_report()
7. analyze_csv() → reporter.print_summary()
8. main() ← 完了
```

## 技術スタック

### コアライブラリ
- **pandas**: CSV読み込み、データ操作
- **matplotlib**: グラフ生成
- **jinja2**: HTMLテンプレートエンジン

### 開発ツール
- **pytest**: テストフレームワーク
- **ruff**: リンター・フォーマッター
- **mypy**: 型チェック

### パッケージ管理
- **uv**: 依存関係管理
- **pyproject.toml**: プロジェクト設定

## エラーハンドリング戦略

1. **ファイル読み込みエラー**
   - ファイルが存在しない → FileNotFoundError
   - 読み込み権限なし → PermissionError

2. **データ検証エラー**
   - 必須カラムが存在しない → ValueError
   - データ型が不正 → ValueError

3. **処理エラー**
   - 統計計算エラー → RuntimeError
   - グラフ生成エラー → RuntimeError

すべてのエラーは適切なメッセージとともにユーザーに表示される。
