"""AI Code Review Assistant - 主入口"""
import os
import sys
import argparse
from pathlib import Path
from typing import List

from config import config
from src.analyzer.complexity import ComplexityAnalyzer
from src.analyzer.security import SecurityAnalyzer
from src.detector.bug_patterns import BugDetector
from src.detector.code_smells import CodeSmellDetector
from src.llm.reviewer import CodeReviewLLM
from src.report.generator import ReportGenerator


class CodeReviewAssistant:
    """代码审查助手"""
    
    def __init__(self):
        self.analyzers = [
            ComplexityAnalyzer(),
            SecurityAnalyzer()
        ]
        self.detectors = [
            BugDetector(),
            CodeSmellDetector()
        ]
        self.llm = CodeReviewLLM(
            api_key=config.openai_api_key,
            model=config.openai_model
        )
        self.report_gen = ReportGenerator(format=config.report_format)
    
    def analyze_file(self, filepath: str) -> dict:
        """分析单个文件"""
        # 读取文件
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                code = f.read()
        except UnicodeDecodeError:
            return {"error": f"无法读取文件（编码问题）: {filepath}"}
        except Exception as e:
            return {"error": str(e)}
        
        if len(code.split('\n')) > config.max_file_size:
            return {"error": f"文件过大: {filepath}"}
        
        # 执行分析
        all_findings = []
        
        for analyzer in self.analyzers:
            findings = analyzer.analyze(code, filepath)
            all_findings.extend(findings)
        
        for detector in self.detectors:
            findings = detector.detect(code, filepath)
            all_findings.extend(findings)
        
        # LLM审查
        llm_result = self.llm.review_code(code, filepath, all_findings)
        
        # 生成报告
        report = self.report_gen.generate(filepath, code, all_findings, llm_result)
        
        return {
            "file": filepath,
            "findings": all_findings,
            "score": llm_result.get("score", 0),
            "report": report
        }
    
    def analyze_directory(self, dirpath: str) -> List[dict]:
        """分析整个目录"""
        results = []
        dir_path = Path(dirpath)
        
        for file_path in dir_path.rglob("*.py"):
            # 跳过忽略的文件
            skip = False
            for pattern in config.ignore_patterns:
                if pattern in str(file_path):
                    skip = True
                    break
            if skip:
                continue
            
            print(f"正在分析: {file_path}")
            result = self.analyze_file(str(file_path))
            results.append(result)
        
        return results
    
    def get_summary(self, results: List[dict]) -> dict:
        """获取审查摘要"""
        total_files = len(results)
        total_issues = sum(len(r.get("findings", [])) for r in results)
        critical_issues = sum(
            sum(1 for f in r.get("findings", []) if f.severity == "critical")
            for r in results
        )
        avg_score = sum(r.get("score", 0) for r in results) / total_files if total_files > 0 else 0
        
        return {
            "total_files": total_files,
            "total_issues": total_issues,
            "critical_issues": critical_issues,
            "average_score": round(avg_score, 2)
        }


def main():
    parser = argparse.ArgumentParser(description="AI Code Review Assistant")
    parser.add_argument("path", help="要审查的文件或目录路径")
    parser.add_argument("--format", choices=["markdown", "json", "html"], default=None)
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument("--summary", action="store_true", help="只显示摘要")
    
    args = parser.parse_args()
    
    # 设置报告格式
    if args.format:
        config.report_format = args.format
    
    assistant = CodeReviewAssistant()
    
    path = Path(args.path)
    if path.is_dir():
        results = assistant.analyze_directory(str(path))
        summary = assistant.get_summary(results)
        
        print("\n" + "="*50)
        print("代码审查摘要")
        print("="*50)
        print(f"分析文件数: {summary['total_files']}")
        print(f"发现问题数: {summary['total_issues']}")
        print(f"严重问题数: {summary['critical_issues']}")
        print(f"平均评分: {summary['average_score']}/100")
        
        if not args.summary and not args.output:
            for result in results:
                print(f"\n{'='*50}")
                print(f"文件: {result['file']}")
                print(f"评分: {result['score']}/100")
                print("-"*50)
                print(result['report'])
    elif path.is_file():
        result = assistant.analyze_file(str(path))
        
        if "error" in result:
            print(f"错误: {result['error']}")
            sys.exit(1)
        
        print("\n" + "="*50)
        print(f"代码审查报告: {result['file']}")
        print("="*50)
        print(result['report'])
    else:
        print(f"错误: 路径不存在 {args.path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
