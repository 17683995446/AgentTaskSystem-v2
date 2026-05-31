from setuptools import setup, find_packages

setup(
    name="AgentTaskSystem",
    version="2.0.0",
    description="Agent长任务执行系统 - 严格二叉树层级模块化架构",
    author="AgentTaskSystem Team",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "pandas>=2.0.0",
        "openpyxl>=3.1.0",
        "selenium>=4.15.0",
        "schedule>=1.2.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
