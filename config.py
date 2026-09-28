"""配置管理"""
import os
from dataclasses import dataclass
from typing import List
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    """配置类"""
    
    # API配置
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o")
    
    # 审查设置
    max_file_size: int = int(os.getenv("MAX_FILE_SIZE", "100000"))
    ignore_patterns: List[str] = None
    
    def __post_init__(self):
        if self.ignore_patterns is None:
            patterns_str = os.getenv("IGNORE_PATTERNS", "__pycache__,*.pyc,node_modules")
            self.ignore_patterns = [p.strip() for p in patterns_str.split(",")]
    
    @property
    def strict_mode(self) -> bool:
        return os.getenv("STRICT_MODE", "false").lower() == "true"
    
    @property
    def report_format(self) -> str:
        return os.getenv("REPORT_FORMAT", "markdown").lower()


# 全局配置实例
config = Config()
