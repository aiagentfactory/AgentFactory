"""
ObservabilityFactory - 可观测性工厂
提供LLM Agent的分布式追踪、性能监控和成本管理
"""

from setuptools import setup, find_packages

setup(
    name="agentfactory-observability",
    version="1.0.0",
    description="Observability, monitoring and tracing for AI Agents",
    author="Agent Factory Team",
    author_email="team@agentfactory.io",
    
    packages=find_packages(),
    python_requires=">=3.8",
    
    install_requires=[
        # Tracing
        "opentelemetry-api>=1.21.0",
        "opentelemetry-sdk>=1.21.0",
        "opentelemetry-exporter-otlp>=1.21.0",
        
        # Metrics
        "prometheus-client>=0.19.0",
        
        # Logging
        "structlog>=23.2.0",
        
        # Cost tracking
        "tiktoken>=0.5.0",  # Token counting
        
        # Utils
        "pydantic>=2.0.0"
    ],
    
    extras_require={
        "langfuse": [
            "langfuse>=2.0.0"
        ],
        "grafana": [
            "grafana-api>=1.0.0"
        ],
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0"
        ],
        "all": [
            "langfuse>=2.0.0",
            "grafana-api>=1.0.0",
            "pytest>=7.4.0"
        ]
    },
    
    entry_points={
        "console_scripts": [
            "observability-server=services.server:main"
        ]
    },
    
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: System :: Monitoring",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ]
)
