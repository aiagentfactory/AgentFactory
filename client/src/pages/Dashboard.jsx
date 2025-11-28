import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Activity, Database, Globe, Brain, Award, Zap, TrendingUp, AlertCircle } from 'lucide-react';

export default function Dashboard() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    // Mock stats - in production, fetch from API
    setStats({
      totalJobs: 147,
      activeAgents: 23,
      datasetsReady: 8,
      evaluationsPass: 18
    });
  }, []);

  const factories = [
    {
      name: 'Compute Factory',
      path: '/compute',
      icon: Activity,
      color: 'blue',
      description: 'GPU/CPU resource scheduling',
      metric: '85% Utilization'
    },
    {
      name: 'Data Factory',
      path: '/data',
      icon: Database,
      color: 'green',
      description: 'Data collection & annotation',
      metric: '8 Datasets Ready'
    },
    {
      name: 'Environment Factory',
      path: '/environment',
      icon: Globe,
      color: 'purple',
      description: 'Task simulation & testing',
      metric: '12 Scenarios Active'
    },
    {
      name: 'Training Factory',
      path: '/training',
      icon: Brain,
      color: 'orange',
      description: 'Model training & fine-tuning',
      metric: '3 Jobs Running'
    },
    {
      name: 'Evaluation Factory',
      path: '/evaluation',
      icon: Award,
      color: 'pink',
      description: 'Quality & safety evaluation',
      metric: '92% Pass Rate'
    },
    {
      name: 'Runtime Factory',
      path: '/runtime',
      icon: Zap,
      color: 'yellow',
      description: 'Agent deployment & serving',
      metric: '23 Agents Live'
    }
  ];

  return (
    <div className="dashboard animate-fade-in">
      <div className="page-header">
        <h1 className="page-title">Agent Factory Dashboard</h1>
        <p className="page-subtitle">Industrial-grade AI Agent production platform</p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-4" style={{ marginBottom: 'var(--spacing-2xl)' }}>
        <div className="stat-card">
          <div className="stat-label">Total Jobs</div>
          <div className="stat-value">{stats?.totalJobs || '-'}</div>
          <div className="stat-trend positive">
            <TrendingUp size={16} style={{ display: 'inline', marginRight: '4px' }} />
            +12% this week
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-label">Active Agents</div>
          <div className="stat-value">{stats?.activeAgents || '-'}</div>
          <div className="stat-trend positive">
            <TrendingUp size={16} style={{ display: 'inline', marginRight: '4px' }} />
            +8% this week
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-label">Datasets Ready</div>
          <div className="stat-value">{stats?.datasetsReady || '-'}</div>
          <div className="stat-trend">Synced 2h ago</div>
        </div>

        <div className="stat-card">
          <div className="stat-label">Eval Pass Rate</div>
          <div className="stat-value">92%</div>
          <div className="stat-trend positive">
            <TrendingUp size={16} style={{ display: 'inline', marginRight: '4px' }} />
            +5% improvement
          </div>
        </div>
      </div>

      {/* Factory Grid */}
      <div className="grid grid-3">
        {factories.map((factory) => {
          const Icon = factory.icon;
          return (
            <Link
              key={factory.path}
              to={factory.path}
              className="factory-card"
              style={{ textDecoration: 'none' }}
            >
              <div className="factory-icon" data-color={factory.color}>
                <Icon size={32} />
              </div>
              <h3>{factory.name}</h3>
              <p className="factory-description">{factory.description}</p>
              <div className="factory-metric">
                <span className="badge badge-info">{factory.metric}</span>
              </div>
            </Link>
          );
        })}
      </div>

      {/* Quick Actions */}
      <div style={{ marginTop: 'var(--spacing-2xl)' }}>
        <h2 style={{ marginBottom: 'var(--spacing-lg)', fontSize: '1.5rem' }}>Quick Actions</h2>
        <div className="grid grid-4">
          <button className="btn btn-primary">Start Training</button>
          <button className="btn btn-primary">Create Dataset</button>
          <button className="btn btn-primary">Run Evaluation</button>
          <button className="btn btn-primary">Deploy Agent</button>
        </div>
      </div>
    </div>
  );
}