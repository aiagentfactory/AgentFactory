# Runtime Factory - 运行工厂

## 📋 功能概述

运行工厂负责Agent的部署、执行和生命周期管理，提供企业级的沙箱隔离环境。

**特色**: 基于 [kubernetes-sigs/agent-sandbox](https://github.com/kubernetes-sigs/agent-sandbox) 的设计理念增强。

## 🎯 核心功能

### 1. 沙箱隔离系统
- **多级隔离**: Process / Container / VM
- **稳定身份**: 每个Sandbox有stable hostname
- **资源限制**: CPU/内存/网络配额
- **网络隔离**: 命名空间隔离，白名单控制

### 2. 模板系统
- **预定义模板**: basic-agent, code-executor, data-analyst, web-navigator
- **自定义模板**: 支持创建和注册
- **配置管理**: 统一的模板配置

### 3. 预热池
- **快速分配**: <1ms部署时间
- **自动补充**: 智能维护池大小
- **池管理**: 支持多模板池

### 4. 生命周期管理
- **Pause/Resume**: 暂停和恢复
- **Hibernation**: 深度休眠（保存状态）
- **Auto-Resume**: 自动恢复
- **Scheduled Cleanup**: 定时清理

## 📁 目录结构

```
runtime/
├── __init__.py              # 模块导出
├── README.md                # 本文档  
├── api.py                   # FastAPI路由
├── models.py                # 数据模型
├── schemas.py               # Pydantic schemas
├── services/                # 业务逻辑
│   ├── sandbox.py           # 沙箱管理
│   ├── template.py          # 模板系统
│   ├── pool.py              # 预热池
│   ├── agent_config.py      # Agent配置
│   ├── deployment.py        # 部署管理
│   └── session_engine.py    # Session引擎
├── isolation/               # 隔离引擎
├── storage/                 # 持久化存储
├── tests/                   # 单元测试
└── migrations/              # 数据库迁移
```

## 🚀 快速开始

### 使用沙箱系统

```python
from factories.runtime.services import SandboxManager, PoolManager

# 方式1: 直接创建沙箱
manager = SandboxManager()
sandbox = manager.create_sandbox(
    agent_id="my_agent",
    template_name="code-executor",
    isolation_level="container"
)

# 方式2: 从预热池获取（推荐）
pool_manager = PoolManager()
pool = pool_manager.create_pool("basic-agent", min_size=5)
sandbox = pool_manager.acquire_sandbox("basic-agent", "my_agent")
```

### 生命周期管理

```python
# 暂停
sandbox.pause()

# 恢复
sandbox.resume()

# 休眠（保存状态）
sandbox.hibernate()

# 终止
sandbox.terminate()
```

### API端点

- `POST /api/runtime/agents` - 创建Agent
- `POST /api/runtime/sandboxes` - 创建Sandbox
- `GET /api/runtime/sandboxes/{id}` - 获取Sandbox信息
- `PUT /api/runtime/sandboxes/{id}/pause` - 暂停
- `PUT /api/runtime/sandboxes/{id}/resume` - 恢复
- `DELETE /api/runtime/sandboxes/{id}` - 终止

## 🎨 模板说明

### Basic Agent
```python
{
    "isolation": "process",
    "resources": {"cpu": 1, "memory_gb": 2},
    "tools": ["python3", "pip"]
}
```

### Code Executor
```python
{
    "isolation": "container",  # 高隔离
    "resources": {"cpu": 2, "memory_gb": 4},
    "tools": ["python3", "node", "git"],
    "network": "restricted"  # 白名单模式
}
```

### Data Analyst
```python
{
    "isolation": "process",
    "resources": {"cpu": 4, "memory_gb": 8},
    "tools": ["jupyter", "pandas", "numpy"]
}
```

### Web Navigator
```python
{
    "isolation": "container",
    "resources": {"cpu": 2, "memory_gb": 4},
    "tools": ["playwright", "selenium", "chromium"]
}
```

## 📊 性能指标

- **部署速度**: <0.001s (预热池) vs 10-30s (冷启动)
- **并发能力**: 200+ Agents
- **资源节省**: 90% (通过休眠)

## 🔒 安全特性

1. **多级隔离**: Process/Container/VM三选一
2. **网络控制**: 白名单/黑名单
3. **资源限制**: CPU/内存/磁盘配额
4. **审计日志**: 完整操作记录

## 🧪 测试

```bash
pytest server/factories/runtime/tests/
```

## 📝 开发指南

1. 新增模板在`TemplateLibrary`中注册
2. 隔离实现在`isolation/`目录
3. 保持沙箱无状态设计
4. 状态保存在`storage/`

## 🔗 相关资源

- [kubernetes-sigs/agent-sandbox](https://github.com/kubernetes-sigs/agent-sandbox)
- [Runtime优化方案](../../.gemini/antigravity/brain/.../runtime_optimization_plan.md)
- [Demo演示](../../Demo/runtime_sandbox_demo.py)
