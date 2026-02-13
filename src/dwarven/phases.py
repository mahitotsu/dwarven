"""フェーズ実行ロジック"""
import time
from pathlib import Path

from .config import logger


class PhaseExecutor:
    """3フェーズの実行を管理"""
    
    def __init__(self, session, requirements_path: Path):
        self.session = session
        self.requirements_path = requirements_path
        self.phase_times = {}
        
        # Phase開始時のトークン状態を記録
        self.phase_start_tokens = {
            'input': 0,
            'output': 0,
            'total': 0
        }
    
    def _log_phase_start(self, phase_num: int, phase_name: str):
        """フェーズ開始時のログ出力"""
        logger.info("=" * 60)
        logger.info(f"📦 Phase {phase_num}: {phase_name}")
        logger.info("=" * 60)
        
        # 開始時のトークン数を記録
        self.phase_start_tokens = {
            'input': self.session.total_input_tokens,
            'output': self.session.total_output_tokens,
            'total': self.session.total_input_tokens + self.session.total_output_tokens
        }
    
    def _log_phase_end(self, phase_num: int, phase_name: str, duration: float):
        """フェーズ終了時のログ出力（トークン情報あり）"""
        # このPhaseで消費したトークンを計算
        phase_input = self.session.total_input_tokens - self.phase_start_tokens['input']
        phase_output = self.session.total_output_tokens - self.phase_start_tokens['output']
        phase_total = phase_input + phase_output
        
        # 累積トークン
        total_tokens = self.session.total_input_tokens + self.session.total_output_tokens
        
        logger.info("-" * 60)
        logger.info(f"✅ Phase {phase_num} COMPLETED ({duration:.1f}s)")
        logger.info("-" * 60)
        
        # このPhaseのトークン使用量
        logger.info("Token Usage (this phase):")
        logger.info(f"  Input tokens      : {phase_input:,}")
        logger.info(f"  Output tokens     : {phase_output:,}")
        logger.info(f"  Total tokens      : {phase_total:,}")
        
        # 累積使用量
        logger.info("Token Usage (cumulative):")
        logger.info(f"  Input tokens      : {self.session.total_input_tokens:,}")
        logger.info(f"  Output tokens     : {self.session.total_output_tokens:,}")
        logger.info(f"  Total tokens      : {total_tokens:,}")
        logger.info(f"  Cache read        : {self.session.total_cache_read_tokens:,}")
        logger.info(f"  Cache write       : {self.session.total_cache_write_tokens:,}")
        logger.info(f"  Total cost        : {self.session.total_cost}")
        
        # コンテキスト使用率
        if self.session.token_limit > 0:
            current_tokens = self.session.current_tokens or total_tokens
            usage_percent = (current_tokens / self.session.token_limit) * 100
            logger.info(f"  Context usage     : {usage_percent:.1f}% ({current_tokens:,} / {self.session.token_limit:,})")
            
            if usage_percent > 80:
                logger.warning("⚠️  Context window usage is over 80%!")
        
        # モデル使用回数
        logger.info(f"  Model usage       : {self.session.model_usage_count}")
        logger.info(f"  Messages          : {self.session.messages_count}")
        
        logger.info("=" * 60)
        logger.info("")
    
    async def execute_all(self):
        """3フェーズを順次実行"""
        logger.info("🚀 作業を開始します...")
        logger.info("")
        
        await self._execute_phase1()
        await self._execute_phase2()
        await self._execute_phase3()
        
        return self.phase_times
    
    async def _execute_phase1(self):
        """フェーズ1: 要件分解と設計"""
        phase1_start = time.time()
        self._log_phase_start(1, "要件分解と設計")
        
        requirements_container_path = f"/workspace/requirements{self.requirements_path.suffix}"
        phase1_prompt = f"""要件ファイル「{requirements_container_path}」の内容に基づいて、要件分解と設計ドキュメントを作成してください。

【このフェーズでやること】
1. {requirements_container_path} をdocs/00_requirements.mdとして保存（後続フェーズで参照するため）
2. 要件の概要整理（docs/01_overview.md）
3. アーキテクチャ設計（docs/02_architecture.md）
4. データモデル設計（docs/03_data_model.md）
5. 主要な設計判断のADR（docs/04_adr.md）
6. タスク分解（docs/05_tasks.md）

【依存管理の必須要件】
- pyproject.tomlを使用する場合、必ず[project]セクションにdependenciesを記載すること
- dependenciesには実行に必要なライブラリを、optional-dependencies.devには開発ツール（pytest, black, mypyなど）を記載

作業ディレクトリ: /workspace
"""
        
        try:
            await self.session.send_prompt_and_wait(phase1_prompt)
        except Exception as phase1_error:
            logger.error(f"フェーズ1実行中にエラー: {phase1_error}")
            raise
        
        phase1_end = time.time()
        phase1_duration = phase1_end - phase1_start
        self.phase_times["フェーズ1: 要件分解と設計"] = phase1_duration
        self._log_phase_end(1, "要件分解と設計", phase1_duration)
    
    async def _execute_phase2(self):
        """フェーズ2: 実装"""
        phase2_start = time.time()
        self._log_phase_start(2, "実装")
        
        phase2_prompt = f"""設計ドキュメント（docs/01_overview.md～05_tasks.md）に基づいて、実装を行ってください。

【このフェーズでやること】
1. ソースコードの実装（src/配下）
2. 依存関係の定義
   - pyproject.toml の [project] dependencies = [...] に実行時依存を記載
   - pyproject.toml の [project.optional-dependencies] dev = [...] に開発依存を記載
     * 必須: pytest, pytest-cov（カバレッジ計測用）, black, mypy
   - requirements.txt も作成（uv syncが失敗した場合のフォールバック用）
3. サンプルデータやサンプル設定ファイルがあれば作成

【必須確認事項】
- pyproject.toml の dependencies セクションが正しく記載されているか
- pytest-cov が dev 依存に含まれているか
- requirements.txt も作成されているか

【実装完了後の必須タスク】
- python-setup-dependencies スキルを使用して、依存関係をインストールしてください
  （Python用スキル: .github/skills/python-setup-dependencies/SKILL.md を読んで、その指示に従って uv venv と uv sync --extra dev を実行）

作業ディレクトリ: /workspace
"""
        
        try:
            await self.session.send_prompt_and_wait(phase2_prompt)
        except Exception as phase2_error:
            logger.error(f"フェーズ2実行中にエラー: {phase2_error}")
            raise
        
        phase2_end = time.time()
        phase2_duration = phase2_end - phase2_start
        self.phase_times["フェーズ2: 実装"] = phase2_duration
        self._log_phase_end(2, "実装", phase2_duration)
    
    async def _execute_phase3(self):
        """フェーズ3: テストと品質"""
        phase3_start = time.time()
        self._log_phase_start(3, "テストと品質")
        
        phase3_prompt = f"""実装に対するテストと品質設定を行ってください。

【このフェーズでやること】
1. テストコード（tests/配下）
2. テスト計画（docs/06_test_plan.md）
3. README.md（セットアップ、実行、テスト手順）

【品質ツール】
- pytest + pytest-cov: テスト実行とカバレッジ計測
- black: コードフォーマット
- mypy: 型チェック
- ruff: Linter（オプション）

【テスト・品質チェック実行の必須タスク】
以下のPythonスキル（.github/skills/）を使用して、実際にテストと品質チェックを実行してください：

1. python-run-tests スキルを使用して、カバレッジ付きテストを実行
   （スキルファイル .github/skills/python-run-tests/SKILL.md を読んで、.venv/bin/python -m pytest --cov=src --cov-report=term-missing を実行）

2. python-run-quality-checks スキルを使用して、品質チェックを実行
   （スキルファイル .github/skills/python-run-quality-checks/SKILL.md を読んで、black と mypy を実行）

3. 実行結果をdocs/07_quality_report.mdに記録
   - pytest の実行結果（成功/失敗件数、実行時間）
   - カバレッジレポート（全体カバー率、各ファイルのカバー率、カバーされていない行）
   - black の実行結果（フォーマット済みファイル数、修正が必要なファイルなど）
   - mypy の実行結果（型エラーの有無、チェックしたファイル数など）
   - 総合評価とコメント

【要件充足性の確認（検収資料）】
docs/08_acceptance_report.md を作成し、以下を記載してください：

- docs/00_requirements.md に記載された各要件項目（機能、技術要件、出力形式など）を参照
- 各要件項目に対する実装状況と対応箇所（ファイル名と機能の説明）
- テスト結果による検証状況（docs/07_quality_report.mdを参照）
- 充足度の評価（✅実装済み / ⚠️部分実装 / ❌未実装）
- 検収可否の総合判定

このレポートが検収の根拠資料となります。

【生成物サマリの作成】
docs/99_generation_summary.md を作成し、以下を記載してください：

- 生成したファイルの一覧と役割
- 定量データ（各カテゴリのファイル数）:
  * ドキュメント（docs/）: X件
  * ソースコード（src/）: X件
  * テストコード（tests/）: X件
  * 設定ファイル: X件
  * その他: X件
  * 合計: X件
- プロジェクト概要と主要な成果物の説明

作業ディレクトリ: /workspace
"""
        
        try:
            await self.session.send_prompt_and_wait(phase3_prompt)
        except Exception as phase3_error:
            logger.error(f"フェーズ3実行中にエラー: {phase3_error}")
            raise
        
        phase3_end = time.time()
        phase3_duration = phase3_end - phase3_start
        self.phase_times["フェーズ3: テストと品質"] = phase3_duration
        self._log_phase_end(3, "テストと品質", phase3_duration)
