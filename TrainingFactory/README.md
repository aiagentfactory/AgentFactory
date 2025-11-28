# TrainingFactory - 训练工厂

基于 [Simple-Efficient/RL-Factory](https://github.com/Simple-Efficient/RL-Factory) 的优秀经验增强

## 📋 功能概述

TrainingFactory是Agent Factory的核心模块，负责从数据到模型的完整训练流程，特别针对AI Agent的Tool-calling和强化学习优化。

### 核心特性

- 🎓 **SFT监督微调**: 基础能力训练
- 🎮 **RL强化学习**: PPO、DPO、GRPO、RFT
- 🎁 **奖励建模**: Reward Model + Process Reward
- ⚡ **高效训练**: 异步并行工具调用（2x速度）
- 📚 **模型注册**: 版本管理与模型晋级
- 🔧 **多模型支持**: Qwen3、DeepSeek、Llama等

---

## 🎯 从RL-Factory学到的经验

### 1. 环境解耦设计 ✅

**RL-Factory的做法:**
- 将环境（工具、奖励函数）与训练框架解耦
- 只需提供一个工具配置和一个奖励函数即可开始训练

**应用到TrainingFactory:**
```python
# 简单的训练配置
config = TrainingConfig(
    model="Qwen3-4B",
    environment_id="env_search",  # 来自EnvironmentFactory
    reward_function="rule_based",  # 规则奖励
    tools=["search", "calculator"]  # MCP工具
)

trainer.train(config)
```

### 2. 异步并行工具调用 ⚡

**RL-Factory的优势:**
- 训练速度提升2x（vs Search-R1）
- 批处理 + 异步并行工具调用
- AsyncLLMEngine支持

**应用到TrainingFactory:**
```python
class AsyncToolExecutor:
    """异步并行工具执行器"""
    
    async def batch_execute(self, tool_calls: List[ToolCall]):
        # 并行执行所有工具调用
        tasks = [self._execute_tool(call) for call in tool_calls]
        results = await asyncio.gather(*tasks)
        return results
```

### 3.进程奖励 (Process Reward) 🎯

**RL-Factory的理念:**
- 不仅奖励最终结果，还奖励中间步骤
- 更好地指导Agent的工具调用行为

**应用到TrainingFactory:**
```python
def calculate_process_reward(trajectory):
    """计算进程奖励"""
    step_rewards = []
    for step in trajectory:
        # 每一步都给奖励
        if step.tool_call_correct:
            step_rewards.append(+0.5)
        if step.reasoning_clear:
            step_rewards.append(+0.3)
    
    final_reward = sum(step_rewards) + outcome_reward
    return final_reward
```

### 4. 多模型支持 🤖

**RL-Factory支持:**
- Qwen3（推荐，支持MCP）
- Qwen2.5
- DeepSeek
- Llama
- 未来支持多模态

**应用到TrainingFactory:**
```python
SUPPORTED_MODELS = {
    "qwen3-4b": "Qwen/Qwen3-4B-Instruct",
    "qwen3-8b": "Qwen/Qwen3-8B-Instruct",
    "deepseek-v3": "deepseek-ai/DeepSeek-V3",
    "llama3-8b": "meta-llama/Llama-3-8B-Instruct"
}
```

### 5. 高效的奖励计算 💰

**RL-Factory的方法:**
- 分布式部署LRM（如QwQ-32B）
- 异步并行计算奖励
- 工具调用结果缓存

**应用到TrainingFactory:**
```python
class DistributedRewardModel:
    """分布式奖励模型"""
    
    def __init__(self, model="QwQ-32B", num_workers=4):
        self.workers = [
            RewardWorker(model) for _ in range(num_workers)
        ]
    
    async def compute_rewards(self, trajectories):
        # 并行计算
        tasks = [
            worker.compute(traj) 
            for worker, traj in zip(self.workers, trajectories)
        ]
        rewards = await asyncio.gather(*tasks)
        return rewards
```

---

## 📁 目录结构

```
TrainingFactory/
├── README.md                  # 本文档
├── setup.py                   # 包配置
├── requirements.txt           # 依赖
│
├── services/                  # 业务逻辑
│   ├── sft_trainer.py         # SFT训练器
│   ├── rl_trainer.py          # RL训练器（PPO/DPO/GRPO）
│   ├── reward_model.py        # 奖励模型
│   ├── model_registry.py      # 模型注册
│   ├── async_executor.py      # 异步工具执行器 ⭐
│   └── process_reward.py      # 进程奖励 ⭐
│
├── algorithms/                # 训练算法
│   ├── ppo.py                 # PPO算法
│   ├── dpo.py                 # DPO算法
│   ├── grpo.py                # GRPO算法 ⭐
│   └── rft.py                 # RFT算法
│
├── models/                    # 模型适配
│   ├── qwen3.py               # Qwen3支持 ⭐
│   ├── deepseek.py            # DeepSeek支持
│   └── llama.py               # Llama支持
│
├── tools/                     # 工具集成
│   ├── mcp_tools.py           # MCP工具支持 ⭐
│   ├── custom_tools.py        # 自定义工具
│   └── tool_cache.py          # 工具缓存 ⭐
│
├── rewards/                   # 奖励系统
│   ├── rule_based.py          # 规则奖励
│   ├── model_judge.py         # 模型判断
│   └── process_reward.py      # 进程奖励 ⭐
│
├── configs/                   # 配置文件
│   ├── qwen3_grpo.yaml        # Qwen3 GRPO配置
│   └── templates/             # 配置模板
│
├── tests/                     # 测试
└── docs/                      # 文档
    └── GRPO_GUIDE.md          # GRPO使用指南
```

---

## 🚀 快速开始

### 安装

```bash
cd TrainingFactory
pip install -e .

# 安装RL依赖
pip install -e ".[rl]"
```

### 简单示例 - SFT训练

```python
from TrainingFactory.services import SFTTrainer
from TrainingFactory.models import Qwen3Model

# 1. 加载模型
model = Qwen3Model("Qwen/Qwen3-4B-Instruct")

# 2. 配置训练
trainer = SFTTrainer(
    model=model,
    dataset_id="ds_tool_calling_v1",  # 来自DataFactory
    learning_rate=2e-5,
    epochs=3
)

# 3. 开始训练
trainer.train()
```

### 高级示例 - GRPO训练（RL-Factory风格）

```python
from TrainingFactory.services import GRPOTrainer
from TrainingFactory.tools import MCPTools
from TrainingFactory.rewards import ProcessReward

# 1. 配置环境和工具
env_config = {
    "environment_id": "env_search_v1",  # 来自EnvironmentFactory
    "tools": MCPTools.load_from_config("tools/search.json"),
    "async_execution": True  # ⭐ 异步并行
}

# 2. 配置奖励函数
reward_fn = ProcessReward(
    outcome_weight=1.0,
    step_rewards={
        "correct_tool": 0.5,
        "clear_reasoning": 0.3,
        "efficient_path": 0.2
    }
)

# 3. 创建训练器
trainer = GRPOTrainer(
    model="Qwen3-4B",
    environment=env_config,
    reward_function=reward_fn,
    num_epochs=100,
    batch_size=8,
    async_rollout=True  # ⭐ 异步Rollout
)

# 4. 训练
trainer.train()
```

---

## ⚡ 性能优化

### 异步并行工具调用

基于RL-Factory的实现：

```python
class AsyncRolloutEngine:
    """异步Rollout引擎"""
    
    def __init__(self, num_workers=8):
        self.workers = [
            ToolWorker() for _ in range(num_workers)
        ]
    
    async def rollout_batch(self, prompts):
        """批量并行Rollout"""
        tasks = []
        for prompt in prompts:
            # 异步执行每个prompt的rollout
            task = self._async_rollout(prompt)
            tasks.append(task)
        
        # 并行等待所有结果
        trajectories = await asyncio.gather(*tasks)
        return trajectories
    
    async def _async_rollout(self, prompt):
        """单个异步Rollout"""
        trajectory = []
        current_state = prompt
        
        while not done:
            # 模型生成下一步
            action = await self.model.generate(current_state)
            
            # 异步执行工具调用
            if action.is_tool_call:
                result = await self.tool_executor.execute(action.tool)
                trajectory.append((action, result))
            
            current_state = update_state(current_state, action, result)
        
        return trajectory
```

### 工具调用缓存

```python
class ToolCache:
    """工具调用结果缓存"""
    
    def __init__(self):
        self.cache = {}
    
    async def execute_with_cache(self, tool_call):
        """带缓存的工具执行"""
        cache_key = self._get_cache_key(tool_call)
        
        if cache_key in self.cache:
            # 命中缓存，直接返回
            return self.cache[cache_key]
        
        # 执行工具调用
        result = await self.execute_tool(tool_call)
        
        # 缓存结果
        self.cache[cache_key] = result
        return result
```

---

## 📊 训练性能对比

基于RL-Factory的benchmark结果：

| 模型 | 框架 | 训练时间 (100 steps) | 每步时间 | 准确度 |
|------|------|---------------------|----------|--------|
| Qwen2.5-3B | Search-R1 | 7.39h | 266s | 0.356 |
| Qwen3-4B | RL-Factory | **5.30h** | **190s** | **0.458** |
| Qwen3-8B | RL-Factory | **5.76h** | **207s** | **0.463** |

**提升:**
- ⚡ 训练速度：**2x**（异步工具调用）
- 🎯 准确度：**+28%**（Qwen3 + 进程奖励）

---

## 🎓 支持的训练算法

### 1. SFT (Supervised Fine-Tuning)
- 基础的监督学习
- 适合：建立基础能力

### 2. PPO (Proximal Policy Optimization)
- 稳定的RL算法
- 适合：通用Agent训练

### 3. DPO (Direct Preference Optimization)
- 基于偏好学习
- 适合：对齐人类偏好

### 4. GRPO (Group Relative Policy Optimization) ⭐
- RL-Factory推荐
- 适合：Tool-calling优化
- 特点：组内相对优化，更稳定

### 5. RFT (Rejection Fine-Tuning)
- 基于采样的微调
- 适合：推理能力提升

---

## 🔧 MCP工具集成

支持Model Context Protocol (MCP)工具：

```python
# tools/search_tool.json
{
  "name": "web_search",
  "description": "Search the web",
  "parameters": {
    "query": {
      "type": "string",
      "description": "Search query"
    }
  },
  "mcp_server": "http://mcp-search:8080"
}
```

```python
# 使用MCP工具
from TrainingFactory.tools import MCPTools

tools = MCPTools.load_from_config("tools/search_tool.json")

# 自动集成到训练
trainer = GRPOTrainer(
    model="Qwen3-4B",
    tools=tools,  # 自动使用MCP协议
    ...
)
```

---

## 📝 配置示例

### GRPO训练配置 (Qwen3)

```yaml
# configs/qwen3_grpo.yaml
model:
  name: "Qwen/Qwen3-4B-Instruct"
  max_length: 4096

training:
  algorithm: "grpo"
  num_epochs: 100
  batch_size: 8
  learning_rate: 1e-6
  warmup_steps: 10

environment:
  environment_id: "env_search_v1"
  async_execution: true
  num_workers: 8

tools:
  - name: "web_search"
    config: "tools/search.json"
    cache_enabled: true

reward:
  type: "process_reward"
  outcome_weight: 1.0
  step_rewards:
    correct_tool: 0.5
    clear_reasoning: 0.3
    efficient_path: 0.2

optimization:
  async_rollout: true
  distributed_reward: true
  tool_cache: true
```

---

## 🔗 与其他Factory集成

### 从ComputeFactory获取资源

```python
from ComputeFactory.services import ResourceManager

# 申请GPU资源
manager = ResourceManager()
allocation = manager.allocate_resource(
    pool_type="training",
    resource_spec=ResourceSpec(
        resource_type="gpu",
        count=8,  # 8x A100
        memory_gb=640
    )
)

# 使用资源训练
trainer = GRPOTrainer(
    allocation_id=allocation.allocation_id,
    ...
)
```

### 从DataFactory加载数据

```python
from DataFactory.services import DatasetManager

# 加载数据集
dataset_manager = DatasetManager()
dataset = dataset_manager.get_dataset("ds_tool_calling_v1")

# 用于训练
trainer = SFTTrainer(
    dataset_id=dataset.dataset_id,
    ...
)
```

### 从EnvironmentFactory获取环境

```python
from EnvironmentFactory.services import ScenarioBuilder

#获取环境
scenario = ScenarioBuilder().get_scenario("env_search_v1")

# 用于RL训练
trainer = GRPOTrainer(
    environment_id=scenario.scenario_id,
    ...
)
```

---

## 🧪 测试

```bash
# 运行所有测试
pytest tests/

# 测试特定算法
pytest tests/test_grpo.py

# 性能测试
pytest tests/test_performance.py
```

---

## 📚 相关资源

- [RL-Factory项目](https://github.com/Simple-Efficient/RL-Factory)
- [VeRL框架](https://github.com/volcengine/veRL)
- [Qwen3模型](https://github.com/QwenLM/Qwen)
- [MCP协议](https://modelcontextprotocol.io/)

---

## 🎯 最佳实践

### 1. 选择合适的Base Model
- **Tool-calling**: 优先Qwen3（支持MCP）
- **推理**: Qwen3或DeepSeek
- **通用**: Llama3

### 2. 配置高效训练
```python
# ✅ 推荐配置
config = {
    "async_rollout": True,      # 异步Rollout
    "async_tools": True,        # 异步工具调用
    "tool_cache": True,         # 工具缓存
    "distributed_reward": True  # 分布式奖励
}
```

### 3. 设计好的奖励函数
```python
# ✅ 进程奖励 > 纯结果奖励
reward_fn = ProcessReward(
    outcome_weight=1.0,
    step_rewards={...}  # 奖励中间步骤
)
```

### 4. 监控训练指标
- 训练速度（steps/second）
- 奖励曲线
- 工具调用成功率
- 模型准确度

---

## 🚧 未来计划

基于RL-Factory的路线图：

- [ ] WebUI for training management
- [ ] 更多模型支持（Gemini、Claude等）
- [ ] 多模态Agent训练
- [ ] Android环境支持
- [ ] Process Reward完善
- [ ] MS-SWIFT集成

---

**TrainingFactory + RL-Factory经验 = 高效的Agent训练！** 🎉
