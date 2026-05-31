from setuptools import setup, find_packages

setup(
    name="datavistasystem",
    version="1.0.0",
    description="Multi-indicator Multi-chart Interactive Visualization Platform",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0",
        "pandas>=2.1.3",
        "numpy>=1.26.2",
        "pydantic>=2.5.0",
    ],
)
