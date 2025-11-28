# ObservabilityFactory - 可观测性工厂

**企业级LLM Agent可观测性、监控和追踪系统**

## 📋功能概述

ObservabilityFactory为Agent Factory提供全方位的可观测性能力，包括分布式追踪、性能监控、成本追踪和结构化日志。

### 核心特性

- 🔍 **分布式追踪**: 端到端执行路径追踪
- 📊 **性能监控**: 实时metrics收集和告警
- 💰 **成本管理**: Token使用和成本追踪
- 📝 **结构化日志**: 便于查询和分析
- 🔗 **标准集成**: OpenTelemetry, Prometheus

---

## 🎯 为什么需要ObservabilityFactory？

根据2024年的调查，**可观测性是LLM生产部署的最大挑战**：

1. **非确定性**: LLM输出不稳定，需要追踪每次调用
2. **复杂工作流**: Agent调用chain复杂，需要可视化
3. **成本管理**: Token费用高，需要实时监控
4. **调试困难**: 多步推理难以调试，需要完整trace

---

## 📁 目录结构

```
ObservabilityFactory/
├── README.md
├── setup.py
├── requirements.txt
│
├── services/                # 核心服务
│   ├── tracer.py           # 分布式追踪
│   ├── metrics.py          # 性能指标
│   ├── logger.py           # 结构化日志
│   └── cost_tracker.py     # 成本追踪
│
├── integrations/            # 外部集成
│   ├── opentelemetry.py    # OpenTelemetry
│   ├── prometheus.py       # Prometheus
│   └── langfuse.py         # Langfuse（可选）
│
├── dashboard/               # 监控面板配置
│   ├── grafana/            # Grafana dashboards
│   └── prometheus/         # Prometheus rules
│
└── tests/                   # 测试
```

---

## 🚀 快速开始

### 安装

```bash
cd ObservabilityFactory
pip install -e .
```

### 基础使用

#### 1. 追踪Agent执行

```python
from ObservabilityFactory import Tracer

# 自动追踪
@Tracer.trace_agent("math_agent")
def train_math_agent(config):
    # 所有子调用都会被追踪
    data = load_data()
    model = train_model(data)
    result = evaluate(model)
    return result

# 手动追踪
with Tracer.start_span("custom_operation") as span:
    span.set_attribute("user_id", "user_001")
    result = do_something()
    span.set_attribute("result_count", len(result))
```

#### 2. 收集性能指标

```python
from ObservabilityFactory import MetricsCollector

metrics = MetricsCollector()

# 记录Agent调用
metrics.record_agent_call(
    agent_id="agent_001",
    latency_ms=234.5,
    tokens_used=1250,
    cost_usd=0.025
)

# 获取统计
stats = metrics.get_stats(agent_id="agent_001")
print(f"平均延迟: {stats['avg_latency_ms']}ms")
print(f"总成本: ${stats['total_cost']}")
```

#### 3. 追踪成本

```python
from ObservabilityFactory import CostTracker

tracker = CostTracker()

# 自动追踪
with tracker.track_cost(agent_id="agent_001"):
    response = llm.generate(prompt)
    # 成本自动计算

# 查看成本报告
report = tracker.get_cost_report(
    start_date="2024-11-01",
    end_date="2024-11-30"
)
print(report)
```

---

## 📊 监控指标

### 关键指标

| 类别 | 指标 | 说明 |
|------|------|------|
| **性能** | latency_ms | 响应延迟 |
| | tokens_per_second | Token生成速度 |
| | throughput | 吞吐量 |
| **成本** | cost_per_request | 每请求成本 |
| | total_tokens | 总Token数 |
| | cost_per_day | 每日成本 |
| **质量** | success_rate | 成功率 |
| | error_rate | 错误率 |
| | timeout_rate | 超时率 |
| **资源** | gpu_utilization | GPU利用率 |
| | memory_usage | 内存使用 |
| | queue_depth | 队列深度 |

---

## 🔗 集成

### OpenTelemetry

```python
from ObservabilityFactory.integrations import OpenTelemetryIntegration

# 配置
otel = OpenTelemetryIntegration(
    service_name="agent-factory",
    endpoint="http://otel-collector:4317"
)

# 自动导出traces
otel.enable()
```

### Prometheus

```python
from ObservabilityFactory.integrations import PrometheusExporter

# 启动metrics导出
exporter = PrometheusExporter(port=9090)
exporter.start()

# Prometheus会抓取 http://localhost:9090/metrics
```

### Grafana Dashboard

导入预配置的Dashboard：

```bash
# 导入Grafana dashboard
kubectl apply -f dashboard/grafana/agent-factory-dashboard.json
```

---

## 📈 可视化

### 1. 追踪可视化

```
Agent调用追踪
┌─────────────────────────────────────────────────────────┐
│ train_agent                         [2.34s]             │
│   ├─ load_data                      [0.45s]             │
│   ├─ train_model                    [1.52s]             │
│   │   ├─ llm.generate (x10)         [1.20s]             │
│   │   └─ update_model               [0.32s]             │
│   └─ evaluate                       [0.37s]             │
│       ├─ run_benchmark              [0.25s]             │
│       └─ calculate_metrics          [0.12s]             │
└─────────────────────────────────────────────────────────┘
```

### 2. 成本仪表板

```
成本概览 (2024-11)
┌─────────────────────────────────────┐
│ 总成本:        $1,234.56           │
│ 每日平均:      $41.15              │
│ Token总数:     12.3M tokens        │
│ 最贵Agent:     code_agent ($456)   │
└─────────────────────────────────────┘

成本趋势
  $60 ┤     ╭╮
  $50 ┤    ╭╯╰╮   ╭╮
  $40 ┤   ╭╯  ╰╮ ╭╯╰╮
  $30 ┤  ╭╯    ╰╮╯  ╰─
  $20 ┤╭╯       ╰
   1  5   10   15  20  25  30 (日)
```

---

## 🎯 使用场景

### 场景1: 调试训练慢

```python
# 发现瓶颈
tracer = Tracer()
trace = tracer.get_trace("training_job_001")

# 分析耗时
for span in trace.spans:
    if span.duration_ms > 1000:
        print(f"慢操作: {span.name} - {span.duration_ms}ms")

# 输出:
# 慢操作: data_loading - 3200ms  ← 瓶颈！
# 慢操作: model_train - 45000ms
```

### 场景2: 成本超标

```python
# 成本告警
cost_tracker = CostTracker()
cost_tracker.set_alert(
    threshold_usd=100,  # 每日超100美元告警
    action=send_email
)

# 分析成本
report = cost_tracker.get_cost_breakdown()
# Agent: code_executor - $45.23 (45%)  ← 占比最高
# Agent: data_analyst  - $32.10 (32%)
# Agent: search_agent  - $22.67 (23%)
```

### 场景3: 性能优化

```python
# 对比A/B测试
metrics = MetricsCollector()

# 版本A
stats_a = metrics.get_stats(agent_id="agent_v1")

# 版本B
stats_b = metrics.get_stats(agent_id="agent_v2")

# 对比
print(f"延迟改善: {stats_a['p95_latency'] - stats_b['p95_latency']}ms")
print(f"成本节省: ${stats_a['avg_cost'] - stats_b['avg_cost']}")
```

---

## 🔧 配置

### 配置文件

```yaml
# observability_config.yaml
tracing:
  enabled: true
  backend: opentelemetry
  endpoint: http://otel-collector:4317
  sample_rate: 1.0  # 100%采样

metrics:
  enabled: true
  export_interval: 60  # 秒
  prometheus_port: 9090

logging:
  level: INFO
  format: json
  output: stdout

cost_tracking:
  enabled: true
  pricing:
    gpt-4: 0.03  # per 1k tokens
    gpt-3.5: 0.002
  alerts:
    - type: daily_budget
      threshold: 100
      action: email
```

---

## 📚 最佳实践

### 1. 追踪粒度

```python
# ✅ 好: 追踪关键操作
@Tracer.trace_agent("train")
def train_agent():
    pass

# ❌ 差: 追踪过于细粒度
@Tracer.trace()  # 每个函数都追踪，开销大
def add(a, b):
    return a + b
```

### 2. 成本优化

```python
# ✅ 好: 使用成本追踪选择模型
if task.complexity == "low":
    model = "gpt-3.5"  # 便宜
else:
    model = "gpt-4"    # 贵但准确

# ❌ 差: 总是用最贵的模型
model = "gpt-4"  # 成本高
```

### 3. 告警设置

```python
# ✅ 好: 分级告警
cost_tracker.add_alert(level="warning", threshold=80)
cost_tracker.add_alert(level="critical", threshold=100)

# ❌ 差: 过于敏感
cost_tracker.add_alert(level="critical", threshold=1)  # 太敏感
```

---

## 🧪 测试

```bash
# 运行测试
pytest tests/

# 测试追踪
pytest tests/test_tracer.py

# 测试成本计算
pytest tests/test_cost_tracker.py
```

---

## 🔗 相关资源

- [OpenTelemetry官方文档](https://opentelemetry.io/)
- [Prometheus监控最佳实践](https://prometheus.io/docs/practices/)
- [Langfuse - LLM可观测性](https://langfuse.com/)

---

## 🎯 预期收益

实施ObservabilityFactory后：

- ✅ **调试效率提升**: 从小时→分钟
- ✅ **成本节省**: 20-30%（通过优化发现）
- ✅ **性能提升**: 识别瓶颈，优化latency
- ✅ **可靠性**: 快速发现和修复问题

---

**ObservabilityFactory = Agent Factory的"眼睛"，看清一切！** 👁️
