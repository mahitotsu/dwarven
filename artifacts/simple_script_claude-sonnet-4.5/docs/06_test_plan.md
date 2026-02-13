# テスト計画

## テスト方針

本プロジェクトでは、以下の方針でテストを実施します：

1. **ユニットテスト**: 各関数の独立した動作を検証
2. **統合テスト**: 複数の関数を組み合わせたend-to-endの動作を検証
3. **異常系テスト**: エラーハンドリングが適切に機能することを検証

## テスト対象

### 主要な関数

| 関数名 | 責務 | テスト優先度 |
|--------|------|------------|
| `parse_arguments()` | コマンドライン引数の解析 | 中 |
| `load_data()` | CSVファイルの読み込みとバリデーション | 高 |
| `calculate_statistics()` | 統計量の計算 | 高 |
| `generate_charts()` | グラフの生成 | 高 |
| `generate_report()` | HTMLレポートの生成 | 高 |
| `main()` | メイン処理フロー | 中（統合テストでカバー） |

## テストケース一覧

### 1. データ読み込み（load_data）

#### 正常系
- **test_load_valid_csv**: 正しい形式のCSVファイルを読み込む
- **test_data_sorted_by_date**: データが日付順にソートされることを確認

#### 異常系
- **test_load_nonexistent_file**: 存在しないファイルを指定した場合
- **test_load_csv_missing_column**: 必須カラムが不足している場合
- **test_load_csv_with_missing_values**: 欠損値が含まれる場合

### 2. 統計計算（calculate_statistics）

#### 正常系
- **test_calculate_basic_statistics**: 基本統計量が正しく計算される
- **test_statistics_types**: 返り値の型が正しい

#### エッジケース
- **test_single_data_point**: 1件だけのデータの統計量計算

### 3. グラフ生成（generate_charts）

#### 正常系
- **test_generate_charts**: グラフが正しく生成され、Base64エンコードされる

### 4. レポート生成（generate_report）

#### 正常系
- **test_generate_html_report**: HTMLレポートが正しく生成される

### 5. 統合テスト（Integration）

#### 正常系
- **test_end_to_end_workflow**: CSV読み込みからHTMLレポート生成までの完全なフロー

#### エッジケース
- **test_single_data_point**: 1件のデータでも処理が完了する

## テストデータ

### サンプルCSV（5行）
```csv
date,value
2024-01-01,100
2024-01-02,110
2024-01-03,105
2024-01-04,115
2024-01-05,120
```

### 不正なCSV（カラム不足）
```csv
date,other
2024-01-01,100
2024-01-02,110
```

### 欠損値を含むCSV
```csv
date,value
2024-01-01,100
2024-01-02,
2024-01-03,105
```

## カバレッジ目標

- **全体カバレッジ**: 80%以上
- **重要な関数**: 90%以上
  - `load_data()`
  - `calculate_statistics()`
  - `generate_charts()`
  - `generate_report()`

## テスト実行環境

### 必要なパッケージ
- pytest >= 7.4.0
- pytest-cov >= 4.1.0

### 実行コマンド

```bash
# 全テスト実行
pytest

# カバレッジ付き実行
pytest --cov=. --cov-report=term-missing --cov-report=html

# 詳細出力
pytest -v

# 特定のテストクラスのみ実行
pytest tests/test_analyze.py::TestLoadData -v
```

## 品質基準

### 合格基準
- ✅ 全テストケースが合格
- ✅ カバレッジが80%以上
- ✅ 重大なバグが存在しない

### 不合格基準
- ❌ 1件でもテストが失敗
- ❌ カバレッジが70%未満
- ❌ 重大なバグが発見される

## テスト実行スケジュール

1. **開発中**: 機能実装ごとにユニットテストを作成・実行
2. **実装完了後**: 統合テストを作成・実行
3. **リリース前**: 全テストを実行し、カバレッジを確認

## 既知の制限事項

- `main()` 関数と `parse_arguments()` 関数は、コマンドライン引数の性質上、テストが複雑になるため、統合テストでカバー
- GUI要素がないため、ビジュアルリグレッションテストは実施しない
- 生成されるグラフの視覚的な正しさは手動で確認

## 今後の改善案

- CI/CDパイプラインへのテスト自動実行の組み込み
- パフォーマンステストの追加（大規模データでの処理時間測定）
- エラーメッセージの国際化対応テスト
