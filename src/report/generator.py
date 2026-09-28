"""
报告生成器
"""
import json
from typing import List, Dict
from datetime import datetime


class ReportGenerator:
    """报告生成器"""
    
    def __init__(self, format: str = "markdown"):
        self.format = format
        
    def generate(self, filepath: str, code: str, findings: List, review_result: Dict) -> str:
        """生成审查报告"""
        if self.format == "json":
            return self._generate_json(filepath, code, findings, review_result)
        elif self.format == "html":
            return self._generate_html(filepath, code, findings, review_result)
        else:
            return self._generate_markdown(filepath, code, findings, review_result)
    
    def _generate_markdown(self, filepath: str, code: str, findings: List, result: Dict) -> str:
        """生成Markdown报告"""
        lines = []
        lines.append(f"# 代码审查报告: {filepath}")
        lines.append(f"\n生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 评分
        score = result.get("score", 0)
        lines.append(f"\n## 📊 总体评分: **{score}/100**")
        
        # 问题统计
        lines.append("\n## 🔍 发现的问题")
        severity_counts = {}
        for f in findings:
            severity_counts[f.severity] = severity_counts.get(f.severity, 0) + 1
        
        for severity, count in severity_counts.items():
            icon = {"critical": "🔴", "major": "🟠", "minor": "🟡", "info": "⚪"}.get(severity, "⚪")
            lines.append(f"- {icon} {severity}: {count}个")
        
        # 详细问题
        if findings:
            lines.append("\n### 详细列表\n")
            for f in findings:
                lines.append(f"**[{f.severity.upper()}] L{f.line}**: {f.message}")
                if f.suggestion:
                    lines.append(f"   💡 建议: {f.suggestion}")
        
        # LLM建议
        if "strengths" in result:
            lines.append("\n## ✅ 优点")
            for s in result["strengths"]:
                lines.append(f"- {s}")
        
        if "improvements" in result:
            lines.append("\n## 📝 改进建议")
            for i in result["improvements"]:
                lines.append(f"- {i}")
        
        return "\n".join(lines)
    
    def _generate_json(self, filepath: str, code: str, findings: List, result: Dict) -> str:
        """生成JSON报告"""
        report = {
            "file": filepath,
            "timestamp": datetime.now().isoformat(),
            "score": result.get("score", 0),
            "findings_count": len(findings),
            "findings": [
                {
                    "severity": f.severity,
                    "category": f.category,
                    "message": f.message,
                    "line": f.line,
                    "suggestion": f.suggestion
                }
                for f in findings
            ],
            "llm_review": result
        }
        return json.dumps(report, indent=2, ensure_ascii=False)
    
    def _generate_html(self, filepath: str, code: str, findings: List, result: Dict) -> str:
        """生成HTML报告"""
        score = result.get("score", 0)
        color = "green" if score >= 80 else "orange" if score >= 60 else "red"
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Code Review: {filepath}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .score {{ font-size: 48px; color: {color}; }}
        .finding {{ padding: 10px; margin: 10px 0; border-left: 4px solid; }}
        .critical {{ border-color: red; background: #ffebee; }}
        .major {{ border-color: orange; background: #fff3e0; }}
        .minor {{ border-color: yellow; background: #fffde7; }}
        .info {{ border-color: blue; background: #e3f2fd; }}
    </style>
</head>
<body>
    <h1>代码审查报告: {filepath}</h1>
    <div class="score">{score}/100</div>
    <h2>发现问题 ({len(findings)})</h2>
"""
        for f in findings:
            html += f'<div class="finding {f.severity}"><strong>[{f.severity.upper()}]</strong> L{f.line}: {f.message}</div>'
        
        html += "</body></html>"
        return html
