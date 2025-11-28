/**
 * ObservabilityFactory监控页面
 * 实时展示追踪、性能指标和成本分析
 */

import React, { useState, useEffect } from 'react';
import { observabilityApi } from '../api';
import './ObservabilityFactory.css';

const ObservabilityFactory = () => {
    const [activeTab, setActiveTab] = useState('traces');
    const [traces, setTraces] = useState([]);
    const [metrics, setMetrics] = useState(null);
    const [costs, setCosts] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadData();
        const interval = setInterval(loadData, 5000); // 每5秒刷新
        return () => clearInterval(interval);
    }, [activeTab]);

    const loadData = async () => {
        try {
            setLoading(true);

            switch (activeTab) {
                case 'traces':
                    const tracesData = await observabilityApi.listTraces();
                    setTraces(tracesData || generateMockTraces());
                    break;

                case 'metrics':
                    const metricsData = await observabilityApi.getMetrics();
                    setMetrics(metricsData || generateMockMetrics());
                    break;

                case 'costs':
                    const costsData = await observabilityApi.getCostReport({ days: 7 });
                    setCosts(costsData || generateMockCosts());
                    break;
            }

            setLoading(false);
        } catch (error) {
            console.error('Error loading observability data:', error);
            // 使用mock数据
            if (activeTab === 'traces') setTraces(generateMockTraces());
            if (activeTab === 'metrics') setMetrics(generateMockMetrics());
            if (activeTab === 'costs') setCosts(generateMockCosts());
            setLoading(false);
        }
    };

    const generateMockTraces = () => [
        {
            trace_id: 'trace_001',
            name: 'train_agent',
            duration_ms: 1234.56,
            timestamp: Date.now() - 300000,
            status: 'OK',
            agent_id: 'code_agent'
        },
        {
            trace_id: 'trace_002',
            name: 'evaluate_model',
            duration_ms: 567.89,
            timestamp: Date.now() - 600000,
            status: 'OK',
            agent_id: 'eval_agent'
        },
        {
            trace_id: 'trace_003',
            name: 'generate_code',
            duration_ms: 2345.67,
            timestamp: Date.now() - 900000,
            status: 'ERROR',
            agent_id: 'code_agent'
        }
    ];

    const generateMockMetrics = () => ({
        agents: {
            code_agent: {
                total_calls: 245,
                avg_latency_ms: 234.5,
                p95_latency_ms: 456.7,
                p99_latency_ms: 789.0,
                success_rate: 0.95
            },
            chat_agent: {
                total_calls: 1234,
                avg_latency_ms: 123.4,
                p95_latency_ms: 234.5,
                p99_latency_ms: 345.6,
                success_rate: 0.98
            },
            search_agent: {
                total_calls: 567,
                avg_latency_ms: 345.6,
                p95_latency_ms: 567.8,
                p99_latency_ms: 678.9,
                success_rate: 0.92
            }
        }
    });

    const generateMockCosts = () => ({
        total_cost_usd: 1234.56,
        by_agent: {
            code_agent: 456.78,
            chat_agent: 345.67,
            search_agent: 234.56,
            eval_agent: 197.55
        },
        daily_breakdown: {
            '2024-11-28': 176.37,
            '2024-11-27': 182.45,
            '2024-11-26': 165.23,
            '2024-11-25': 198.76,
            '2024-11-24': 155.89,
            '2024-11-23': 189.34,
            '2024-11-22': 166.52
        }
    });

    const renderTraces = () => (
        <div className="traces-section">
            <div className="section-header">
                <h2>🔍 分布式追踪</h2>
                <span className="trace-count">{traces.length} traces</span>
            </div>

            <div className="traces-list">
                {traces.map(trace => (
                    <div key={trace.trace_id} className={`trace-card ${trace.status.toLowerCase()}`}>
                        <div className="trace-header">
                            <span className="trace-name">{trace.name}</span>
                            <span className={`trace-status ${trace.status.toLowerCase()}`}>
                                {trace.status === 'OK' ? '✓' : '✗'} {trace.status}
                            </span>
                        </div>

                        <div className="trace-details">
                            <div className="trace-detail">
                                <span className="label">Trace ID:</span>
                                <span className="value">{trace.trace_id}</span>
                            </div>
                            <div className="trace-detail">
                                <span className="label">Duration:</span>
                                <span className="value">{trace.duration_ms.toFixed(2)}ms</span>
                            </div>
                            <div className="trace-detail">
                                <span className="label">Agent:</span>
                                <span className="value">{trace.agent_id}</span>
                            </div>
                            <div className="trace-detail">
                                <span className="label">Time:</span>
                                <span className="value">{new Date(trace.timestamp).toLocaleString()}</span>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );

    const renderMetrics = () => (
        <div className="metrics-section">
            <div className="section-header">
                <h2>📊 性能指标</h2>
            </div>

            {metrics && (
                <div className="metrics-grid">
                    {Object.entries(metrics.agents).map(([agentId, stats]) => (
                        <div key={agentId} className="metric-card">
                            <div className="metric-header">
                                <h3>🤖 {agentId}</h3>
                                <span className="success-rate">
                                    {(stats.success_rate * 100).toFixed(1)}% success
                                </span>
                            </div>

                            <div className="metric-stats">
                                <div className="stat">
                                    <span className="stat-label">Total Calls</span>
                                    <span className="stat-value">{stats.total_calls.toLocaleString()}</span>
                                </div>
                                <div className="stat">
                                    <span className="stat-label">Avg Latency</span>
                                    <span className="stat-value">{stats.avg_latency_ms.toFixed(1)}ms</span>
                                </div>
                                <div className="stat">
                                    <span className="stat-label">P95 Latency</span>
                                    <span className="stat-value">{stats.p95_latency_ms.toFixed(1)}ms</span>
                                </div>
                                <div className="stat">
                                    <span className="stat-label">P99 Latency</span>
                                    <span className="stat-value">{stats.p99_latency_ms.toFixed(1)}ms</span>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );

    const renderCosts = () => (
        <div className="costs-section">
            <div className="section-header">
                <h2>💰 成本分析</h2>
            </div>

            {costs && (
                <>
                    <div className="cost-summary">
                        <div className="summary-card total">
                            <span className="summary-label">Total Cost (7 days)</span>
                            <span className="summary-value">${costs.total_cost_usd.toFixed(2)}</span>
                        </div>
                        <div className="summary-card avg">
                            <span className="summary-label">Daily Average</span>
                            <span className="summary-value">
                                ${(costs.total_cost_usd / 7).toFixed(2)}
                            </span>
                        </div>
                    </div>

                    <div className="cost-breakdown">
                        <h3>By Agent</h3>
                        <div className="agent-costs">
                            {Object.entries(costs.by_agent)
                                .sort((a, b) => b[1] - a[1])
                                .map(([agent, cost]) => (
                                    <div key={agent} className="agent-cost-item">
                                        <span className="agent-name">{agent}</span>
                                        <div className="cost-bar-wrapper">
                                            <div
                                                className="cost-bar"
                                                style={{
                                                    width: `${(cost / costs.total_cost_usd * 100)}%`
                                                }}
                                            ></div>
                                            <span className="cost-amount">${cost.toFixed(2)}</span>
                                        </div>
                                        <span className="cost-percent">
                                            {(cost / costs.total_cost_usd * 100).toFixed(1)}%
                                        </span>
                                    </div>
                                ))}
                        </div>
                    </div>

                    <div className="cost-trend">
                        <h3>Daily Trend</h3>
                        <div className="trend-chart">
                            {Object.entries(costs.daily_breakdown).map(([date, cost]) => (
                                <div key={date} className="trend-bar-wrapper">
                                    <span className="trend-date">{date.substring(5)}</span>
                                    <div
                                        className="trend-bar"
                                        style={{ height: `${(cost / 200 * 100)}%` }}
                                        title={`$${cost.toFixed(2)}`}
                                    >
                                        <span className="trend-value">${cost.toFixed(0)}</span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </>
            )}
        </div>
    );

    return (
        <div className="observability-factory">
            <div className="page-header">
                <h1>👁️ ObservabilityFactory - 可观测性工厂</h1>
                <p className="page-description">
                    实时追踪、性能监控和成本管理
                </p>
            </div>

            <div className="tabs">
                <button
                    className={`tab ${activeTab === 'traces' ? 'active' : ''}`}
                    onClick={() => setActiveTab('traces')}
                >
                    🔍 Traces
                </button>
                <button
                    className={`tab ${activeTab === 'metrics' ? 'active' : ''}`}
                    onClick={() => setActiveTab('metrics')}
                >
                    📊 Metrics
                </button>
                <button
                    className={`tab ${activeTab === 'costs' ? 'active' : ''}`}
                    onClick={() => setActiveTab('costs')}
                >
                    💰 Costs
                </button>
            </div>

            <div className="tab-content">
                {loading ? (
                    <div className="loading">Loading...</div>
                ) : (
                    <>
                        {activeTab === 'traces' && renderTraces()}
                        {activeTab === 'metrics' && renderMetrics()}
                        {activeTab === 'costs' && renderCosts()}
                    </>
                )}
            </div>
        </div>
    );
};

export default ObservabilityFactory;
