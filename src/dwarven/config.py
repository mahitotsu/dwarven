"""設定とロガー"""
import logging
import sys

# 定数
IMAGE_NAME = "dwarven-copilot"
CONTAINER_NAME_PREFIX = "dwarven-copilot-"
COPILOT_CLI_PORT = 3000

# ロガー設定
logger = logging.getLogger("dwarven")


class RelativeTimeFormatter(logging.Formatter):
    """起動時からの経過時間を表示するフォーマッタ"""
    def format(self, record):
        elapsed_seconds = record.relativeCreated / 1000.0
        record.elapsed = f"[+{elapsed_seconds:6.1f}s]"
        return super().format(record)


def setup_logger(debug: bool = False):
    """ロガーを初期化"""
    level = logging.DEBUG if debug else logging.INFO
    logger.setLevel(level)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        
        formatter = RelativeTimeFormatter(
            '%(elapsed)s %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger
