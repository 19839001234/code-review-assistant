"""
安全漏洞检测器
"""
import re
from typing import List
from .base import BaseAnalyzer, Finding


class SecurityAnalyzer(BaseAnalyzer):
    """安全漏洞分析器"""
    
    # 危险模式
    DANGEROUS_PATTERNS = {
        "sql_injection": {
            "pattern": r"(?i)(SELECT|INSERT|UPDATE|DELETE|DROP|UNION)\s+.*?(FROM|INTO|TABLE|WHERE)",
            "severity": "critical",
            "message": "可能的SQL注入漏洞"
        },
        "command_injection": {
            "pattern": r"(?i)(os\.system|subprocess\.(call|run|Popen)|exec\(|eval\()",
            "severity": "critical",
            "message": "命令注入风险"
        },
        "hardcoded_password": {
            "pattern": r"(?i)(password|passwd|secret|api_key)\s*=\s*['\"][^'\"]+['\"]",
            "severity": "major",
            "message": "硬编码密码或密钥"
        },
        "insecure_random": {
            "pattern": r"(?i)random\.(random|randint|choice)",
            "severity": "minor",
            "message": "使用不安全的随机数生成器（用于密码时应使用secrets模块）"
        },
        "pickle_deserialize": {
            "pattern": r"(?i)pickle\.(loads|load)",
            "severity": "major",
            "message": "使用pickle反序列化可能存在安全风险"
        }
    }
    
    def __init__(self):
        super().__init__("security")
        
    def analyze(self, code: str, filepath: str) -> List[Finding]:
        findings = []
        lines = code.split('\n')
        
        for pattern_name, config in self.DANGEROUS_PATTERNS.items():
            for i, line in enumerate(lines, 1):
                if re.search(config["pattern"], line):
                    findings.append(Finding(
                        severity=config["severity"],
                        category="security",
                        message=config["message"],
                        line=i,
                        suggestion=self._get_suggestion(pattern_name)
                    ))
        
        return findings
    
    def _get_suggestion(self, pattern_name: str) -> str:
        suggestions = {
            "sql_injection": "使用参数化查询或ORM代替字符串拼接",
            "command_injection": "使用subprocess.run()并传入参数列表，避免shell=True",
            "hardcoded_password": "使用环境变量或密钥管理服务",
            "insecure_random": "使用secrets模块代替random用于密码场景",
            "pickle_deserialize": "使用json或安全的数据格式"
        }
        return suggestions.get(pattern_name, "请审查此代码的安全性")
