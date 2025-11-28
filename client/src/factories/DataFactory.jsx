import React, { useState, useEffect } from 'react';
import { Database, FileText, CheckCircle } from 'lucide-react';
import axios from 'axios';

export default function DataFactory() {
  const [datasets, setDatasets] = useState([]);
  const [stats, setStats] = useState(null);
  
  useEffect(() => {
    fetchData();
  }, []);
  
  const fetchData = async () => {
    try {
      const [datasetsRes, statsRes] = await Promise.all([
        axios.get('/api/data/datasets'),
        axios.get('/api/data/events/statistics')
      ]);
      setDatasets(datasetsRes.data.datasets || []);
      setStats(statsRes.data || {});
    } catch (error) {
      console.error('Failed to fetch data:', error);
    }
  };
  
  return (
    <div className="data-factory animate-fade-in">
      <div className="page-header">
        <h1 className="page-title">🗃️ Data Factory</h1>
        <p className="page-subtitle">Data collection, cleaning & annotation</p>
      </div>
      
      {/* Stats */}
      <div className="grid grid-4">
        <div className="stat-card">
          <div className="stat-label">Total Events</div>
          <div className="stat-value">{stats?.total_events || 0}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Datasets</div>
          <div className="stat-value">{datasets.length}</div>
          <div className="stat-trend">{datasets.filter(d => d.status === 'ready').length} ready</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Annotations</div>
          <div className="stat-value">1,247</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Quality Score</div>
          <div className="stat-value">94%</div>
        </div>
      </div>
      
      {/* Datasets List */}
      <div style={{ marginTop: 'var(--spacing-2xl)' }}>
        <h2 style={{ marginBottom: 'var(--spacing-lg)', fontSize: '1.5rem' }}>Datasets</h2>
        <div className="grid grid-2">
          {datasets.length === 0 && (
            <div className="card">
              <p style={{ textAlign: 'center', color: 'var(--color-text-muted)' }}>No datasets yet. Create your first dataset to get started.</p>
            </div>
          )}
          {datasets.map((dataset, idx) => (
            <div key={idx} className="card">
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 'var(--spacing-sm)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-sm)' }}>
                  <FileText size={20} />
                  <h3>{dataset.name}</h3>
                </div>
                <span className={`badge badge-${dataset.status === 'ready' ? 'success' : 'warning'}`}>
                  {dataset.status}
                </span>
              </div>
              <p style={{ fontSize: '0.875rem', color: 'var(--color-text-muted)', marginBottom: 'var(--spacing-sm)' }}>
                Type: {dataset.dataset_type} • Version: {dataset.version}
              </p>
              <p style={{ fontSize: '0.875rem' }}>
                {dataset.size} events
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
