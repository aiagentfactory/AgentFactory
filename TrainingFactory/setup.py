"""
TrainingFactory - Agent训练工厂模块
基于RL-Factory的优秀经验，提供高效的AI Agent训练能力
"""

from setuptools import setup, find_packages

setup(
    name="agentfactory-training",
    version="1.0.0",
    description="AI Agent training with SFT, RL (PPO/DPO/GRPO), and Reward Modeling",
    author="Agent Factory Team",
    author_email="team@agentfactory.io",
    
    packages=find_packages(),
    python_requires=">=3.10",
    
    install_requires=[
        "torch>=2.0.0",
        "transformers>=4.35.0",
        "accelerate>=0.24.0",
        "datasets>=2.14.0",
        "peft>=0.6.0",
        "httpx>=0.25.0",
        "aiohttp>=3.9.0",
        "redis>=5.0.0"
    ],
    
    extras_require={
        "rl": [
            "verl>=0.5.0",  # RL framework (inspired by RL-Factory)
            "bitsandbytes>=0.41.0"
        ],
        "mcp": [
            "mcp-python>=0.1.0"  # Model Context Protocol
        ],
        "monitoring": [
            "tensorboard>=2.14.0",
            "wandb>=0.15.0"
        ],
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0"
        ],
        "all": [
            "verl>=0.5.0",
            "mcp-python>=0.1.0",
            "tensorboard>=2.14.0",
            "wandb>=0.15.0",
            "pytest>=7.4.0"
        ]
    },
    
    entry_points={
        "console_scripts": [
            "training-factory=api.main:run",
            "train-grpo=scripts.train_grpo:main",  # GRPO快捷命令
            "train-sft=scripts.train_sft:main"     # SFT快捷命令
        ]
    },
    
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    
    project_urls={
        "Bug Reports": "https://github.com/your-org/AgentFactory/issues",
        "Source": "https://github.com/your-org/AgentFactory",
        "RL-Factory": "https://github.com/Simple-Efficient/RL-Factory"
    }
)
