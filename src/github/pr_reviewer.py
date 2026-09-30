"""
GitHub PR集成模块
"""
from typing import Dict, List, Optional, Any
import asyncio
import json
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ReviewComment:
    """审查评论"""
    path: str
    line: int
    body: str
    side: str = "LEFT"  # LEFT or RIGHT


@dataclass
class GitHubPR:
    """GitHub PR信息"""
    owner: str
    repo: str
    pr_number: int
    title: str
    body: str
    base_branch: str
    head_branch: str
    files: List[Dict] = field(default_factory=list)
    comments: List[ReviewComment] = field(default_factory=list)


class GitHubPRReviewer:
    """
    GitHub PR自动审查器
    
    功能:
    - 自动获取PR diff
    - 分析代码变更
    - 生成审查评论
    - 提交到GitHub
    """
    
    def __init__(self, token: str, owner: str, repo: str):
        self.token = token
        self.owner = owner
        self.repo = repo
        self.api_base = f"https://api.github.com/repos/{owner}/{repo}"
    
    async def get_pr(self, pr_number: int) -> GitHubPR:
        """获取PR信息"""
        # 实际项目使用PyGithub库
        import requests
        headers = {"Authorization": f"token {self.token}"}
        
        pr_response = requests.get(f"{self.api_base}/pulls/{pr_number}", headers=headers)
        pr_data = pr_response.json()
        
        files_response = requests.get(f"{self.api_base}/pulls/{pr_number}/files", headers=headers)
        files = files_response.json()
        
        return GitHubPR(
            owner=self.owner,
            repo=self.repo,
            pr_number=pr_number,
            title=pr_data.get("title", ""),
            body=pr_data.get("body", ""),
            base_branch=pr_data.get("base", {}).get("ref", ""),
            head_branch=pr_data.get("head", {}).get("ref", ""),
            files=files
        )
    
    async def review_pr(self, pr: GitHubPR) -> List[ReviewComment]:
        """审查PR"""
        comments = []
        
        for file_info in pr.files:
            filename = file_info.get("filename", "")
            patch = file_info.get("patch", "")
            
            # 逐行分析
            lines = patch.split("\n")
            current_line = 0
            
            for line in lines:
                if line.startswith("+") and not line.startswith("+++"):
                    current_line += 1
                    # 在这里添加审查逻辑
                    # 例如：检查安全模式、代码风格等
                    
        return comments
    
    async def post_comments(self, pr: GitHubPR, comments: List[ReviewComment]):
        """提交评论到GitHub"""
        import requests
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # GitHub API要求body是数组形式
        comment_body = "\n".join([c.body for c in comments])
        
        response = requests.post(
            f"{self.api_base}/issues/{pr.pr_number}/comments",
            headers=headers,
            json={"body": comment_body}
        )
        
        return response.status_code == 201
    
    async def create_review(self, pr: GitHubPR, comments: List[ReviewComment], event: str = "COMMENT"):
        """创建PR审查（更正式的方式）"""
        import requests
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # 组织评论
        comments_by_file = {}
        for comment in comments:
            if comment.path not in comments_by_file:
                comments_by_file[comment.path] = []
            comments_by_file[comment.path].append({
                "path": comment.path,
                "position": comment.line,
                "body": comment.body
            })
        
        # GitHub PR review API
        payload = {
            "body": f"🤖 AI Code Review\n\n自动审查结果",
            "event": event,
            "comments": []
        }
        
        for path, file_comments in comments_by_file.items():
            payload["comments"].extend(file_comments)
        
        response = requests.post(
            f"{self.api_base}/pulls/{pr.pr_number}/reviews",
            headers=headers,
            json=payload
        )
        
        return response.status_code == 200


# 工厂函数
def create_github_reviewer(token: str, owner: str, repo: str) -> GitHubPRReviewer:
    """创建GitHub PR审查器"""
    return GitHubPRReviewer(token, owner, repo)
