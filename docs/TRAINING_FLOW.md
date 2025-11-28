# Agent Factory - 从零到一训练Agent完整流程

## 🎯 流程概览

```
┌─────────────────────────────────────────────────────────────┐
│                从零到一训练一个AI Agent                      │
└─────────────────────────────────────────────────────────────┘

Step 1: 资源准备        Step 2: 数据准备        Step 3: 环境构建
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│ Compute      │       │ Data         │       │ Environment  │
│ Factory      │──────▶│ Factory      │──────▶│ Factory      │
│              │       │              │       │              │
│ 分配GPU/CPU  │       │ 采集清洗数据 │       │ 创建测试环境 │
└──────────────┘       └──────────────┘       └──────────────┘
                                                      │
                                                      ▼
Step 6: 部署上线        Step 5: 质量评估        Step 4: 模型训练
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│ Runtime      │       │ Evaluation   │       │ Training     │
│ Factory      │◀──────│ Factory      │◀──────│ Factory      │
│              │       │              │       │              │
│ 生产部署Agent│       │ 评估模型质量 │       │ 训练优化模型 │
└──────────────┘       └──────────────┘       └──────────────┘
```

---

## 📋 详细步骤

### Step 1: ComputeFactory - 资源准备 🔧

**目标**: 为训练分配计算资源

**输入**: 无（首步）

**操作**:
1. 检查可用资源池
2. 提交资源申请（如2x GPU, 80GB内存）
3. 创建训练作业队列
4. 分配资源ID

**输出**: 
- `allocation_id`: alloc_xxx
- `resource_spec`: 2x GPU, 80GB RAM

**示例**:
```python
from ComputeFactory.services import ResourceManager

manager = ResourceManager()
allocation = manager.allocate_resource(
    pool_type="training",
    resource_spec=ResourceSpec(
        resource_type="gpu",
        count=2,
        memory_gb=80
    )
)
# allocation_id: alloc_1234567890
```

**为什么重要？**  
没有GPU/CPU，后面都是空谈。ComputeFactory确保整个流程有算力保障。

---

### Step 2: DataFactory - 数据准备 🗃️

**目标**: 构建高质量训练数据集

**输入**: 
- 原始交互日志
- 人工标注（可选）

**操作**:
1. **采集**: 收集Agent交互数据
   ```python
   collector.collect_interaction(
       agent_id="v0",
       prompt="What is 5+3?",
       response="8"
   )
   ```

2. **清洗**: PII脱敏、去重、过滤
   ```python
   cleaner.remove_pii(text)
   cleaner.filter_garbage(text)
   ```

3. **标注**: 人工或LLM打分
   ```python
   annotator.add_human_rating(
       event_id="evt_001",
       rating=0.9
   )
   ```

4. **构建**: 创建数据集
   ```python
   dataset = dataset_manager.create_dataset(
       name="math_qa_v1",
       dataset_type="sft",
       event_ids=[...]
   )
   ```

**输出**:
- `dataset_id`: ds_math_qa_v1
- 数据集大小: 1000条
- 数据类型: SFT (监督微调)

**为什么重要？**  
"Garbage in, garbage out"。高质量数据是模型性能的基础。

---

### Step 3: EnvironmentFactory - 环境构建 🌍

**目标**: 创建Agent训练和测试环境

**输入**:
- 任务定义
- 场景描述

**操作**:
1. **定义环境**: 选择环境类型
   ```python
   scenario = ScenarioBuilder()
   scenario.set_type("math_calculator")
   scenario.add_test_cases([
       {"prompt": "3+7?", "expected": 10},
       {"prompt": "20-8?", "expected": 12}
   ])
   ```

2. **轨迹生成**: 在环境中运行收集数据
   ```python
   executor = EnvExecutor()
   trace = executor.run(
       agent="baseline",
       scenario=scenario
   )
   ```

3. **环境验证**: 确保环境稳定
   ```python
   validator.check_environment(scenario)
   ```

**输出**:
- `scenario_id`: scn_math_v1
- 测试用例数: 5个
- 环境类型: calculator

**为什么重要？**  
Agent需要在真实或模拟环境中学习。好的环境=好的训练场地。

---

### Step 4: TrainingFactory - 模型训练 🧠

**目标**: 使用数据在环境中训练Agent

**输入**:
- `dataset_id` (来自DataFactory)
- `allocation_id` (来自ComputeFactory)
- `scenario_id` (来自EnvironmentFactory)

**操作**:
1. **创建训练作业**:
   ```python
   job = training_factory.create_job(
       name="MathAgent_v1",
       model_base="gpt-3.5-turbo",
       dataset_id="ds_math_qa_v1",
       training_type="sft"
   )
   ```

2. **执行训练**:
   ```python
   trainer = SFTTrainer()
   trainer.train(
       model=model,
       dataset=dataset,
       epochs=3,
       batch_size=8
   )
   ```

3. **保存模型**:
   ```python
   registry.register_model(
       model_id="math_agent_v1",
       checkpoint_path="/models/math_v1.pt"
   )
   ```

**输出**:
- `model_id`: math_agent_v1
- 训练准确度: 95%
- Checkpoint路径: /models/math_v1.pt

**为什么重要？**  
这是整个流程的核心！前三步都是为训练做准备。

---

### Step 5: EvaluationFactory - 质量评估 🏆

**目标**: 全方位评估模型质量

**输入**:
- `model_id` (来自TrainingFactory)
- `scenario_id` (测试环境)

**操作**:
1. **创建评估任务**:
   ```python
   taskset = eval_factory.create_taskset(
       name="math_eval_L3",
       difficulty="medium",
       test_cases=[...]
   )
   ```

2. **运行评估**:
   ```python
   results = evaluator.run(
       model_id="math_agent_v1",
       taskset_id="taskset_001"
   )
   ```

3. **多维度打分**:
   - 准确度: 100% (5/5通过)
   - 安全性: 通过
   - 延迟: 平均200ms

4. **LLM-as-judge**:
   ```python
   judge_score = llm_judge.evaluate(
       prediction=pred,
       reference=ref
   )
   ```

**输出**:
- 评估结果: PASS ✅
- 准确度: 100%
- 质量分数: 92/100

**决策点**: 
- ✅ 准确度≥80% → 进入Step 6 (部署)
- ❌ 准确度<80% → 回到Step 4 (继续训练)

**为什么重要？**  
质量门禁！只有通过评估的Agent才能部署到生产。

---

### Step 6: RuntimeFactory - 部署上线 ⚡

**目标**: 将Agent部署到生产环境

**输入**:
- `model_id` (评估通过的模型)
- 部署配置

**操作**:
1. **选择模板**:
   ```python
   template = TemplateLibrary.get_template("basic-agent")
   ```

2. **从预热池分配沙箱** (快速):
   ```python
   pool = pool_manager.get_pool("basic-agent")
   sandbox = pool.acquire("math_agent_v1")
   # 分配时间: <1ms ⚡
   ```

3. **加载模型**:
   ```python
   deployment = deployer.deploy(
       agent_id="math_agent_v1",
       sandbox_id=sandbox.sandbox_id,
       model_path="/models/math_v1.pt"
   )
   ```

4. **健康检查**:
   ```python
   health = sandbox.health_check()
   # status: healthy ✅
   ```

5. **开始服务**:
   ```python
   response = agent.run("What is 42+28?")
   # "The answer is 70.0"
   ```

**输出**:
- `deployment_id`: deploy_math_v1
- 状态: Active
- 端点: http://agent-api/math_v1

**为什么重要？**  
终点线！Agent可以为真实用户服务了。

---

## 🔄 完整示例代码

```python
"""
完整的从0到1训练流程
"""

# Step 1: 分配资源
from ComputeFactory.services import ResourceManager
manager = ResourceManager()
allocation = manager.allocate_resource(
    pool_type="training",
    resource_spec=ResourceSpec(resource_type="gpu", count=2)
)

# Step 2: 准备数据
from DataFactory.services import DataCollector, DatasetManager
collector = DataCollector()
dataset_manager = DatasetManager()

# 收集数据
for prompt, answer in training_data:
    event = collector.collect_interaction(
        agent_id="v0",
        prompt=prompt,
        response=answer
    )
    event_ids.append(event.event_id)

# 创建数据集
dataset = dataset_manager.create_dataset(
    name="training_data_v1",
    dataset_type="sft",
    event_ids=event_ids
)

# Step 3: 创建环境
from EnvironmentFactory.services import ScenarioBuilder
builder = ScenarioBuilder()
scenario = builder.create_scenario(
    name="test_env_v1",
    test_cases=test_cases
)

# Step 4: 训练模型
from TrainingFactory.services import SFTTrainer
trainer = SFTTrainer()
model = trainer.train(
    dataset_id=dataset.dataset_id,
    model_base="gpt-3.5-turbo",
    epochs=3
)

# Step 5: 评估
from EvaluationFactory.services import Evaluator
evaluator = Evaluator()
results = evaluator.run(
    model_id=model.model_id,
    scenario_id=scenario.scenario_id
)

if results.verdict == "PASS":
    # Step 6: 部署
    from RuntimeFactory.services import PoolManager
    pool_manager = PoolManager()
    sandbox = pool_manager.acquire_sandbox(
        template_name="basic-agent",
        agent_id=model.model_id
    )
    print(f"✅ Agent deployed: {sandbox.sandbox_id}")
else:
    print("❌ Agent failed evaluation, need more training")
```

---

## 📊 时间估算

| 步骤 | 操作 | 预计时间 |
|------|------|----------|
| Step 1 | 分配资源 | <1分钟 |
| Step 2 | 数据准备 | 1-2小时 (1000条) |
| Step 3 | 环境构建 | 10-30分钟 |
| Step 4 | 模型训练 | 30分钟-数小时 |
| Step 5 | 质量评估 | 10-30分钟 |
| Step 6 | 部署上线 | <1秒 (预热池) |

**总计**: 约2-6小时（取决于数据量和模型大小）

---

## 🎯 关键成功因素

### 1. 高质量数据 (Step 2)
- ✅ 数量充足（>=1000条）
- ✅ 标注准确（人工+LLM双重验证）
- ✅ 分布均衡（覆盖各种场景）

### 2. 合适的环境 (Step 3)
- ✅ 真实性（贴近生产环境）
- ✅ 稳定性（可重复运行）
- ✅ 多样性（各种边界情况）

### 3. 充足的训练 (Step 4)
- ✅ 合适的epochs（不欠拟合不过拟合）
- ✅ 足够的算力（GPU数量和时长）
- ✅ 好的超参数（学习率、batch size等）

### 4. 严格的评估 (Step 5)
- ✅ 多维度指标（不只看准确度）
- ✅ 真实场景测试（贴近生产）
- ✅ 安全性检查（避免有害输出）

---

## 🔁 迭代优化循环

```
训练 → 评估 → 分析问题 → 改进
  ▲                          │
  └──────────────────────────┘

常见改进点:
1. 数据不足 → 回Step 2扩充数据
2. 环境不够 → 回Step 3增加场景
3. 训练不够 → 回Step 4调整超参数
4. 评估未过 → 分析错误，针对性优化
```

---

## ✨ 总结

**Agent Factory的From Zero to Agents流程**:

1. **ComputeFactory** → 保障算力
2. **DataFactory** → 打造数据
3. **EnvironmentFactory** → 构建赛道
4. **TrainingFactory** → 训练奔跑
5. **EvaluationFactory** → 验收成果
6. **RuntimeFactory** → 上场比赛

**每个Factory都是不可或缺的一环，共同完成从零到一的AI Agent训练！** 🎉
