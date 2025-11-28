"""
性能指标收集器 (MetricsCollector)
收集和统计Agent的性能指标
"""

import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict
from datetime import datetime
import statistics


@dataclass
class MetricRecord:
    """指标记录"""
    timestamp: float
    agent_id: str
    metric_name: str
    value: float
    labels: Dict[str, str] = field(default_factory=dict)


class MetricsCollector:
    """
    性能指标收集器
    
    特性:
    - 实时指标收集
    - 多维度统计（P50, P95, P99）
    - 时间序列数据
    - Prometheus兼容
    """
    
    def __init__(self):
        self.records: List[MetricRecord] = []
        self._counters: Dict[str, float] = defaultdict(float)
        self._gauges: Dict[str, float] = {}
        self._histograms: Dict[str, List[float]] = defaultdict(list)
    
    def record_agent_call(
        self,
        agent_id: str,
        latency_ms: float,
        tokens_used: int,
        cost_usd: float,
        labels: Optional[Dict[str, str]] = None
    ):
        """
        记录Agent调用
        
        Args:
            agent_id: Agent ID
            latency_ms: 延迟（毫秒）
            tokens_used: Token使用量
            cost_usd: 成本（美元）
            labels: 额外标签
        """
        timestamp = time.time()
        labels = labels or {}
        labels["agent_id"] = agent_id
        
        # 记录延迟
        self.records.append(MetricRecord(
            timestamp=timestamp,
            agent_id=agent_id,
            metric_name="latency_ms",
            value=latency_ms,
            labels=labels
        ))
        self._histograms[f"{agent_id}.latency_ms"].append(latency_ms)
        
        # 记录token使用
        self.records.append(MetricRecord(
            timestamp=timestamp,
            agent_id=agent_id,
            metric_name="tokens_used",
            value=tokens_used,
            labels=labels
        ))
        self._counters[f"{agent_id}.tokens_total"] += tokens_used
        
        # 记录成本
        self.records.append(MetricRecord(
            timestamp=timestamp,
            agent_id=agent_id,
            metric_name="cost_usd",
            value=cost_usd,
            labels=labels
        ))
        self._counters[f"{agent_id}.cost_total"] += cost_usd
        
        # 调用次数
        self._counters[f"{agent_id}.calls_total"] += 1
    
    def record_metric(
        self,
        name: str,
        value: float,
        agent_id: Optional[str] = None,
        labels: Optional[Dict[str, str]] = None
    ):
        """记录自定义指标"""
        self.records.append(MetricRecord(
            timestamp=time.time(),
            agent_id=agent_id or "global",
            metric_name=name,
            value=value,
            labels=labels or {}
        ))
    
    def increment_counter(self, name: str, value: float = 1.0):
        """增加计数器"""
        self._counters[name] += value
    
    def set_gauge(self, name: str, value: float):
        """设置仪表值"""
        self._gauges[name] = value
    
    def observe_histogram(self, name: str, value: float):
        """观测直方图"""
        self._histograms[name].append(value)
    
    def get_stats(
        self,
        agent_id: Optional[str] = None,
        metric_name: Optional[str] = None,
        time_window_seconds: Optional[int] = None
    ) -> Dict:
        """
        获取统计信息
        
        Args:
            agent_id: 过滤特定Agent
            metric_name: 过滤特定指标
            time_window_seconds: 时间窗口（秒）
        
        Returns:
            统计字典
        """
        # 过滤记录
        filtered = self.records
        
        if agent_id:
            filtered = [r for r in filtered if r.agent_id == agent_id]
        
        if metric_name:
            filtered = [r for r in filtered if r.metric_name == metric_name]
        
        if time_window_seconds:
            cutoff = time.time() - time_window_seconds
            filtered = [r for r in filtered if r.timestamp >= cutoff]
        
        if not filtered:
            return {}
        
        # 按指标分组统计
        stats_by_metric = defaultdict(list)
        for record in filtered:
            stats_by_metric[record.metric_name].append(record.value)
        
        # 计算统计量
        result = {}
        for metric, values in stats_by_metric.items():
            result[metric] = self._calculate_stats(values)
        
        return result
    
    def _calculate_stats(self, values: List[float]) -> Dict:
        """计算统计量"""
        if not values:
            return {}
        
        sorted_values = sorted(values)
        count = len(values)
        
        return {
            "count": count,
            "sum": sum(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "min": min(values),
            "max": max(values),
            "p50": sorted_values[int(count * 0.5)],
            "p95": sorted_values[int(count * 0.95)] if count > 1 else sorted_values[0],
            "p99": sorted_values[int(count * 0.99)] if count > 1 else sorted_values[0],
            "stddev": statistics.stdev(values) if count > 1 else 0.0
        }
    
    def get_counter(self, name: str) -> float:
        """获取计数器值"""
        return self._counters.get(name, 0.0)
    
    def get_gauge(self, name: str) -> Optional[float]:
        """获取仪表值"""
        return self._gauges.get(name)
    
    def get_histogram_stats(self, name: str) -> Dict:
        """获取直方图统计"""
        values = self._histograms.get(name, [])
        return self._calculate_stats(values)
    
    def get_agent_summary(self, agent_id: str) -> Dict:
        """获取Agent摘要"""
        latency_key = f"{agent_id}.latency_ms"
        
        return {
            "agent_id": agent_id,
            "total_calls": self.get_counter(f"{agent_id}.calls_total"),
            "total_tokens": self.get_counter(f"{agent_id}.tokens_total"),
            "total_cost_usd": self.get_counter(f"{agent_id}.cost_total"),
            "latency_stats": self.get_histogram_stats(latency_key),
            "avg_tokens_per_call": (
                self.get_counter(f"{agent_id}.tokens_total") / 
                self.get_counter(f"{agent_id}.calls_total")
                if self.get_counter(f"{agent_id}.calls_total") > 0 else 0
            ),
            "avg_cost_per_call": (
                self.get_counter(f"{agent_id}.cost_total") / 
                self.get_counter(f"{agent_id}.calls_total")
                if self.get_counter(f"{agent_id}.calls_total") > 0 else 0
            )
        }
    
    def export_prometheus_format(self) -> str:
        """
        导出为Prometheus格式
        
        Returns:
            Prometheus metrics格式的字符串
        """
        lines = []
        
        # Counters
        for name, value in self._counters.items():
            metric_name = name.replace(".", "_")
            lines.append(f"# TYPE {metric_name} counter")
            lines.append(f"{metric_name} {value}")
        
        # Gauges
        for name, value in self._gauges.items():
            metric_name = name.replace(".", "_")
            lines.append(f"# TYPE {metric_name} gauge")
            lines.append(f"{metric_name} {value}")
        
        # Histograms (summary)
        for name, values in self._histograms.items():
            if not values:
                continue
            
            metric_name = name.replace(".", "_")
            stats = self._calculate_stats(values)
            
            lines.append(f"# TYPE {metric_name} summary")
            lines.append(f"{metric_name}_count {stats['count']}")
            lines.append(f"{metric_name}_sum {stats['sum']}")
            lines.append(f"{metric_name}{{quantile=\"0.5\"}} {stats['p50']}")
            lines.append(f"{metric_name}{{quantile=\"0.95\"}} {stats['p95']}")
            lines.append(f"{metric_name}{{quantile=\"0.99\"}} {stats['p99']}")
        
        return "\n".join(lines)
    
    def print_summary(self):
        """打印摘要"""
        print("\n📊 性能指标摘要")
        print("=" * 60)
        
        # 按agent分组
        agents = set(r.agent_id for r in self.records)
        
        for agent_id in sorted(agents):
            summary = self.get_agent_summary(agent_id)
            
            print(f"\n🤖 Agent: {agent_id}")
            print(f"   总调用: {summary['total_calls']:.0f}次")
            print(f"   总Tokens: {summary['total_tokens']:.0f}")
            print(f"   总成本: ${summary['total_cost_usd']:.4f}")
            
            latency = summary['latency_stats']
            if latency:
                print(f"   延迟统计:")
                print(f"      P50: {latency['p50']:.2f}ms")
                print(f"      P95: {latency['p95']:.2f}ms")
                print(f"      P99: {latency['p99']:.2f}ms")
                print(f"      平均: {latency['mean']:.2f}ms")


# Demo
def demo_metrics_collector():
    """演示MetricsCollector"""
    print("=" * 60)
    print("MetricsCollector Demo")
    print("=" * 60)
    
    collector = MetricsCollector()
    
    # 模拟一些Agent调用
    print("\n🤖 模拟Agent调用...")
    
    # code_agent: 快但贵
    for i in range(10):
        collector.record_agent_call(
            agent_id="code_agent",
            latency_ms=100 + i * 10,
            tokens_used=1000 + i * 50,
            cost_usd=0.05
        )
    
    # chat_agent: 慢但便宜
    for i in range(20):
        collector.record_agent_call(
            agent_id="chat_agent",
            latency_ms=300 + i * 20,
            tokens_used=500 + i * 20,
            cost_usd=0.01
        )
    
    # 打印摘要
    collector.print_summary()
    
    # Prometheus导出
    print("\n📈 Prometheus格式导出:")
    print(collector.export_prometheus_format()[:500] + "...")


if __name__ == "__main__":
    demo_metrics_collector()
