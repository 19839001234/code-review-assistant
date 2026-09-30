"""
多语言代码审查支持 - 新增TypeScript/Java/Go支持
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
import re


@dataclass
class LanguageConfig:
    """语言配置"""
    name: str
    extensions: List[str]
    keywords: Dict[str, str]
    complexity_metrics: List[str]
    security_rules: List[str]


# 预置语言配置
LANGUAGE_CONFIGS: Dict[str, LanguageConfig] = {
    "python": LanguageConfig(
        name="Python",
        extensions=[".py"],
        keywords={
            "function": "def",
            "class": "class", 
            "import": "import",
            "try": "try",
            "except": "except"
        },
        complexity_metrics=["cyclomatic", "cognitive", "maintainability"],
        security_rules=["SQL注入", "硬编码密钥", "不安全的反序列化"]
    ),
    "typescript": LanguageConfig(
        name="TypeScript",
        extensions=[".ts", ".tsx"],
        keywords={
            "function": "function",
            "class": "class",
            "interface": "interface",
            "import": "import",
            "async": "async"
        },
        complexity_metrics=["cyclomatic", "type_complexity"],
        security_rules=["XSS", "类型转换漏洞", "不安全的fetch"]
    ),
    "java": LanguageConfig(
        name="Java",
        extensions=[".java"],
        keywords={
            "function": "public/private/protected",
            "class": "class",
            "interface": "interface",
            "import": "import",
            "try": "try"
        },
        complexity_metrics=["cyclomatic", "nesting_depth"],
        security_rules=["SQL注入", "路径遍历", "反序列化漏洞"]
    ),
    "go": LanguageConfig(
        name="Go",
        extensions=[".go"],
        keywords={
            "function": "func",
            "struct": "struct",
            "interface": "interface",
            "import": "import",
            "go": "go"
        },
        complexity_metrics=["cyclomatic", "fan_in_fan_out"],
        security_rules=["goroutine泄漏", "竞态条件", "不安全转换"]
    )
}


def get_language_config(filepath: str) -> Optional[LanguageConfig]:
    """根据文件路径获取语言配置"""
    ext = Path(filepath).suffix.lower()
    
    for config in LANGUAGE_CONFIGS.values():
        if ext in config.extensions:
            return config
    
    return None


def detect_language(filepath: str) -> str:
    """检测文件语言"""
    config = get_language_config(filepath)
    return config.name if config else "unknown"


from pathlib import Path
