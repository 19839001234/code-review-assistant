"""
分析器基类
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class Finding:
    """审查发现"""
    severity: str  # critical, major, minor, info
    category: str
    message: str
    line: int = 0
    suggestion: str = ""


class BaseAnalyzer(ABC):
    """分析器基类"""
    
    def __init__(self, name: str):
        self.name = name
        
    @abstractmethod
    def analyze(self, code: str, filepath: str) -> List[Finding]:
        """分析代码"""
        pass
    
    def get_score(self, findings: List[Finding]) -> float:
        """计算质量分数 (0-100)"""
        if not findings:
            return 100.0
        
        penalties = {
            "critical": 20,
            "major": 10,
            "minor": 5,
            "info": 1
        }
        
        total_penalty = sum(
            penalties.get(f.severity, 0) for f in findings
        )
        
        return max(0, 100 - total_penalty)
