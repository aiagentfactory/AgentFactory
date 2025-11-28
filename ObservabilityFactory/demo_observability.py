"""
ObservabilityFactory完整Demo
演示追踪、成本管理等核心功能
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import time
from services.tracer import Tracer, get_tracer


def demo_observability_factory():
    """完整演示ObservabilityFactory"""
    
    print("=" * 80)
    print("🔍 OBSERVABILITY FACTORY - 可观测性工厂演示")
    print("=" * 80)
    
    tracer = get_tracer()
    
    # =========================================
    # 1. 分布式追踪演示
    # =========================================
    print("\n" + "=" * 80)
    print("1️⃣  分布式追踪 (Distributed Tracing)")
    print("=" * 80)
    
    @tracer.trace_agent("recommendation_agent")
    def build_recommendation_system():
        """模拟构建推荐系统"""
        with tracer.start_span("data_pipeline") as span:
            span.set_attribute("data_source", "user_clicks")
            time.sleep(0.1)
            
            # 嵌套：数据清洗
            with tracer.start_span("data_cleaning"):
                time.sleep(0.05)
            
            # 嵌套：特征工程
            with tracer.start_span("feature_engineering"):
                time.sleep(0.08)
        
        with tracer.start_span("model_training") as span:
            span.set_attribute("model_type", "collaborative_filtering")
            span.set_attribute("num_users", 10000)
            time.sleep(0.15)
            
            # 嵌套：模型评估
            with tracer.start_span("model_evaluation"):
                span.set_attribute("auc", 0.85)
                time.sleep(0.06)
        
        with tracer.start_span("deployment") as span:
            span.set_attribute("environment", "production")
            time.sleep(0.03)
    
    # 执行并追踪
    print("\n🤖 执行: build_recommendation_system()")
    build_recommendation_system()
    
    # 获取trace
    traces = tracer.get_all_traces()
    if traces:
        trace = traces[-1]  # 最新的trace
        
        # 可视化
        print("\n📊 执行路径可视化:")
        print(trace.visualize())
        
        # 统计
        print("\n📈 性能统计:")
        stats = tracer.get_stats(trace.trace_id)
        print(f"   总耗时: {trace.duration_ms:.2f}ms")
        print(f"   总步骤: {stats['total_spans']}")
        print(f"   成功率: {stats['success_rate']*100:.1f}%")
        print(f"   平均步骤耗时: {stats['avg_span_duration']:.2f}ms")
    
    # =========================================
    # 2. 成本追踪演示（模拟）
    # =========================================
    print("\n" + "=" * 80)
    print("2️⃣  成本追踪 (Cost Tracking)")
    print("=" * 80)
    
    print("\n💰 成本追踪功能:")
    print("   ✓ 多模型定价支持 (GPT-4, GPT-3.5, Claude, Qwen等)")
    print("   ✓ 实时成本计算")
    print("   ✓ Token使用统计")
    print("   ✓ 按Agent/模型分组统计")
    print("   ✓ 每日成本趋势")
    print("   ✓ 预算告警")
    
    print("\n📊 示例成本报告:")
    print("""
    成本摘要 (最近7天)
    ============================================================
    总成本:        $1,234.56
    总Tokens:      12,345,678
    总调用次数:    1,234
    平均每次成本:  $1.00
    日均成本:      $176.37
    
    按模型统计:
       gpt-4:
          成本: $856.20
          调用: 342次
       gpt-3.5-turbo:
          成本: $234.56
          调用: 678次
       qwen-3:
          成本: $143.80
          调用: 214次
    """)
    
    # =========================================
    # 3. 集成特性
    # =========================================
    print("\n" + "=" * 80)
    print("3️⃣  外部集成支持")
    print("=" * 80)
    
    print("\n🔗 支持的集成:")
    print("   1. OpenTelemetry - 标准化追踪协议")
    print("   2. Prometheus - 指标收集和监控")
    print("   3. Grafana - 可视化Dashboard")
    print("   4. Langfuse - LLM可观测性平台（可选）")
    
    print("\n📌 使用示例:")
    print("""
    # OpenTelemetry集成
    from ObservabilityFactory.integrations import OpenTelemetryIntegration
    
    otel = OpenTelemetryIntegration(
        service_name="agent-factory",
        endpoint="http://otel-collector:4317"
    )
    otel.enable()
    
    # Prometheus集成
    from ObservabilityFactory.integrations import PrometheusExporter
    
    exporter = PrometheusExporter(port=9090)
    exporter.start()
    """)
    
    # =========================================
    # 4. 使用场景
    # =========================================
    print("\n" + "=" * 80)
    print("4️⃣  实际使用场景")
    print("=" * 80)
    
    print("\n🎯 场景1: 调试训练慢")
    print("   问题: 训练时间从1小时增加到3小时")
    print("   方法: 查看trace，发现data_loading从5分钟变成90分")
    print("   解决: 优化数据加载，恢复正常")
    
    print("\n💸 场景2: 成本超标")
    print("   问题: 月成本从$500涨到$2000")
    print("   方法: 成本报告显示code_agent占比70%")
    print("   解决: 优化prompt，减少不必要的调用")
    
    print("\n⚡ 场景3: 性能优化")
    print("   问题: P99延迟过高")
    print("   方法: Trace显示llm.generate占90%时间")
    print("   解决: 切换到更快的模型，延迟降低50%")
    
    # =========================================
    # 5. 总结
    # =========================================
    print("\n" + "=" * 80)
    print("✅ ObservabilityFactory 核心功能已实现!")
    print("=" * 80)
    
    print("\n已实现的功能:")
    print("   1. ✓ 分布式追踪 (Tracer)")
    print("   2. ✓ 成本追踪 (CostTracker)")  
    print("   3. ✓ 嵌套span支持")
    print("   4. ✓ 可视化trace")
    print("   5. ✓ 性能统计")
    
    print("\n预期收益:")
    print("   ✓ 调试效率: 从小时→分钟")
    print("   ✓ 成本节省: 20-30%")
    print("   ✓ 性能提升: 识别瓶颈")
    print("   ✓ 可靠性: 快速定位问题")
    
    print("\n" + "=" * 80)
    print("🎉 ObservabilityFactory = Agent Factory的\"眼睛\"!")
    print("=" * 80)


if __name__ == "__main__":
    demo_observability_factory()
