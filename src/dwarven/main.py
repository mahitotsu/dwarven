"""Dwarven - GitHub Copilot CLI を使った自動開発システム"""
import argparse
import asyncio
import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

from .config import setup_logger, logger
from .container import DockerContainerManager
from .copilot_session import CopilotSession
from .phases import PhaseExecutor


async def run(requirements_file: str, output_dir: str, model: str, debug: bool):
    """メイン処理"""
    setup_logger(debug)
    
    # .envファイルを読み込み
    load_dotenv()
    
    # パス設定
    requirements_path = Path(requirements_file).resolve()
    output_path = Path(output_dir).resolve()
    
    if not requirements_path.exists():
        logger.error(f"❌ 要件ファイルが見つかりません: {requirements_path}")
        sys.exit(1)
    
    logger.info("=" * 60)
    logger.info("🏔️  Dwarven - 自動開発システム")
    logger.info("=" * 60)
    logger.info(f"📄 要件ファイル: {requirements_path}")
    logger.info(f"📁 出力ディレクトリ: {output_path}")
    logger.info(f"🤖 モデル: {model}")
    logger.info("=" * 60)
    logger.info("")
    
    start_time = time.time()
    
    # GitHub Token確認
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        logger.error("❌ GITHUB_TOKEN が設定されていません")
        logger.error("")
        logger.error("以下のいずれかの方法で設定してください：")
        logger.error("   1. export GITHUB_TOKEN=your_token")
        logger.error("   2. .env ファイルに GITHUB_TOKEN=your_token を記載")
        sys.exit(1)
    
    # コンテナ管理
    container = DockerContainerManager(requirements_path, output_path, github_token)
    session = None
    
    try:
        # コンテナ起動とファイルコピー
        container.start_container()
        container.copy_requirements_to_container()
        
        # Copilot CLI接続
        session = CopilotSession()
        await session.connect()
        await session.create_session(model)
        
        # 3フェーズ実行
        executor = PhaseExecutor(session, requirements_path)
        phase_times = await executor.execute_all()
        
        # 全体の終了時刻
        end_time = time.time()
        total_time = end_time - start_time
        
        # 作業完了
        logger.info("")
        logger.info("=" * 60)
        logger.info("✅ 全作業が完了しました！")
        logger.info("=" * 60)
        logger.info(f"📁 成果物: /workspace (コンテナ内)")
        logger.info("")
        logger.info("⏱️  実行時間:")
        for phase_name, duration in phase_times.items():
            logger.info(f"  - {phase_name}: {duration:.1f}秒")
        logger.info(f"  - 合計: {total_time:.1f}秒")
        logger.info("")
        
        # トークン使用状況の総計
        total_tokens = session.total_input_tokens + session.total_output_tokens
        logger.info("📊 トークン使用状況（合計）:")
        logger.info(f"  - Input tokens    : {session.total_input_tokens:,}")
        logger.info(f"  - Output tokens   : {session.total_output_tokens:,}")
        logger.info(f"  - Total tokens    : {total_tokens:,}")
        logger.info(f"  - Cache read      : {session.total_cache_read_tokens:,}")
        logger.info(f"  - Cache write     : {session.total_cache_write_tokens:,}")
        logger.info(f"  - Model usage     : {session.model_usage_count}")
        logger.info(f"  - Total duration  : {session.total_duration_ms/1000:.1f}s")
        logger.info(f"  - Total cost      : {session.total_cost}")
        logger.info("")
        logger.info(f"🤖 Primary model   : {session.first_model or session.requested_model}")
        if session.requested_model != session.first_model:
            logger.info(f"   (requested: {session.requested_model})")
        logger.info("")
        logger.info("💡 成果物は自動的にホストの出力ディレクトリにコピーされています")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"❌ エラーが発生しました: {e}")
        raise
    
    finally:
        # クリーンアップ
        if session:
            await session.close()
        
        container.copy_outputs_from_container()
        container.cleanup()


def main():
    """CLI エントリーポイント"""
    parser = argparse.ArgumentParser(
        description="Dwarven - GitHub Copilot CLI を使った自動開発システム"
    )
    parser.add_argument("requirements", help="要件ファイル (.md)")
    parser.add_argument(
        "-o", "--output",
        dest="output_dir",
        default=None,
        help="出力ディレクトリ (デフォルト: outputs/<requirements_name>)"
    )
    parser.add_argument(
        "-m", "--model",
        default="gpt-5-mini",
        help="使用するモデル (デフォルト: gpt-5-mini [無料], 他: gpt-4.1 [無料], gpt-5.2-codex, claude-sonnet-4.5など)"
    )
    parser.add_argument(
        "-d", "--debug",
        action="store_true",
        help="デバッグログを有効化"
    )
    
    args = parser.parse_args()
    
    # 出力ディレクトリのデフォルト設定
    output_dir = args.output_dir
    if output_dir is None:
        requirement_name = Path(args.requirements).stem
        output_dir = str(Path("outputs") / requirement_name)
    
    try:
        asyncio.run(run(args.requirements, output_dir, args.model, args.debug))
    except KeyboardInterrupt:
        logger.warning("⚠️  中断されました")
        sys.exit(130)


if __name__ == "__main__":
    main()
