"""
Bug模式检测器
"""
import re
from typing import List
from .base import Finding


class BugDetector:
    """Bug模式检测器"""
    
    BUG_PATTERNS = [
        {
            "name": "unreachable_code",
            "pattern": r"(?:return|raise|break|continue)\s*\n\s*\S",
            "severity": "major",
            "message": "存在不可达代码"
        },
        {
            "name": "mutable_default_arg",
            "pattern": r"def\s+\w+\([^)]*\w+\s*=\s*(\[\]|\{\}|set\(\)))",
            "severity": "major",
            "message": "使用可变对象作为默认参数"
        },
        {
            "name": "bare_except",
            "pattern": r"except\s*:",
            "severity": "major",
            "message": "使用bare except会捕获所有异常，包括KeyboardInterrupt"
        },
        {
            "name": "implicit_string_concatenation",
            "pattern": r'["\'].*?["\']\s*["\']',
            "severity": "minor",
            "message": "隐式字符串连接可能导致意外结果"
        },
        {
            "name": "unused_variable",
            "pattern": r"\b(\w+)\s*=\s*[^=].*?\n(?:.*?\n)*?\s*(?!.*?\b\1\b)",
            "severity": "minor",
            "message": "变量可能未使用"
        }
    ]
    
    def detect(self, code: str, filepath: str) -> List[Finding]:
        findings = []
        lines = code.split('\n')
        
        for pattern_info in self.BUG_PATTERNS:
            pattern = pattern_info["pattern"]
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line):
                    findings.append(Finding(
                        severity=pattern_info["severity"],
                        category="bug",
                        message=pattern_info["message"],
                        line=i
                    ))
        
        return findings
