"""
成本追踪器 (CostTracker)
追踪和管理LLM使用成本
"""

import time
import tiktoken
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict


@dataclass
class CostRecord:
    """成本记录"""
    record_id: str
    timestamp: float
    agent_id: str
    model: str
    tokens_input: int
    tokens_output: int
    cost_usd: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def total_tokens(self) -> int:
        """总token数"""
        return self.tokens_input + self.tokens_output


class CostTracker:
    """
    成本追踪器
    
    特性:
    - 实时成本计算
    - 多模型定价支持
    - 成本报告生成
    - 预算告警
    """
    
    # 默认定价（USD per 1K tokens）
    DEFAULT_PRICING = {
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-4-turbo": {"input": 0.01, "output": 0.03},
        "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
        "claude-3-opus": {"in put": 0.015, "output": 0.075},
        "claude-3-sonnet": {"input": 0.003, "output": 0.015},
        "qwen-3": {"input": 0.0002, "output": 0.0006},
    }
    
    def __init__(self, pricing: Optional[Dict] = None):
        self.pricing = pricing or self.DEFAULT_PRICING
        self.records: List[CostRecord] = []
        self.alerts: List[Dict] = []
        self._record_counter = 0
    
    def calculate_cost(
        self,
        model: str,
        tokens_input: int,
        tokens_output: int
    ) -> float:
        """计算成本（USD）"""
        if model not in self.pricing:
            # 默认使用gpt-3.5定价
            model = "gpt-3.5-turbo"
        
        pricing = self.pricing[model]
        cost_input = (tokens_input / 1000) * pricing["input"]
        cost_output = (tokens_output / 1000) * pricing["output"]
        
        return cost_input + cost_output
    
    def count_tokens(self, text: str, model: str = "gpt-3.5-turbo") -> int:
        """计算文本的token数"""
        try:
            encoding = tiktoken.encoding_for_model(model)
            return len(encoding.encode(text))
        except:
            # 简单估算：1 token ≈ 4 characters
            return len(text) // 4
    
    def record_usage(
        self,
        agent_id: str,
        model: str,
        tokens_input: int,
        tokens_output: int,
        metadata: Optional[Dict] = None
    ) -> CostRecord:
        """记录使用并计算成本"""
        self._record_counter += 1
        
        cost = self.calculate_cost(model, tokens_input, tokens_output)
        
        record = CostRecord(
            record_id=f"cost_{self._record_counter}",
            timestamp=time.time(),
            agent_id=agent_id,
            model=model,
            tokens_input=tokens_input,
            tokens_output=tokens_output,
            cost_usd=cost,
            metadata=metadata or {}
        )
        
        self.records.append(record)
        
        # 检查告警
        self._check_alerts(record)
        
        return record
    
    def get_total_cost(
        self,
        agent_id: Optional[str] = None,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None
    ) -> float:
        """获取总成本"""
        filtered = self._filter_records(agent_id, start_time, end_time)
        return sum(r.cost_usd for r in filtered)
    
    def get_total_tokens(
        self,
        agent_id: Optional[str] = None,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None
    ) -> int:
        """获取总token数"""
        filtered = self._filter_records(agent_id, start_time, end_time)
        return sum(r.total_tokens for r in filtered)
    
    def get_cost_by_agent(self) -> Dict[str, float]:
        """按Agent统计成本"""
        costs = defaultdict(float)
        for record in self.records:
            costs[record.agent_id] += record.cost_usd
        return dict(costs)
    
    def get_cost_by_model(self) -> Dict[str, float]:
        """按模型统计成本"""
        costs = defaultdict(float)
        for record in self.records:
            costs[record.model] += record.cost_usd
        return dict(costs)
    
    def get_daily_cost(self, days: int = 7) -> Dict[str, float]:
        """获取每日成本（最近N天）"""
        now = time.time()
        daily_costs = {}
        
        for day in range(days):
            start = now - (day + 1) * 86400
            end = now - day * 86400
            cost = self.get_total_cost(start_time=start, end_time=end)
            date_str = datetime.fromtimestamp(end).strftime("%Y-%m-%d")
            daily_costs[date_str] = cost
        
        return daily_costs
    
    def get_cost_report(
        self,
        agent_id: Optional[str] = None,
        days: int = 30
    ) -> Dict:
        """生成成本报告"""
        end_time = time.time()
        start_time = end_time - days * 86400
        
        filtered = self._filter_records(agent_id, start_time, end_time)
        
        total_cost = sum(r.cost_usd for r in filtered)
        total_tokens = sum(r.total_tokens for r in filtered)
        
        # 按模型分组
        by_model = defaultdict(lambda: {"cost": 0, "tokens": 0, "calls": 0})
        for record in filtered:
            by_model[record.model]["cost"] += record.cost_usd
            by_model[record.model]["tokens"] += record.total_tokens
            by_model[record.model]["calls"] += 1
        
        return {
            "period": {
                "start": datetime.fromtimestamp(start_time).isoformat(),
                "end": datetime.fromtimestamp(end_time).isoformat(),
                "days": days
            },
            "summary": {
                "total_cost_usd": round(total_cost, 4),
                "total_tokens": total_tokens,
                "total_calls": len(filtered),
                "avg_cost_per_call": round(total_cost / len(filtered), 4) if filtered else 0,
                "daily_avg": round(total_cost / days, 4)
            },
            "by_model": dict(by_model),
            "daily_breakdown": self.get_daily_cost(days=min(days, 30))
        }
    
    def set_alert(
        self,
        alert_type: str,
        threshold: float,
        action: Optional[callable] = None
    ):
        """
        设置成本告警
        
        Args:
            alert_type: 告警类型（daily_budget, total_budget）
            threshold: 阈值（USD）
            action: 触发时的回调函数
        """
        self.alerts.append({
            "type": alert_type,
            "threshold": threshold,
            "action": action
        })
    
    def _check_alerts(self, record: CostRecord):
        """检查是否触发告警"""
        for alert in self.alerts:
            if alert["type"] == "daily_budget":
                # 检查今日成本
                today_start = datetime.now().replace(
                    hour=0, minute=0, second=0, microsecond=0
                ).timestamp()
                today_cost = self.get_total_cost(start_time=today_start)
                
                if today_cost >= alert["threshold"]:
                    if alert["action"]:
                        alert["action"](f"Daily budget exceeded: ${today_cost:.2f}")
    
    def _filter_records(
        self,
        agent_id: Optional[str],
        start_time: Optional[float],
        end_time: Optional[float]
    ) -> List[CostRecord]:
        """过滤记录"""
        filtered = self.records
        
        if agent_id:
            filtered = [r for r in filtered if r.agent_id == agent_id]
        
        if start_time:
            filtered = [r for r in filtered if r.timestamp >= start_time]
        
        if end_time:
            filtered = [r for r in filtered if r.timestamp <= end_time]
        
        return filtered
    
    def export_to_csv(self, filename: str):
        """导出到CSV"""
        import csv
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp", "agent_id", "model",
                "tokens_input", "tokens_output", "cost_usd"
            ])
            
            for record in self.records:
                writer.writerow([
                    datetime.fromtimestamp(record.timestamp).isoformat(),
                    record.agent_id,
                    record.model,
                    record.tokens_input,
                    record.tokens_output,
                    record.cost_usd
                ])
    
    def print_summary(self):
        """打印成本摘要"""
        report = self.get_cost_report(days=7)
        
        print("\n📊 成本摘要 (最近7天)")
        print("=" * 60)
        print(f"总成本:        ${report['summary']['total_cost_usd']:.4f}")
        print(f"总Tokens:      {report['summary']['total_tokens']:,}")
        print(f"总调用次数:    {report['summary']['total_calls']}")
        print(f"平均每次成本:  ${report['summary']['avg_cost_per_call']:.4f}")
        print(f"日均成本:      ${report['summary']['daily_avg']:.4f}")
        
        print("\n📈 按模型统计:")
        for model, stats in report['by_model'].items():
            print(f"   {model}:")
            print(f"      成本: ${stats['cost']:.4f}")
            print(f"      调用: {stats['calls']}次")


# Demo
def demo_cost_tracker():
    """演示CostTracker使用"""
    print("=" * 60)
    print("CostTracker Demo")
    print("=" * 60)
    
    tracker = CostTracker()
    
    # 模拟一些agent调用
    print("\n🤖 模拟Agent调用...")
    
    # GPT-4调用
    tracker.record_usage(
        agent_id="code_agent",
        model="gpt-4",
        tokens_input=1000,
        tokens_output=500
    )
    
    # GPT-3.5调用
    for i in range(5):
        tracker.record_usage(
            agent_id="chat_agent",
            model="gpt-3.5-turbo",
            tokens_input=500,
            tokens_output=300
        )
    
    # Qwen调用
    for i in range(10):
        tracker.record_usage(
            agent_id="search_agent",
            model="qwen-3",
            tokens_input=800,
            tokens_output=400
        )
    
    # 打印摘要
    tracker.print_summary()
    
    # 按Agent统计
    print("\n💰 按Agent统计成本:")
    by_agent = tracker.get_cost_by_agent()
    for agent, cost in sorted(by_agent.items(), key=lambda x: x[1], reverse=True):
        print(f"   {agent}: ${cost:.4f}")


if __name__ == "__main__":
    demo_cost_tracker()
