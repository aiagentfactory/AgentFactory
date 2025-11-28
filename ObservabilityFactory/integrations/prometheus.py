"""
Prometheus导出器
将metrics导出为Prometheus格式
"""

from typing import Optional
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler


class PrometheusHandler(BaseHTTPRequestHandler):
    """HTTP handler for Prometheus metrics"""
    
    metrics_collector = None  # Will be set by PrometheusExporter
    
    def do_GET(self):
        """Handle GET request"""
        if self.path == "/metrics":
            # 导出metrics
            metrics_text = self.metrics_collector.export_prometheus_format()
            
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(metrics_text.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Suppress log messages"""
        pass


class PrometheusExporter:
    """
    Prometheus Exporter
    
    启动HTTP服务器，在/metrics端点导出指标
    Prometheus可以定期抓取这个端点
    """
    
    def __init__(
        self,
        metrics_collector,
        port: int = 9090,
        host: str = "0.0.0.0"
    ):
        """
        Args:
            metrics_collector: MetricsCollector实例
            port: HTTP端口
            host: 绑定地址
        """
        self.metrics_collector = metrics_collector
        self.port = port
        self.host = host
        
        self.server: Optional[HTTPServer] = None
        self.thread: Optional[threading.Thread] = None
    
    def start(self):
        """启动导出服务器"""
        # 设置handler的metrics_collector
        PrometheusHandler.metrics_collector = self.metrics_collector
        
        # 创建服务器
        self.server = HTTPServer((self.host, self.port), PrometheusHandler)
        
        # 在后台线程运行
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        
        print(f"✅ Prometheus exporter started at http://{self.host}:{self.port}/metrics")
        print(f"   Prometheus configuration:")
        print(f"   ```yaml")
        print(f"   scrape_configs:")
        print(f"     - job_name: 'agent-factory'")
        print(f"       static_configs:")
        print(f"         - targets: ['{self.host}:{self.port}']")
        print(f"   ```")
    
    def stop(self):
        """停止导出服务器"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            print("✅ Prometheus exporter stopped")


# Demo
def demo_prometheus_exporter():
    """演示Prometheus导出器"""
    print("=" * 60)
    print("Prometheus Exporter Demo")
    print("=" * 60)
    
    from services.metrics import MetricsCollector
    import time
    
    # 创建metrics collector
    collector = MetricsCollector()
    
    # 记录一些数据
    print("\n📊 记录metrics...")
    for i in range(10):
        collector.record_agent_call(
            agent_id="demo_agent",
            latency_ms=100 + i * 10,
            tokens_used=500,
            cost_usd=0.01
        )
    
    # 启动导出器
    exporter = PrometheusExporter(collector, port=9090)
    exporter.start()
    
    print("\n🌐 访问 http://localhost:9090/metrics 查看指标")
    print("按Ctrl+C停止...")
    
    try:
        # 持续记录数据
        while True:
            time.sleep(2)
            collector.record_agent_call(
                agent_id="demo_agent",
                latency_ms=120,
                tokens_used=600,
                cost_usd=0.012
            )
            print(".", end="", flush=True)
    except KeyboardInterrupt:
        print("\n\n停止中...")
        exporter.stop()


if __name__ == "__main__":
    demo_prometheus_exporter()
