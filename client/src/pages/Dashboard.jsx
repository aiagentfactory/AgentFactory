import React, { useState, useEffect } from 'react';
import { Activity, Users, Server } from 'lucide-react';

const Dashboard = () => {
  const [status, setStatus] = useState({ msg: 'Connecting...', online: false });
  const [stats, setStats] = useState({ agents: 0, events: 0 });

  useEffect(() => {
    fetch('http://127.0.0.1:8000/')
      .then(res => res.json())
      .then(data => setStatus({ msg: 'Online', online: true }))
      .catch(() => setStatus({ msg: 'Offline', online: false }));

    fetch('http://127.0.0.1:8000/runtime/agents')
        .then(res => res.json())
        .then(data => setStats(prev => ({ ...prev, agents: data.length })));
    
    fetch('http://127.0.0.1:8000/data/events')
        .then(res => res.json())
        .then(data => setStats(prev => ({ ...prev, events: data.length })));
  }, []);

  const cards = [
    { label: 'System Status', value: status.msg, icon: <Activity />, color: status.online ? 'text-green-600' : 'text-red-600' },
    { label: 'Active Agents', value: stats.agents, icon: <Users />, color: 'text-blue-600' },
    { label: 'Data Events', value: stats.events, icon: <Server />, color: 'text-purple-600' },
  ];

  return (
    <div className="page-container">
      <header className="page-header">
        <h1>Dashboard</h1>
        <p>Overview of your Agent Factory ecosystem.</p>
      </header>

      <div className="dashboard-stats">
        {cards.map((c, i) => (
            <div key={i} className="stat-card">
                <div className={`icon-wrapper ${c.color}`}>{c.icon}</div>
                <div className="stat-info">
                    <span className="stat-label">{c.label}</span>
                    <span className="stat-value">{c.value}</span>
                </div>
            </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
