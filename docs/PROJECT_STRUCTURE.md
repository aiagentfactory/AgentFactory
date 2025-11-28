# Agent Factory - 项目结构可视化

## 🏗️ 顶级目录结构

```
AgentFactory/                          # 项目根目录
│
├── 🔧 ComputeFactory/                 # 计算工厂（独立项目）
│   ├── setup.py                       # Python包配置
│   ├── requirements.txt               # 独立依赖
│   ├── README.md                      # 工厂文档
│   ├── services/                      # 业务逻辑
│   │   ├── resource_manager.py        # 资源管理
│   │   ├── scheduler.py               # 作业调度
│   │   └── monitor.py                 # 监控计费
│   ├── tests/                         # 单元测试
│   └── migrations/                    # 数据库迁移
│
├── 🗃️ DataFactory/                    # 数据工厂（独立项目）
│   ├── setup.py
│   ├── requirements.txt
│   ├── README.md
│   ├── services/
│   │   ├── collector.py               # 数据采集
│   │   ├── cleaner.py                 # 数据清洗
│   │   ├── annotator.py               # 数据标注
│   │   └── dataset_manager.py         # 数据集管理
│   ├── tests/
│   └── migrations/
│
├── 🌍 EnvironmentFactory/             # 环境工厂（独立项目）
│   ├── setup.py
│   ├── requirements.txt
│   ├── README.md
│   ├── services/
│   │   ├── scenario_builder.py        # 场景构建
│   │   ├── executor.py                # 环境执行
│   │   └── replay.py                  # 轨迹回放
│   ├── tests/
│   └── migrations/
│
├── 🧠 TrainingFactory/                # 训练工厂（独立项目）
│   ├── setup.py
│   ├── requirements.txt
│   ├── README.md
│   ├── services/
│   │   ├── sft_trainer.py             # SFT训练
│   │   ├── rl_trainer.py              # RL训练
│   │   └── model_registry.py          # 模型注册
│   ├── tests/
│   └── migrations/
│
├── 🏆 EvaluationFactory/              # 评估工厂（独立项目）
│   ├── setup.py
│   ├── requirements.txt
│   ├── README.md
│   ├── services/
│   │   ├── taskset_manager.py         # 任务集管理
│   │   ├── evaluator.py               # 评估器
│   │   └── judge.py                   # LLM-as-judge
│   ├── tests/
│   └── migrations/
│
├── ⚡ RuntimeFactory/                 # 运行工厂（独立项目）⭐
│   ├── setup.py
│   ├── requirements.txt
│   ├── README.md                      # 详细文档
│   ├── services/
│   │   ├── sandbox.py                 # 沙箱管理 ⭐
│   │   ├── template.py                # 模板系统
│   │   ├── pool.py                    # 预热池
│   │   └── deployment.py              # 部署管理
│   ├── isolation/                     # 隔离引擎
│   ├── storage/                       # 持久化存储
│   ├── tests/
│   └── migrations/
│
├── 📦 shared/                         # 共享资源
│   ├── backend/                       # 后端共享库
│   │   ├── database/                  # 数据库工具
│   │   ├── auth/                      # 认证授权
│   │   └── utils/                     # 工具函数
│   ├── frontend/                      # 前端共享资源
│   │   ├── design-system/             # 设计系统
│   │   ├── components/                # 通用组件
│   │   └── utils/                     # 前端工具
│   └── docs/                          # 共享文档
│       ├── API.md                     # API文档
│       └── DEVELOPMENT.md             # 开发指南
│
├── 🎬 Demo/                           # 演示程序
│   ├── README.md
│   ├── run_e2e_demo.py                # 完整流程Demo
│   ├── runtime_sandbox_demo.py        # Runtime沙箱Demo
│   ├── data/                          # 测试数据
│   ├── models/                        # 训练模型
│   ├── test_results/                  # 测试结果
│   └── sandboxes/                     # 沙箱存储
│
├── 📄 docs/                           # 项目文档
│   ├── getting-started.md
│   ├── architecture/
│   ├── tutorials/
│   └── api/
│
├── 🐳 docker/                         # Docker配置（待创建）
│   ├── docker-compose.yml
│   └── {Factory}/Dockerfile
│
├── ☸️ k8s/                            # Kubernetes配置（待创建）
│   └── {Factory}/
│
├── 🔧 scripts/                        # 脚本工具（待创建）
│   ├── install-all.sh
│   ├── start-all.sh
│   └── deploy.sh
│
├── ARCHITECTURE.md                    # 架构设计文档 ⭐
├── PROJECT_SUMMARY.md                 # 项目总结 ⭐
├── README.md                          # 项目说明 ⭐
├── LICENSE                            # 开源许可证
└── .gitignore                         # Git忽略配置
```

---

## 🎯 架构亮点

### 1. 一级目录 = 独立项目

```
AgentFactory/
├── ComputeFactory/    ← 独立Python包，有setup.py
├── DataFactory/       ← 独立Python包，有setup.py
├── ...                ← 每个都是独立项目！
```

**优势**:
- ✅ 开发者一眼看出项目模块
- ✅ 每个Factory可独立git clone
- ✅ 清晰的模块边界
- ✅ 便于新成员理解架构

### 2. 统一的Factory结构

每个Factory都遵循相同的结构：

```
{FactoryName}/
├── setup.py           # 包配置
├── requirements.txt   # 依赖
├── README.md          # 文档
├── services/          # 业务逻辑
├── tests/             # 测试
└── migrations/        # 数据库
```

**优势**:
- ✅ 结构一致，易于维护
- ✅ 快速上手新Factory
- ✅ 代码规范统一

### 3. 共享资源集中管理

```
shared/
├── backend/           # 后端通用库
├── frontend/          # 前端设计系统 
└── docs/              # 共享文档
```

**优势**:
- ✅ 避免代码重复
- ✅ 统一的设计系统
- ✅ 集中的文档管理

---

## 📊 vs 传统架构对比

### 传统单体架构

```
project/
├── src/
│   ├── services/      ← 混在一起
│   │   ├── compute.py
│   │   ├── data.py
│   │   └── ...
│   ├── models/        ← 难以区分
│   └── api/           ← 耦合严重
└── tests/             ← 测试混杂
```

**问题**:
- ❌ 模块边界模糊
- ❌ 代码耦合
- ❌ 难以独立部署
- ❌ 新人难以理解

### Agent Factory架构

```
AgentFactory/
├── ComputeFactory/    ← 清晰独立
├── DataFactory/       ← 清晰独立
├── ...                ← 一目了然！
```

**优势**:
- ✅ 模块边界清晰
- ✅ 低耦合
- ✅ 可独立部署
- ✅ 架构一目了然

---

## 🚀 部署模式

### Mode 1: 开发模式（单机）

```bash
# 每个Factory独立运行，方便调试
cd ComputeFactory && uvicorn api.main:app --port 8001 &
cd DataFactory && uvicorn api.main:app --port 8002 &
cd RuntimeFactory && uvicorn api.main:app --port 8006 &
...
```

### Mode 2: 生产模式（Docker Compose）

```yaml
# docker-compose.yml
services:
  compute-factory:
    build: ./ComputeFactory
    ports: ["8001:8001"]
  
  data-factory:
    build: ./DataFactory
    ports: ["8002:8002"]
  
  # ... 其他Factory
```

### Mode 3: 云原生（Kubernetes）

```yaml
# k8s/compute-factory/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: compute-factory
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: compute
        image: agentfactory/compute:latest
```

---

## 🎓 新成员学习路径

### Day 1: 理解架构

1. 查看项目根目录，看到6个Factory
2. 阅读 `ARCHITECTURE.md`
3. 了解每个Factory的职责

### Day 2: 深入一个Factory

1. 选择感兴趣的Factory（如 ComputeFactory）
2. 阅读 `ComputeFactory/README.md`
3. 查看 `services/` 中的代码
4. 运行测试：`cd ComputeFactory && pytest`

### Day 3: 运行Demo

1. 运行 `Demo/run_e2e_demo.py`
2. 观察6个Factory如何协作
3. 理解端到端流程

### Week 2: 开始贡献

1. 选择一个Factory
2. 创建功能分支
3. 开发新功能
4. 提交PR

---

## ✨ 总结

**新架构的核心价值**:

1. **清晰可见** 👁️  
   打开项目文件夹，立即看到6个Factory

2. **独立自治** 🎯  
   每个Factory是完整的项目，有setup.py、tests、docs

3. **灵活部署** 🚀  
   支持单体、微服务、混合等多种部署模式

4. **易于协作** 🤝  
   团队成员可独立工作在不同Factory

5. **新人友好** 📖  
   架构一目了然，快速上手

---

**这就是Agent Factory的模块化架构优势！** 🎉
