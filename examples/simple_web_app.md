# 簡単なWebアプリケーションの作成

## 要件

FastAPIを使った簡単なTODOアプリケーションを作成してください。

## 機能要件

1. TODOアイテムの一覧表示（GET /todos）
2. TODOアイテムの追加（POST /todos）
3. TODOアイテムの完了/未完了の切り替え（PUT /todos/{id}/toggle）
4. TODOアイテムの削除（DELETE /todos/{id}）

## 技術要件

- FastAPIを使用
- データはメモリ内で管理（データベース不要）
- Pydanticモデルを使用してデータ検証
- uvicornで起動できること

## ファイル構成

以下のファイルを作成してください：

1. `main.py` - FastAPIアプリケーション本体
2. `models.py` - Pydanticモデルの定義
3. `requirements.txt` - 依存パッケージのリスト
4. `README.md` - 実行方法の説明

## その他

- コードには適切なコメントを付けてください
- RESTful APIのベストプラクティスに従ってください
