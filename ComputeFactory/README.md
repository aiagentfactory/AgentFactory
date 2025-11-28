# Compute Factory - 计算工厂

## 📋 功能概述

计算工厂负责统一管理和调度计算资源（GPU、CPU、TPU等），为其他工厂提供算力支持。

## 🎯 核心功能

### 1. 资源管理
- GPU/CPU/NPU/TPU资源抽象
- 资源池管理（Training/Inference/Environment池）
- 资源分配与释放

### 2. 作业调度
- 优先级调度（HIGH/MEDIUM/LOW）
- FIFO队列管理
- 可抢占作业支持
- 作业状态跟踪

### 3. 监控计费
- 实时资源使用监控
- 成本计算与报告
- 资源使用统计

## 📁 目录结构

```
compute/
├── __init__.py              # 模块导出
├── README.md                # 本文档
├── api.py                   # FastAPI路由
├── models.py                # 数据模型
├── schemas.py               # Pydantic schemas
├── services/                # 业务逻辑
│   ├── resource_manager.py  # 资源管理器
│   ├── scheduler.py         # 作业调度器
│   └── monitor.py           # 资源监控器
├── tests/                   # 单元测试
└── migrations/              # 数据库迁移
```

## 🚀 快速开始

### 使用API

```python
from factories.compute.services import ResourceManager, JobScheduler

# 分配资源
manager = ResourceManager()
allocation = manager.allocate_resource(
    pool_type="training",
    resource_spec=ResourceSpec(
        resource_type="gpu",
        count=2,
        memory_gb=80
    )
)

# 提交作业
scheduler = JobScheduler()
job = scheduler.submit_job(
    name="train_model_v1",
    priority="high"
)
```

### API端点

- `POST /api/compute/allocate` - 分配资源
- `POST /api/compute/release` - 释放资源
- `GET /api/compute/pools` - 获取资源池状态
- `POST /api/compute/jobs` - 提交作业
- `GET /api/compute/usage` - 获取使用统计

## 🔧 配置

资源池配置示例:
```python
RESOURCE_POOLS = {
    "training": {
        "gpu": 8,
        "cpu": 32,
        "memory_gb": 256
    },
    "inference": {
        "gpu": 4,
        "cpu": 16,
        "memory_gb": 128
    }
}
```

## 📊 数据模型

### ResourceSpec
- `resource_type`: GPU/CPU/TPU等
- `count`: 资源数量
- `memory_gb`: 内存大小

### Job
- `job_id`: 作业ID
- `name`: 作业名称
- `priority`: 优先级
- `status`: 状态

## 🧪 测试

```bash
pytest server/factories/compute/tests/
```

## 📝 开发指南

1. 新增功能在`services/`中实现
2. 保持单一职责原则
3. 添加单元测试
4. 更新API文档
