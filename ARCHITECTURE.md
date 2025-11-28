# Agent Factory - 独立模块化架构

## 🎯 架构理念

每个Factory都是**完全独立的项目模块**，可以独立开发、测试、部署和扩展。

---

## 📁 新的项目结构

```
AgentFactory/
├── server/                    # 后端服务
│   └── factories/
│       ├── ComputeFactory/    ✅ 计算工厂（独立项目）
│       ├── DataFactory/       ✅ 数据工厂（独立项目）
│       ├── EnvironmentFactory/✅ 环境工厂（独立项目）
│       ├── TrainingFactory/   ✅ 训练工厂（独立项目）
│       ├── EvaluationFactory/ ✅ 评估工厂（独立项目）
│       └── RuntimeFactory/    ✅ 运行工厂（独立项目）
│
└── client/                    # 前端服务
    └── src/
        └── factories/
            ├── ComputeFactory/    ✅ 计算工厂前端
            ├── DataFactory/       ✅ 数据工厂前端
            ├── EnvironmentFactory/✅ 环境工厂前端
            ├── TrainingFactory/   ✅ 训练工厂前端
            ├── EvaluationFactory/ ✅ 评估工厂前端
            └── RuntimeFactory/    ✅ 运行工厂前端
```

---

## 📦 每个Factory的独立项目结构

### 后端Factory项目结构

```
{FactoryName}/                 # 如 ComputeFactory/
├── README.md                  # 工厂说明文档
├── requirements.txt           # Python依赖（独立）
├── setup.py                   # 包配置（可独立安装）
├── __init__.py                # 模块导出
│
├── api/                       # API层
│   ├── __init__.py
│   ├── routes.py              # 路由定义
│   └── dependencies.py        # 依赖注入
│
├── services/                  # 业务逻辑层
│   ├── __init__.py
│   └── *.py                   # 各种服务
│
├── models/                    # 数据模型
│   ├── __init__.py
│   ├── database.py            # 数据库模型
│   └── schemas.py             # Pydantic schemas
│
├── core/                      # 核心配置
│   ├── __init__.py
│   ├── config.py              # 配置管理
│   └── exceptions.py          # 异常定义
│
├── utils/                     # 工具函数
│   └── __init__.py
│
├── tests/                     # 测试套件
│   ├── __init__.py
│   ├── test_services.py
│   └── test_api.py
│
├── migrations/                # 数据库迁移
│   └── versions/
│
└── docs/                      # 文档
    ├── API.md
    └── ARCHITECTURE.md
```

### 前端Factory项目结构

```
{FactoryName}/                 # 如 ComputeFactory/
├── README.md                  # 工厂前端说明
├── package.json               # NPM依赖（可选，独立）
│
├── pages/                     # 页面组件
│   ├── index.jsx              # 主页面
│   └── *.jsx                  # 其他页面
│
├── components/                # UI组件
│   ├── index.js               # 组件导出
│   └── *.jsx                  # 各种组件
│
├── api/                       # API客户端
│   ├── index.js
│   └── client.js              # HTTP客户端
│
├── hooks/                     # React Hooks
│   └── use*.js
│
├── utils/                     # 工具函数
│   └── helpers.js
│
├── styles/                    # 样式文件
│   ├── index.css
│   └── *.css
│
├── constants/                 # 常量定义
│   └── index.js
│
└── tests/                     # 前端测试
    └── *.test.jsx
```

---

## 🔧 独立Factory示例

### 1. ComputeFactory (计算工厂)

**功能**: GPU/CPU资源调度与管理

**后端**:
```
ComputeFactory/
├── README.md
├── requirements.txt           # fastapi, sqlalchemy, prometheus-client
├── setup.py
├── api/
│   └── routes.py              # /compute/* 路由
├── services/
│   ├── resource_manager.py
│   ├── scheduler.py
│   └── monitor.py
└── models/
    └── schemas.py             # ResourceSpec, Job, etc.
```

**前端**:
```
ComputeFactory/
├── pages/
│   └── ComputeFactoryDashboard.jsx
├── components/
│   ├── ResourcePool.jsx
│   ├── JobQueue.jsx
│   └── UsageChart.jsx
└── api/
    └── computeClient.js
```

---

### 2. DataFactory (数据工厂)

**功能**: 数据采集、清洗、标注、版本管理

**后端**:
```
DataFactory/
├── requirements.txt           # pandas, sqlalchemy
├── services/
│   ├── collector.py
│   ├── cleaner.py
│   ├── annotator.py
│   └── dataset_manager.py
└── models/
    └── schemas.py             # Event, Dataset, Annotation
```

**前端**:
```
DataFactory/
├── components/
│   ├── DataCollector.jsx
│   ├── AnnotationTool.jsx
│   └── DatasetExplorer.jsx
└── api/
    └── dataClient.js
```

---

### 3. RuntimeFactory (运行工厂)

**功能**: Agent部署、沙箱隔离、生命周期管理

**特色**: 基于kubernetes-sigs/agent-sandbox

**后端**:
```
RuntimeFactory/
├── requirements.txt           # docker, kubernetes
├── services/
│   ├── sandbox.py
│   ├── template.py
│   ├── pool.py
│   └── deployment.py
├── isolation/                 # 隔离引擎
└── storage/                   # 持久化
```

**前端**:
```
RuntimeFactory/
├── components/
│   ├── SandboxManager.jsx
│   ├── TemplateSelector.jsx
│   └── DeploymentPanel.jsx
└── api/
    └── runtimeClient.js
```

---

## � 独立部署支持

### 作为Python包安装

每个Factory可独立安装：

```bash
# 安装单个Factory
cd server/factories/ComputeFactory
pip install -e .

# 或安装所有Factories
cd server
pip install -e ./factories/ComputeFactory
pip install -e ./factories/DataFactory
# ...
```

### 独立运行

每个Factory可独立运行（微服务模式）：

```bash
# 运行ComputeFactory
cd server/factories/ComputeFactory
uvicorn api.routes:app --port 8001

# 运行DataFactory
cd server/factories/DataFactory
uvicorn api.routes:app --port 8002
```

### Docker部署

每个Factory有独立的Dockerfile：

```dockerfile
# ComputeFactory/Dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "api.routes:app", "--host", "0.0.0.0"]
```

---

## 📋 Factory命名规范

| 中文名 | 英文名 | 目录名 | API前缀 |
|--------|--------|--------|---------|
| 计算工厂 | Compute Factory | `ComputeFactory` | `/compute` |
| 数据工厂 | Data Factory | `DataFactory` | `/data` |
| 环境工厂 | Environment Factory | `EnvironmentFactory` | `/env` |
| 训练工厂 | Training Factory | `TrainingFactory` | `/train` |
| 评估工厂 | Evaluation Factory | `EvaluationFactory` | `/eval` |
| 运行工厂 | Runtime Factory | `RuntimeFactory` | `/runtime` |

---

## � Factory间通信

虽然每个Factory是独立的，但它们需要协作。通信方式：

### 1. REST API调用
```python
# TrainingFactory调用ComputeFactory
import requests

response = requests.post(
    "http://compute-factory:8001/compute/allocate",
    json={"resource_type": "gpu", "count": 2}
)
```

### 2. 消息队列（推荐）
```python
# 使用RabbitMQ/Kafka
from kombu import Connection, Exchange, Queue

# 发布事件
training_complete = {
    "model_id": "model_v1",
    "status": "completed"
}
publish_event("training.completed", training_complete)
```

### 3. gRPC（高性能）
```protobuf
service ComputeService {
  rpc AllocateResource(ResourceRequest) returns (Allocation);
}
```

---

## 🛠️ 开发工作流

### 开发新功能

1. **选择Factory**: 确定功能属于哪个Factory
2. **进入目录**: `cd server/factories/ComputeFactory`
3. **创建分支**: `git checkout -b feature/new-scheduler`
4. **开发**: 只修改该Factory的代码
5. **测试**: `pytest tests/`
6. **提交**: 代码改动限定在该Factory

### 添加新Factory

```bash
# 创建新Factory
mkdir -p server/factories/NewFactory/{api,services,models,tests}
mkdir -p client/src/factories/NewFactory/{pages,components,api}

# 复制模板
cp server/factories/ComputeFactory/setup.py server/factories/NewFactory/
# 修改配置...
```

---

## 📦 Package.json / Setup.py 示例

### setup.py (后端)
```python
from setuptools import setup, find_packages

setup(
    name="agentfactory-compute",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.104.0",
        "sqlalchemy>=2.0.0",
        "prometheus-client>=0.18.0"
    ],
    entry_points={
        "console_scripts": [
            "compute-factory=api.routes:main"
        ]
    }
)
```

### package.json (前端 - 可选)
```json
{
  "name": "@agentfactory/compute-ui",
  "version": "1.0.0",
  "main": "index.js",
  "dependencies": {
    "react": "^19.0.0",
    "recharts": "^2.10.0"
  }
}
```

---

## ✨ 架构优势

### 1. 完全独立
- ✅ 每个Factory是独立的Python包
- ✅ 独立的依赖管理
- ✅ 独立的版本控制

### 2. 易于扩展
- ✅ 添加新Factory无需修改其他Factory
- ✅ Factory内部结构统一
- ✅ 清晰的接口定义

### 3. 灵活部署
- ✅ 单体部署：所有Factory在一个进程
- ✅ 微服务部署：每个Factory独立服务
- ✅ 混合部署：核心Factory独立，其他共享

### 4. 团队协作
- ✅ 不同团队负责不同Factory
- ✅ 代码冲突最小化
- ✅ 独立的发版节奏

---

## 📝 迁移检查清单

- [x] 重命名后端目录为FactoryName格式
- [x] 重命名前端目录为FactoryName格式
- [ ] 为每个Factory创建setup.py
- [ ] 为每个Factory创建requirements.txt
- [ ] 更新所有import路径
- [ ] 创建Factory间通信层
- [ ] 添加独立测试套件
- [ ] 更新部署脚本
- [ ] 创建Docker配置

---

**每个Factory现在都是一个完整的、独立的项目模块！** �
