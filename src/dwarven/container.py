"""Dockerコンテナ管理"""
import subprocess
import shutil
import socket
import time
from pathlib import Path
from typing import Optional

from .config import logger, IMAGE_NAME, CONTAINER_NAME_PREFIX


class DockerContainerManager:
    """Dockerコンテナのライフサイクルを管理"""
    
    def __init__(self, requirements_path: Path, output_path: Path, github_token: str):
        self.requirements_path = requirements_path
        self.output_path = output_path
        self.github_token = github_token
        self.container_name: Optional[str] = None
        self.dockerfile_path = Path(__file__).parent.parent.parent / "Dockerfile"
    
    def build_image_if_needed(self):
        """イメージが存在しない場合はビルド"""
        result = subprocess.run(
            ["docker", "images", "-q", IMAGE_NAME],
            capture_output=True,
            text=True
        )
        
        if not result.stdout.strip():
            logger.info(f"🏗️  Docker イメージをビルド中: {IMAGE_NAME}")
            build_result = subprocess.run(
                ["docker", "build", "-t", IMAGE_NAME, "-f", str(self.dockerfile_path), "."],
                cwd=self.dockerfile_path.parent,
                capture_output=True,
                text=True
            )
            
            if build_result.returncode != 0:
                logger.error(f"❌ Docker ビルドに失敗:\n{build_result.stderr}")
                raise RuntimeError("Docker build failed")
            
            logger.info(f"✅ イメージビルド完了: {IMAGE_NAME}")
        else:
            logger.debug(f"✅ イメージが存在します: {IMAGE_NAME}")
    
    def start_container(self) -> str:
        """コンテナを起動"""
        import secrets
        
        self.build_image_if_needed()
        
        # ユニークなコンテナ名を生成
        suffix = secrets.token_hex(4)
        self.container_name = f"{CONTAINER_NAME_PREFIX}{suffix}"
        
        logger.info(f"🚀 コンテナを起動中: {self.container_name}")
        
        result = subprocess.run(
            [
                "docker", "run",
                "--rm",  # 終了時に自動削除
                "-d",  # デタッチモード
                "--name", self.container_name,
                "-e", f"GITHUB_TOKEN={self.github_token}",
                "-p", "3000:3000",
                IMAGE_NAME
            ],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            logger.error(f"❌ コンテナ起動に失敗:\n{result.stderr}")
            raise RuntimeError("Failed to start container")
        
        # GitHub Copilot CLIサーバーが起動するまで待機
        logger.info("⏳ GitHub Copilot CLIサーバーの起動を待機中...")
        if self._wait_for_server_ready(timeout=30):
            logger.info("✅ GitHub Copilot CLIサーバーが起動しました")
        else:
            logger.warning("⚠️  GitHub Copilot CLIサーバーの起動確認がタイムアウトしましたが続行します")
        
        logger.info(f"✅ コンテナが起動しました: {self.container_name}")
        
        # ログストリーミング開始
        self._start_log_streaming()
        
        return self.container_name
    
    def _wait_for_server_ready(self, timeout: int = 30) -> bool:
        """サーバーが完全に起動するまで待機（ログを監視）
        
        Args:
            timeout: タイムアウト秒数
            
        Returns:
            サーバーが起動した場合はTrue、タイムアウトした場合はFalse
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # コンテナのログを取得
                result = subprocess.run(
                    ["docker", "logs", self.container_name],
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                # "CLI server listening" メッセージを確認
                log_output = result.stdout + result.stderr
                if "CLI server listening" in log_output:
                    # ログメッセージが表示された後、少し待機してから接続
                    time.sleep(1)
                    return True
            except (subprocess.TimeoutExpired, Exception):
                pass
            time.sleep(0.5)
        return False
    
    def _wait_for_port(self, host: str, port: int, timeout: int = 30) -> bool:
        """指定されたポートが利用可能になるまで待機
        
        Args:
            host: ホスト名またはIPアドレス
            port: ポート番号
            timeout: タイムアウト秒数
            
        Returns:
            ポートが利用可能になった場合はTrue、タイムアウトした場合はFalse
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                with socket.create_connection((host, port), timeout=1):
                    return True
            except (socket.timeout, ConnectionRefusedError, OSError):
                time.sleep(0.5)
        return False
    
    def _start_log_streaming(self):
        """コンテナログをバックグラウンドでストリーミング"""
        def stream_logs():
            try:
                process = subprocess.Popen(
                    ["docker", "logs", "-f", self.container_name],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1
                )
                for line in process.stdout:
                    logger.info(f"[Container] {line.rstrip()}")
            except Exception as e:
                logger.debug(f"ログストリーミング終了: {e}")
        
        import threading
        log_thread = threading.Thread(target=stream_logs, daemon=True)
        log_thread.start()
        logger.info("🔍 コンテナログ監視を開始しました")
    
    def copy_requirements_to_container(self):
        """要件ファイルをコンテナにコピー"""
        requirements_container_path = f"/workspace/requirements{self.requirements_path.suffix}"
        logger.info(f"📤 要件ファイルをコンテナにコピー: {requirements_container_path}")
        
        result = subprocess.run(
            ["docker", "cp", str(self.requirements_path), f"{self.container_name}:{requirements_container_path}"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            logger.error(f"❌ 要件ファイルのコピーに失敗: {result.stderr}")
            raise RuntimeError("Failed to copy requirements file to container")
    
    def copy_outputs_from_container(self):
        """成果物をコンテナからホストにコピー"""
        logger.info("")
        logger.info("📦 成果物をコンテナから取得中...")
        
        # 出力ディレクトリをクリーンアップ
        if self.output_path.exists():
            shutil.rmtree(self.output_path)
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        # docker cpで成果物を取得
        result = subprocess.run(
            ["docker", "cp", f"{self.container_name}:/workspace/.", str(self.output_path)],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            # .githubディレクトリを削除（スキルと要件ファイルが含まれるため）
            github_dir = self.output_path / ".github"
            if github_dir.exists():
                shutil.rmtree(github_dir)
            
            # 要件ファイルも削除（コピーしたものなので不要）
            req_file = self.output_path / f"requirements{self.requirements_path.suffix}"
            if req_file.exists():
                req_file.unlink()
            
            # 不要なビルド成果物やキャッシュを削除
            cleanup_patterns = [
                "__pycache__",
                ".mypy_cache",
                ".pytest_cache",
                ".venv",
                "venv",
                ".ruff_cache",
                "*.pyc",
                "*.pyo",
                "*.pyd",
                ".DS_Store",
                "*.egg-info",
                "dist",
                "build",
                ".coverage",
                "htmlcov",
                "node_modules",
                ".next",
                ".nuxt",
            ]
            
            for pattern in cleanup_patterns:
                if "*" in pattern:
                    # ワイルドカード付きパターン
                    for item in self.output_path.rglob(pattern):
                        if item.is_file():
                            item.unlink()
                else:
                    # ディレクトリパターン
                    for item in self.output_path.rglob(pattern):
                        if item.is_dir():
                            shutil.rmtree(item)
            
            logger.info(f"✅ 成果物を取得しました: {self.output_path}")
        else:
            logger.error(f"❌ 成果物の取得に失敗: {result.stderr}")
    
    def cleanup(self):
        """コンテナをクリーンアップ"""
        if not self.container_name:
            return
        
        logger.debug(f"🧹 コンテナをクリーンアップ中: {self.container_name}")
        
        # コンテナを停止
        subprocess.run(
            ["docker", "stop", self.container_name],
            capture_output=True,
            text=True
        )
        
        logger.debug(f"✅ コンテナをクリーンアップしました: {self.container_name}")
