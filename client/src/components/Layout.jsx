import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, Database, Box, BrainCircuit, Award, Server, MessageSquare } from 'lucide-react';
import './Layout.css';

const Layout = ({ children }) => {
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Dashboard', icon: <LayoutDashboard size={20} /> },
    { path: '/factory/data', label: 'Data Factory', icon: <Database size={20} /> },
    { path: '/factory/env', label: 'Environment Factory', icon: <Box size={20} /> },
    { path: '/factory/algo', label: 'Algorithm Factory', icon: <BrainCircuit size={20} /> },
    { path: '/factory/reward', label: 'Reward Factory', icon: <Award size={20} /> },
    { path: '/factory/compute', label: 'Compute Factory', icon: <Server size={20} /> },
    { path: '/factory/runtime', label: 'Runtime Factory', icon: <MessageSquare size={20} /> },
  ];

  return (
    <div className="layout-container">
      <aside className="sidebar">
        <div className="brand">
          <h2>Agent Factory</h2>
          <span className="version">v2.0</span>
        </div>
        <nav>
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`nav-item ${location.pathname === item.path ? 'active' : ''}`}
            >
              {item.icon}
              <span>{item.label}</span>
            </Link>
          ))}
        </nav>
        <div className="sidebar-footer">
            <div className="user-info">
                <div className="avatar">U</div>
                <span>User Workspace</span>
            </div>
        </div>
      </aside>
      <main className="main-content">
        {children}
      </main>
    </div>
  );
};

export default Layout;
