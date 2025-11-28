import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, BrainCircuit, MessageSquare, Database, Settings } from 'lucide-react';
import './Layout.css';

const Layout = ({ children }) => {
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Dashboard', icon: <LayoutDashboard size={20} /> },
    { path: '/training', label: 'Training Center', icon: <BrainCircuit size={20} /> },
    { path: '/data', label: 'Data & Scenarios', icon: <Database size={20} /> },
    { path: '/playground', label: 'Agent Playground', icon: <MessageSquare size={20} /> },
  ];

  return (
    <div className="layout-container">
      <aside className="sidebar">
        <div className="brand">
          <h2>Agent Factory</h2>
          <span className="version">v1.0</span>
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
