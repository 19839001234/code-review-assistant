"""
代码气味检测器
"""
from typing import List
from .base import Finding


class CodeSmellDetector:
    """代码气味检测器"""
    
    def detect(self, code: str, filepath: str) -> List[Finding]:
        findings = []
        lines = code.split('\n')
        
        # 检测过长行
        for i, line in enumerate(lines, 1):
            if len(line) > 100:
                findings.append(Finding(
                    severity="minor",
                    category="style",
                    message=f"行过长 ({len(line)}字符)，建议控制在100字符以内",
                    line=i
                ))
        
        # 检测TODO/FIXME注释
        for i, line in enumerate(lines, 1):
            if "TODO" in line.upper() or "FIXME" in line.upper():
                findings.append(Finding(
                    severity="info",
                    category="documentation",
                    message="发现TODO/FIXME注释",
                    line=i
                ))
        
        # 检测空函数/类
        in_function = False
        function_lines = []
        
        for i, line in enumerate(lines, 1):
            if line.strip().startswith("def ") or line.strip().startswith("class "):
                if in_function and len(function_lines) <= 2:
                    findings.append(Finding(
                        severity="minor",
                        category="quality",
                        message="空函数或类定义"
                    ))
                in_function = True
                function_lines = [line]
            elif in_function:
                function_lines.append(line)
        
        return findings
