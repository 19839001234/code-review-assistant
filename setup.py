from setuptools import setup, find_packages

setup(
    name="code-review-assistant",
    version="2.0.0",
    packages=find_packages(),
    install_requires=[
        "openai>=1.6.0",
        "pyyaml>=6.0.1",
        "click>=8.1.0",
        "jinja2>=3.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
        ],
        "github": ["pygithub>=2.0.0"],
    },
    python_requires=">=3.9",
    author="张智博",
    author_email="1132228548@qq.com",
    description="AI Code Review Assistant - 支持多语言的代码审查工具",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/19839001234/code-review-assistant",
    license="MIT",
    entry_points={
        "console_scripts": [
            "code-review=main:main",
        ],
    },
)
