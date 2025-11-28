"""
OpenTelemetry集成
提供标准化的分布式追踪导出
"""

from typing import Optional, Dict, Any
import time


try:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.resources import Resource
    OTEL_AVAILABLE = True
except ImportError:
    OTEL_AVAILABLE = False


class OpenTelemetryIntegration:
    """
    OpenTelemetry集成
    
    将Agent Factory的追踪导出到OpenTelemetry标准格式
    可以发送到:
    - Jaeger
    - Zipkin
    - OpenTelemetry Collector
    - 其他OTLP兼容后端
    """
    
    def __init__(
        self,
        service_name: str = "agent-factory",
        endpoint: Optional[str] = None,
        console_export: bool = False
    ):
        """
        Args:
            service_name: 服务名称
            endpoint: OTLP endpoint (例如: http://localhost:4317)
            console_export: 是否同时输出到控制台（调试用）
        """
        if not OTEL_AVAILABLE:
            raise ImportError(
                "OpenTelemetry not installed. "
                "Install with: pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp"
            )
        
        self.service_name = service_name
        self.endpoint = endpoint
        self.console_export = console_export
        
        self.provider: Optional[TracerProvider] = None
        self.tracer: Optional[trace.Tracer] = None
        self._enabled = False
    
    def enable(self):
        """启用OpenTelemetry集成"""
        # 创建Resource（描述服务）
        resource = Resource.create({
            "service.name": self.service_name,
            "service.version": "1.0.0"
        })
        
        # 创建TracerProvider
        self.provider = TracerProvider(resource=resource)
        
        # 添加导出器
        if self.endpoint:
            # OTLP导出器（发送到Collector）
            otlp_exporter = OTLPSpanExporter(endpoint=self.endpoint)
            span_processor = BatchSpanProcessor(otlp_exporter)
            self.provider.add_span_processor(span_processor)
        
        if self.console_export:
            # 控制台导出器（调试用）
            console_exporter = ConsoleSpanExporter()
            console_processor = BatchSpanProcessor(console_exporter)
            self.provider.add_span_processor(console_processor)
        
        # 设置全局TracerProvider
        trace.set_tracer_provider(self.provider)
        
        # 获取tracer
        self.tracer = trace.get_tracer(__name__)
        
        self._enabled = True
        
        print(f"✅ OpenTelemetry enabled for service: {self.service_name}")
        if self.endpoint:
            print(f"   Exporting to: {self.endpoint}")
    
    def create_span(
        self,
        name: str,
        attributes: Optional[Dict[str, Any]] = None
    ):
        """
        创建span
        
        用法:
            with otel.create_span("operation") as span:
                span.set_attribute("key", "value")
                do_something()
        """
        if not self._enabled or not self.tracer:
            raise RuntimeError("OpenTelemetry not enabled. Call enable() first.")
        
        span = self.tracer.start_span(name)
        
        if attributes:
            for key, value in attributes.items():
                span.set_attribute(key, value)
        
        return span
    
    def shutdown(self):
        """关闭并刷新所有spans"""
        if self.provider:
            self.provider.shutdown()
        
        self._enabled = False
        print("✅ OpenTelemetry shutdown")


# Demo（需要安装opentelemetry包）
def demo_opentelemetry():
    """演示OpenTelemetry集成"""
    print("=" * 60)
    print("OpenTelemetry Integration Demo")
    print("=" * 60)
    
    if not OTEL_AVAILABLE:
        print("\n❌ OpenTelemetry未安装")
        print("安装命令:")
        print("   pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp")
        return
    
    # 创建集成（控制台导出）
    otel = OpenTelemetryIntegration(
        service_name="agent-factory-demo",
        console_export=True  # 输出到控制台
    )
    
    # 启用
    otel.enable()
    
    # 创建spans
    print("\n🔍 创建追踪spans...")
    
    with otel.create_span("train_agent") as span:
        span.set_attribute("agent_type", "code_generator")
        time.sleep(0.1)
        
        with otel.create_span("load_data"):
            time.sleep(0.05)
        
        with otel.create_span("train_model"):
            time.sleep(0.08)
    
    # 等待导出
    time.sleep(1)
    
    # 关闭
    otel.shutdown()
    
    print("\n✅ Spans已导出到控制台")


if __name__ == "__main__":
    demo_opentelemetry()
