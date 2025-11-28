import React, { useState, useEffect } from 'react';
import { Activity, Cpu, Server, TrendingUp } from 'lucide-react';
import axios from 'axios';

export default function ComputeFactory() {
  const [pools, setPools] = useState([]);
  const [usage, setUsage] = useState(null);
  
  useEffect(() => {
    fetchData();
  }, []);
  
  const fetchData = async () => {
    try {
      const [poolsRes, usageRes] = await Promise.all([
        axios.get('/api/compute/pools'),
        axios.get('/api/compute/usage')
      ]);
      setPools(poolsRes.data.pools || []);
      setUsage(usageRes.data.usage || {});
    } catch (error) {
      console.error('Failed to fetch compute data:', error);
    }
  };
  
  return (
    <div className="compute-factory animate-fade-in">
      <div className="page-header">
        <h1 className="page-title">⚡ Compute Factory</h1>
        <p className="page-subtitle">Unified resource scheduling & orchestration</p>
      </div>
      
      {/* Resource Usage */}
      <div className="grid grid-4">
        <div className="stat-card">
          <div className="stat-label">CPU Usage</div>
          <div className="stat-value">{usage?.cpu_percent?.toFixed(1) || '0'}%</div>
          <div className="stat-trend">
            <Cpu size={16} style={{ display: 'inline', marginRight: '4px' }} />
            {usage?.memory_total_gb?.toFixed(1) || '0'} GB Total
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Memory Usage</div>
          <div className="stat-value">{usage?.memory_percent?.toFixed(1) || '0'}%</div>
          <div className="stat-trend">
            {usage?.memory_used_gb?.toFixed(1) || '0'} / {usage?.memory_total_gb?.toFixed(1) || '0'} GB
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Disk Usage</div>
          <div className="stat-value">{usage?.disk_percent?.toFixed(1) || '0'}%</div>
          <div className="stat-trend">
            {usage?.disk_used_gb?.toFixed(1) || '0'} / {usage?.disk_total_gb?.toFixed(1) || '0'} GB
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Active Jobs</div>
          <div className="stat-value">5</div>
         <div className="stat-trend positive">
            <TrendingUp size={16} style={{ display: 'inline', marginRight: '4px' }} />
            2 Pending
          </div>
        </div>
      </div>
      
      {/* Resource Pools */}
      <div style={{ marginTop: 'var(--spacing-2xl)' }}>
        <h2 style={{ marginBottom: 'var(--spacing-lg)', fontSize: '1.5rem' }}>Resource Pools</h2>
        <div className="grid grid-3">
          {pools.map((pool, idx) => (
            <div key={idx} className="card">
              <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-md)', marginBottom: 'var(--spacing-md)' }}>
                <Server size={24} />
                <div>
                  <h3 style={{ fontSize: '1.1rem' }}>{pool.pool_type}</h3>
                  <p style={{ fontSize: '0.875rem', color: 'var(--color-text-muted)' }}>
                    {pool.active_allocations} / {pool.total_resources} used
                  </p>
                </div>
              </div>
              <div className="progress-bar" style={{ width: '100%', height: '8px', background: 'var(--color-border)', borderRadius: 'var(--radius-sm)', overflow: 'hidden' }}>
                <div style={{ width: `${(pool.active_allocations / Math.max(pool.total_resources, 1)) * 100}%`, height: '100%', background: 'var(--gradient-primary)' }}></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
