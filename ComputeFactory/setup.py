"""
ComputeFactory - Agent Factory计算资源管理模块
提供GPU/CPU/TPU资源调度、作业队列管理和资源监控功能
"""

from setuptools import setup, find_packages

setup(
    name="agentfactory-compute",
    version="1.0.0",
    description="Compute resource management and scheduling for Agent Factory",
    author="Agent Factory Team",
    author_email="team@agentfactory.io",
    
    packages=find_packages(),
    python_requires=">=3.8",
    
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.24.0",
        "pydantic>=2.0.0",
        "sqlalchemy>=2.0.0",
        "prometheus-client>=0.18.0",
        "psutil>=5.9.0"
    ],
    
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0"
        ]
    },
    
    entry_points={
        "console_scripts": [
            "compute-factory=api.main:run"
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
