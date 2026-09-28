"""
代码复杂度分析器
"""
import ast
import re
from typing import List
from .base import BaseAnalyzer, Finding


class ComplexityAnalyzer(BaseAnalyzer):
    """代码复杂度分析器"""
    
    def __init__(self):
        super().__init__("complexity")
        
    def analyze(self, code: str, filepath: str) -> List[Finding]:
        findings = []
        
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            findings.append(Finding(
                severity="critical",
                category="syntax",
                message=f"语法错误: {e}",
                line=e.lineno or 0
            ))
            return findings
        
        # 检查函数复杂度
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                findings.extend(self._analyze_function(node))
            elif isinstance(node, ast.ClassDef):
                findings.extend(self._analyze_class(node))
        
        return findings
    
    def _analyze_function(self, func_node) -> List[Finding]:
        """分析函数复杂度"""
        findings = []
        
        # 检查函数名
        if not re.match(r'^[a-z_][a-z0-9_]*$', func_node.name):
            findings.append(Finding(
                severity="minor",
                category="naming",
                message=f"函数名 '{func_node.name}' 不符合snake_case规范",
                line=func_node.lineno,
                suggestion="使用小写字母和下划线命名"
            ))
        
        # 检查参数数量
        num_args = len(func_node.args.args)
        if num_args > 5:
            findings.append(Finding(
                severity="major",
                category="complexity",
                message=f"函数 '{func_node.name}' 参数过多 ({num_args}个)",
                line=func_node.lineno,
                suggestion="考虑使用类或数据类封装参数"
            ))
        
        # 检查嵌套层级
        max_depth = self._get_max_nesting(func_node)
        if max_depth > 4:
            findings.append(Finding(
                severity="major",
                category="complexity",
                message=f"函数 '{func_node.name}' 嵌套层级过深 ({max_depth}层)",
                line=func_node.lineno,
                suggestion="考虑提取子函数简化逻辑"
            ))
        
        # 检查函数长度
        if func_node.end_lineno and func_node.lineno:
            length = func_node.end_lineno - func_node.lineno + 1
            if length > 50:
                findings.append(Finding(
                    severity="major",
                    category="maintainability",
                    message=f"函数 '{func_node.name}' 过长 ({length}行)",
                    line=func_node.lineno,
                    suggestion="拆分为多个小函数"
                ))
        
        return findings
    
    def _analyze_class(self, class_node) -> List[Finding]:
        """分析类"""
        findings = []
        
        # 检查类名
        if not re.match(r'^[A-Z][a-zA-Z0-9]*$', class_node.name):
            findings.append(Finding(
                severity="minor",
                category="naming",
                message=f"类名 '{class_node.name}' 不符合PascalCase规范",
                line=class_node.lineno,
                suggestion="使用大写字母开头的PascalCase命名"
            ))
        
        return findings
    
    def _get_max_nesting(self, node, depth: int = 0) -> int:
        """获取最大嵌套深度"""
        max_depth = depth
        
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.With)):
                child_depth = self._get_max_nesting(child, depth + 1)
                max_depth = max(max_depth, child_depth)
            else:
                child_depth = self._get_max_nesting(child, depth)
                max_depth = max(max_depth, child_depth)
        
        return max_depth
