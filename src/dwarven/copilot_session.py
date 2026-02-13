"""Copilot CLIセッション管理"""
import asyncio
import logging
import re
from pathlib import Path
from typing import Optional
from copilot import CopilotClient

from .config import logger, COPILOT_CLI_PORT


class CopilotSession:
    """Copilot CLIセッションの管理とイベント処理"""
    
    def __init__(self):
        self.client: Optional[CopilotClient] = None
        self.session = None
        self.done = asyncio.Event()
        self.assistant_message = ""
        self.execution_tracking = {}
        
        # セッション情報追跡
        self.requested_model: Optional[str] = None
        self.first_model: Optional[str] = None  # 最初に確認されたモデル（サマリー用）
        
        # トークン使用状況追跡
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cache_read_tokens = 0
        self.total_cache_write_tokens = 0
        self.total_cost = 0.0
        self.total_duration_ms = 0.0
        self.model_usage_count = 0
        
        # セッション状態追跡
        self.current_tokens = 0
        self.token_limit = 0
        self.messages_count = 0
    
    def _load_custom_agents(self, agents_dir: Path) -> list:
        """./agentsディレクトリからカスタムエージェントを読み込む"""
        custom_agents = []
        
        if not agents_dir.exists():
            logger.debug(f"エージェントディレクトリが見つかりません: {agents_dir}")
            return custom_agents
        
        for agent_file in agents_dir.glob("*.agent.md"):
            try:
                content = agent_file.read_text(encoding='utf-8')
                
                # Frontmatterを解析（---で囲まれた部分）
                frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
                
                if not frontmatter_match:
                    logger.warning(f"エージェントファイルの形式が不正です: {agent_file.name}")
                    continue
                
                frontmatter_text = frontmatter_match.group(1)
                prompt = frontmatter_match.group(2).strip()
                
                # 簡易YAML解析（name と description のみ）
                name_match = re.search(r'^name:\s*(.+)$', frontmatter_text, re.MULTILINE)
                desc_match = re.search(r'^description:\s*(.+)$', frontmatter_text, re.MULTILINE)
                
                if not name_match:
                    logger.warning(f"エージェント名が見つかりません: {agent_file.name}")
                    continue
                
                name = name_match.group(1).strip()
                description = desc_match.group(1).strip() if desc_match else ""
                
                # CustomAgentConfig 形式で追加
                agent_config = {
                    "name": name,
                    "display_name": name.replace("-", " ").title(),
                    "description": description,
                    "prompt": prompt,
                }
                
                custom_agents.append(agent_config)
                logger.info(f"✅ カスタムエージェント読み込み: {name}")
                
            except Exception as e:
                logger.warning(f"エージェント読み込みエラー ({agent_file.name}): {e}")
        
        return custom_agents
    
    async def connect(self):
        """Copilot CLIに接続"""
        cli_url = f"localhost:{COPILOT_CLI_PORT}"
        logger.info(f"🔗 Copilot CLI に接続中...")
        
        self.client = CopilotClient({"cli_url": cli_url})
        await self.client.start()
        logger.debug("✅ Copilot CLI接続完了")
    
    async def create_session(self, model: str):
        """セッションを作成してイベントハンドラを設定"""
        self.requested_model = model
        
        # 利用可能なモデルリストを取得してバリデーション
        logger.debug("利用可能なモデルを確認中...")
        try:
            available_models = await self.client.list_models()
            model_ids = [m.id for m in available_models]
            
            if model not in model_ids:
                logger.warning("=" * 60)
                logger.warning("⚠️  MODEL NOT FOUND")
                logger.warning("=" * 60)
                logger.warning(f"Requested Model : {model}")
                logger.warning("")
                logger.warning("This model is not in the available models list.")
                logger.warning("The system will use a default fallback model.")
                logger.warning("")
                logger.warning("💡 Free models: gpt-5-mini, gpt-4.1")
                logger.warning("💡 See AVAILABLE_MODELS.md for all valid model names")
                logger.warning("")
                logger.warning(f"Available models: {', '.join(model_ids[:5])}...")
                logger.warning("=" * 60)
        except Exception as e:
            logger.debug(f"モデルリスト取得エラー（続行します）: {e}")
        
        # ツール実行を監視するHooks
        tool_counter = 0
        pending_tools = {}
        
        async def on_pre_tool_use(input_data, invocation):
            nonlocal tool_counter
            tool_counter += 1
            exec_id = tool_counter
            tool_name = input_data.get('toolName', 'unknown')
            
            tool_key = f"{tool_name}_{exec_id}"
            pending_tools[tool_key] = (exec_id, tool_name)
            
            return {"permissionDecision": "allow"}
        
        async def on_post_tool_use(input_data, invocation):
            pass
        
        # カスタムエージェントを読み込む
        agents_dir = Path("./agents")
        custom_agents = self._load_custom_agents(agents_dir)
        
        # セッション作成
        logger.debug("セッション作成中...")
        session_config = {
            "model": model,
            "hooks": {
                "pre_tool_use": on_pre_tool_use,
                "post_tool_use": on_post_tool_use,
            }
        }
        
        # カスタムエージェントがあれば追加
        if custom_agents:
            session_config["custom_agents"] = custom_agents
            logger.info(f"カスタムエージェント数: {len(custom_agents)}")
        
        self.session = await self.client.create_session(session_config)
        logger.info("=" * 60)
        logger.info("SESSION CREATED")
        logger.info("=" * 60)
        logger.info(f"Requested Model : {model}")
        logger.info(f"Session ID      : {self.session._session_id if hasattr(self.session, '_session_id') else 'N/A'}")
        logger.info("=" * 60)
        
        # イベントハンドラを設定
        self._setup_event_handlers()
    
    def _setup_event_handlers(self):
        """イベントハンドラを設定"""
        def on_event(event):
            """イベント処理"""
            event_type = event.type.value
            
            # デバッグモードで全イベントをダンプ
            if logger.level == logging.DEBUG:
                logger.debug("=" * 80)
                logger.debug(f"📥 EVENT: {event_type}")
                logger.debug(f"   Raw Event: {event}")
                if hasattr(event, 'data'):
                    logger.debug(f"   Data: {event.data}")
                    # dataオブジェクトの全属性を表示
                    if hasattr(event.data, '__dict__'):
                        for key, value in event.data.__dict__.items():
                            logger.debug(f"   - {key}: {value}")
                logger.debug("=" * 80)
            
            if event_type == "assistant.message_delta":
                # ストリーミング形式（delta_content）
                delta = event.data.delta_content
                if delta:
                    self.assistant_message += delta
            
            elif event_type == "assistant.message":
                # エージェント情報を取得
                agent_name = getattr(event.data, 'agent_name', None)
                agent_display_name = getattr(event.data, 'agent_display_name', None)
                role = getattr(event.data, 'role', None)
                producer = getattr(event.data, 'producer', None)
                
                # エージェント情報があれば表示
                agent_info = ""
                if agent_display_name:
                    agent_info = f"[{agent_display_name}] "
                elif agent_name:
                    agent_info = f"[@{agent_name}] "
                elif role:
                    agent_info = f"[{role}] "
                elif producer:
                    agent_info = f"[{producer}] "
                
                # 完全なメッセージの場合は content フィールドから取得
                content = getattr(event.data, 'content', None)
                if content:
                    logger.info(f"{agent_info}{content}")
                # ストリーミングで蓄積したメッセージがあれば出力
                elif self.assistant_message:
                    logger.info(f"{agent_info}{self.assistant_message}")
                    self.assistant_message = ""
            
            elif event_type == "tool.execution_start":
                execution_id = getattr(event.data, 'tool_call_id', None)
                tool_name = getattr(event.data, 'tool_name', None)
                tool_args = getattr(event.data, 'arguments', None)
                
                self.execution_tracking[execution_id] = (tool_name, tool_args)
                
                args_preview = ""
                if tool_args:
                    args_str = str(tool_args)
                    if len(args_str) > 50:
                        args_preview = f" {args_str[:50]}..."
                    else:
                        args_preview = f" {args_str}"
                
                logger.info(f"🔧 [{execution_id}] {tool_name}{args_preview}")
            
            elif event_type == "tool.execution_complete":
                execution_id = getattr(event.data, 'tool_call_id', None)
                tool_name, tool_args = self.execution_tracking.get(execution_id, ('?', None))
                logger.info(f"✅ [{execution_id}] {tool_name}")
            
            elif event_type == "assistant.usage":
                # トークン使用状況を記録して出力
                model = getattr(event.data, 'model', None)
                input_tokens = getattr(event.data, 'input_tokens', 0) or 0
                output_tokens = getattr(event.data, 'output_tokens', 0) or 0
                cache_read_tokens = getattr(event.data, 'cache_read_tokens', 0) or 0
                cache_write_tokens = getattr(event.data, 'cache_write_tokens', 0) or 0
                cost = getattr(event.data, 'cost', 0) or 0
                duration = getattr(event.data, 'duration', 0) or 0
                initiator = getattr(event.data, 'initiator', 'unknown')
                
                # 累積
                self.total_input_tokens += input_tokens
                self.total_output_tokens += output_tokens
                self.total_cache_read_tokens += cache_read_tokens
                self.total_cache_write_tokens += cache_write_tokens
                self.total_cost += cost
                self.total_duration_ms += duration
                self.model_usage_count += 1
                
                # 最初のモデルを記録（最終サマリー用）
                if model and not self.first_model:
                    self.first_model = model
                
                # 各モデル使用の詳細をログ出力
                total_tokens = input_tokens + output_tokens
                logger.info("-" * 60)
                logger.info(f"📊 推論完了 #{self.model_usage_count} [{initiator}]")
                logger.info(f"  Model             : {model or 'N/A'}")
                logger.info(f"  Input tokens      : {input_tokens:,}")
                logger.info(f"  Output tokens     : {output_tokens:,}")
                logger.info(f"  Total tokens      : {total_tokens:,}")
                logger.info(f"  Cache read        : {cache_read_tokens:,}")
                logger.info(f"  Cache write       : {cache_write_tokens:,}")
                logger.info(f"  Duration          : {duration/1000:.2f}s")
                logger.info(f"  Cost              : {cost}")
                logger.info("-" * 60)
            
            elif event_type == "assistant.turn_start":
                # ターン開始
                turn_id = getattr(event.data, 'turn_id', None)
                logger.info(f"🔄 Turn #{turn_id} started")
            
            elif event_type == "assistant.turn_end":
                # ターン終了
                turn_id = getattr(event.data, 'turn_id', None)
                logger.info(f"✓ Turn #{turn_id} completed")
            
            elif event_type == "session.usage_info":
                # セッション状態を記録
                self.current_tokens = getattr(event.data, 'current_tokens', 0) or 0
                self.token_limit = getattr(event.data, 'token_limit', 0) or 0
                self.messages_count = int(getattr(event.data, 'messages_length', 0) or 0)
            
            elif event_type == "session.idle":
                logger.info("セッションがアイドル状態になりました")
                self.done.set()
        
        self.session.on(on_event)
    
    async def send_prompt_and_wait(self, prompt: str):
        """プロンプトを送信して完了を待機"""
        self.done.clear()
        await self.session.send({"prompt": prompt})
        await self.done.wait()
    
    async def close(self):
        """セッションとクライアントを閉じる"""
        if self.session:
            logger.debug("セッション破棄中...")
            await self.session.destroy()
            logger.debug("セッション破棄完了")
        
        if self.client:
            await self.client.stop()
