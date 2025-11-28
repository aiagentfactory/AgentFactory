"""
RuntimeFactory - Agent Factory运行工厂模块
基于kubernetes-sigs/agent-sandbox的沙箱隔离和部署管理系统
"""

from setuptools import setup, find_packages

setup(
    name="agentfactory-runtime",
    version="1.0.0",
    description="Agent runtime, sandbox isolation, and deployment management",
    author="Agent Factory Team",
    author_email="team@agentfactory.io",
    
    packages=find_packages(),
    python_requires=">=3.8",
    
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.24.0",
        "pydantic>=2.0.0",
        "sqlalchemy>=2.0.0",
        "docker>=6.1.0",  # Container isolation
        "psutil>=5.9.0"
    ],
    
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0"
        ],
        "kubernetes": [
            "kubernetes>=28.0.0"
        ],
        "gvisor": [
            "gvisor>=0.1.0"  # VM-level isolation
        ]
    },
    
    entry_points={
        "console_scripts": [
            "runtime-factory=api.main:run"
        ]
    },
    
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ]
)
