# AI Code Review Assistant - AI代码审查助手

## 项目概述

AI Code Review Assistant是一个基于大语言模型的自动化代码审查工具，能够分析代码质量、识别潜在问题、提供优化建议，并生成详细的审查报告。

## 技术栈

- **Python 3.10+**
- **LLM API** - OpenAI/Claude/Ollama
- **AST** - Python抽象语法树解析
- **Regex** - 模式匹配和代码分析
- **Jinja2** - 报告模板引擎

## 核心功能

### 1. 代码质量分析
- 代码复杂度检测
- 重复代码识别
- 命名规范检查
- 注释覆盖率分析

### 2. 问题检测
- Bug模式识别
- 安全漏洞检测
- 性能瓶颈分析
- 最佳实践违反

### 3. 优化建议
- 重构建议
- 代码风格改进
- 性能优化方案
- 可读性提升

### 4. 报告生成
- Markdown格式报告
- 可视化评分
- 问题分类统计
- 改进优先级排序

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑.env，填入API密钥

# 使用命令行
python main.py analyze path/to/code.py
python main.py review path/to/project/

# 使用API
python main.py --api --port 8000
```

## 项目结构

```
code-review-assistant/
├── README.md
├── requirements.txt
├── .env.example
├── main.py                 # 主入口
├── config.py              # 配置管理
├── src/
│   ├── analyzer/          # 分析器模块
│   │   ├── base.py        # 分析器基类
│   │   ├── complexity.py  # 复杂度分析
│   │   ├── security.py    # 安全分析
│   │   └── style.py       # 风格分析
│   ├── detector/          # 问题检测器
│   │   ├── bug_patterns.py
│   │   └── code_smells.py
│   ├── llm/               # LLM集成
│   │   ├── base.py
│   │   └── openai.py
│   └── report/            # 报告生成
│       ├── base.py
│       └── markdown.py
└── templates/             # 报告模板
```

## 审查维度

### 代码质量指标

| 指标 | 权重 | 说明 |
|------|------|------|
| 可读性 | 25% | 代码清晰度和理解难度 |
| 可维护性 | 25% | 修改和扩展的难易程度 |
| 安全性 | 20% | 潜在安全漏洞和风险 |
| 性能 | 15% | 运行效率和资源使用 |
| 规范性 | 15% | 代码风格和最佳实践 |

### 问题类型

- **Critical** - 严重问题（bug、安全漏洞）
- **Major** - 主要问题（性能、可维护性）
- **Minor** - 次要问题（代码风格、可读性）
- **Info** - 提示信息（最佳实践建议）

## 应用场景

1. **代码审查** - 自动化PR审查
2. **代码质量门禁** - CI/CD集成
3. **学习辅助** - 编程学习反馈
4. **团队协作** - 统一代码标准

## 作者

张智博
新疆大学智能科学与技术学院

## 许可证

MIT License
