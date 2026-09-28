"""
LLM集成
"""
import json
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class CodeReviewLLM:
    """代码审查LLM客户端"""
    
    def __init__(self, api_key: str = None, model: str = "gpt-4o"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.model = model
        
    def review_code(self, code: str, filepath: str, findings) -> dict:
        """使用LLM进行代码审查"""
        if not self.api_key:
            return self._mock_review(code, findings)
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            
            prompt = f"""请对以下{filepath}代码进行详细审查：

```python
{code[:2000]}
```

已发现的问题：
{self._format_findings(findings)}

请提供：
1. 总体评分（0-100）
2. 主要优点
3. 需要改进的地方
4. 具体建议
"""
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            return {"error": str(e), "score": 70}
    
    def _format_findings(self, findings) -> str:
        """格式化发现问题"""
        if not findings:
            return "无重大问题"
        
        lines = []
        for f in findings[:10]:  # 最多显示10个
            lines.append(f"- [{f.severity}] {f.message} (line {f.line})")
        return "\n".join(lines)
    
    def _mock_review(self, code: str, findings) -> dict:
        """模拟审查结果"""
        critical = sum(1 for f in findings if f.severity == "critical")
        major = sum(1 for f in findings if f.severity == "major")
        minor = sum(1 for f in findings if f.severity == "minor")
        
        base_score = 100
        base_score -= critical * 20
        base_score -= major * 10
        base_score -= minor * 5
        base_score = max(0, base_score)
        
        return {
            "score": base_score,
            "strengths": ["代码结构清晰"],
            "improvements": [
                f"修复 {critical} 个严重问题",
                f"解决 {major} 个主要问题",
                "优化代码风格"
            ],
            "suggestions": [
                "添加更多单元测试",
                "完善文档注释",
                "考虑类型注解"
            ]
        }
