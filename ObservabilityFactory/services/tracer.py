"""
分布式追踪器 (Tracer)
提供端到端的Agent执行路径追踪
"""

import time
import uuid
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from contextlib import contextmanager
import functools


@dataclass
class Span:
    """追踪跨度（一个操作的执行记录）"""
    span_id: str
    trace_id: str
    name: str
    start_time: float
    end_time: Optional[float] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    parent_span_id: Optional[str] = None
    status: str = "OK"  # OK, ERROR
    
    @property
    def duration_ms(self) -> float:
        """执行时长（毫秒）"""
        if self.end_time:
            return (self.end_time - self.start_time) * 1000
        return 0.0
    
    def set_attribute(self, key: str, value: Any):
        """设置属性"""
        self.attributes[key] = value
    
    def set_status(self, status: str):
        """设置状态"""
        self.status = status
    
    def finish(self):
        """结束span"""
        self.end_time = time.time()
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "span_id": self.span_id,
            "trace_id": self.trace_id,
            "name": self.name,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration_ms": self.duration_ms,
            "attributes": self.attributes,
            "parent_span_id": self.parent_span_id,
            "status": self.status
        }


@dataclass
class Trace:
    """完整的追踪记录"""
    trace_id: str
    spans: List[Span] = field(default_factory=list)
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    
    def add_span(self, span: Span):
        """添加span"""
        self.spans.append(span)
    
    @property
    def duration_ms(self) -> float:
        """总执行时长"""
        if self.end_time:
            return (self.end_time - self.start_time) * 1000
        return 0.0
    
    def get_root_span(self) -> Optional[Span]:
        """获取根span"""
        for span in self.spans:
            if span.parent_span_id is None:
                return span
        return None
    
    def visualize(self) -> str:
        """可视化trace（树形结构）"""
        lines = []
        lines.append(f"Trace ID: {self.trace_id}")
        lines.append(f"Duration: {self.duration_ms:.2f}ms\n")
        
        # 构建span树
        root = self.get_root_span()
        if root:
            self._visualize_span(root, lines, indent=0)
        
        return "\n".join(lines)
    
    def _visualize_span(self, span: Span, lines: List[str], indent: int):
        """递归可视化span"""
        prefix = "  " * indent + "├─ " if indent > 0 else ""
        duration_str = f"[{span.duration_ms:.2f}ms]"
        status_icon = "✓" if span.status == "OK" else "✗"
        
        line = f"{prefix}{status_icon} {span.name} {duration_str}"
        lines.append(line)
        
        # 添加关键属性
        if span.attributes:
            for key, value in list(span.attributes.items())[:3]:  # 最多显示3个
                attr_line = f"{' ' * (indent + 1)}  └─ {key}: {value}"
                lines.append(attr_line)
        
        # 递归显示子span
        children = [s for s in self.spans if s.parent_span_id == span.span_id]
        for child in children:
            self._visualize_span(child, lines, indent + 1)


class Tracer:
    """
    分布式追踪器
    
    特性:
    - 自动追踪Agent执行路径
    - 嵌套span支持
    - 属性记录
    - 可视化trace
    """
    
    def __init__(self):
        self.traces: Dict[str, Trace] = {}
        self.current_trace_id: Optional[str] = None
        self.current_span_id: Optional[str] = None
        self._span_stack: List[str] = []
    
    def start_trace(self, trace_id: Optional[str] = None) -> str:
        """开始新的trace"""
        if trace_id is None:
            trace_id = f"trace_{uuid.uuid4().hex[:16]}"
        
        trace = Trace(trace_id=trace_id)
        self.traces[trace_id] = trace
        self.current_trace_id = trace_id
        
        return trace_id
    
    def end_trace(self, trace_id: Optional[str] = None):
        """结束trace"""
        trace_id = trace_id or self.current_trace_id
        if trace_id and trace_id in self.traces:
            self.traces[trace_id].end_time = time.time()
            self.current_trace_id = None
    
    @contextmanager
    def start_span(
        self,
        name: str,
        attributes: Optional[Dict[str, Any]] = None
    ):
        """
        开始一个span（上下文管理器）
        
        用法:
            with tracer.start_span("operation") as span:
                span.set_attribute("key", "value")
                do_something()
        """
        # 确保有trace
        if not self.current_trace_id:
            self.start_trace()
        
        # 创建span
        span = Span(
            span_id=f"span_{uuid.uuid4().hex[:16]}",
            trace_id=self.current_trace_id,
            name=name,
            start_time=time.time(),
            parent_span_id=self.current_span_id,  # 嵌套支持
            attributes=attributes or {}
        )
        
        # 添加到trace
        self.traces[self.current_trace_id].add_span(span)
        
        # 更新当前span
        old_span_id = self.current_span_id
        self.current_span_id = span.span_id
        self._span_stack.append(span.span_id)
        
        try:
            yield span
        except Exception as e:
            span.set_status("ERROR")
            span.set_attribute("error", str(e))
            raise
        finally:
            span.finish()
            self._span_stack.pop()
            self.current_span_id = self._span_stack[-1] if self._span_stack else old_span_id
    
    def trace_agent(self, agent_name: str) -> Callable:
        """
        装饰器：自动追踪Agent函数
        
        用法:
            @tracer.trace_agent("math_agent")
            def train_agent(config):
                pass
        """
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # 开始trace
                trace_id = self.start_trace()
                
                # 执行并追踪
                with self.start_span(f"{agent_name}.{func.__name__}") as span:
                    span.set_attribute("agent_name", agent_name)
                    span.set_attribute("function", func.__name__)
                    
                    try:
                        result = func(*args, **kwargs)
                        span.set_attribute("result_type", type(result).__name__)
                        return result
                    finally:
                        self.end_trace(trace_id)
            
            return wrapper
        return decorator
    
    def get_trace(self, trace_id: str) -> Optional[Trace]:
        """获取trace"""
        return self.traces.get(trace_id)
    
    def get_all_traces(self) -> List[Trace]:
        """获取所有traces"""
        return list(self.traces.values())
    
    def export_trace(self, trace_id: str) -> Dict:
        """导出trace为JSON"""
        trace = self.get_trace(trace_id)
        if not trace:
            return {}
        
        return {
            "trace_id": trace.trace_id,
            "duration_ms": trace.duration_ms,
            "start_time": trace.start_time,
            "end_time": trace.end_time,
            "spans": [span.to_dict() for span in trace.spans]
        }
    
    def print_trace(self, trace_id: str):
        """打印trace（可视化）"""
        trace = self.get_trace(trace_id)
        if trace:
            print(trace.visualize())
    
    def get_stats(self, trace_id: str) -> Dict:
        """获取trace统计"""
        trace = self.get_trace(trace_id)
        if not trace:
            return {}
        
        return {
            "total_spans": len(trace.spans),
            "duration_ms": trace.duration_ms,
            "success_rate": sum(1 for s in trace.spans if s.status == "OK") / len(trace.spans) if trace.spans else 0,
            "avg_span_duration": sum(s.duration_ms for s in trace.spans) / len(trace.spans) if trace.spans else 0
        }


# 全局tracer实例
_global_tracer = Tracer()

def get_tracer() -> Tracer:
    """获取全局tracer"""
    return _global_tracer


# Demo
def demo_tracer():
    """演示Tracer使用"""
    print("=" * 60)
    print("Tracer Demo")
    print("=" * 60)
    
    tracer = get_tracer()
    
    # 使用装饰器
    @tracer.trace_agent("demo_agent")
    def train_agent():
        # 模拟训练步骤
        with tracer.start_span("load_data") as span:
            time.sleep(0.1)
            span.set_attribute("data_size", 1000)
        
        with tracer.start_span("train_model") as span:
            # 嵌套span
            with tracer.start_span("forward_pass"):
                time.sleep(0.2)
            
            with tracer.start_span("backward_pass"):
                time.sleep(0.15)
            
        span.set_attribute("model_type", "transformer")
        
        with tracer.start_span("evaluate") as span:
            time.sleep(0.05)
            span.set_attribute("accuracy", 0.95)
    
    # 执行
    train_agent()
    
    # 获取trace
    traces = tracer.get_all_traces()
    if traces:
        trace = traces[0]
        
        # 可视化
        print("\n📊 Trace可视化:")
        print(trace.visualize())
        
        # 统计
        print("\n📈 Trace统计:")
        stats = tracer.get_stats(trace.trace_id)
        for key, value in stats.items():
            print(f"   {key}: {value}")


if __name__ == "__main__":
    demo_tracer()
