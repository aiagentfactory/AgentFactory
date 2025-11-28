import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import {
  Home, Database, Globe, Brain, Award, Zap, Settings,
  LayoutDashboard, Moon, Sun, Activity, Eye // Added Eye icon for Observability
} from 'lucide-react';

// Import design system
import './design-system/index.css';
import './App.css';

// Import factory pages
import Dashboard from './pages/Dashboard';
import ComputeFactory from './pages/factories/ComputeFactory';
import DataFactory from './pages/factories/DataFactory';
import EnvironmentFactory from './pages/factories/EnvironmentFactory';
import TrainingFactory from './pages/factories/TrainingFactory';
import EvaluationFactory from './pages/factories/EvaluationFactory';
import RuntimeFactory from './pages/factories/RuntimeFactory';
import ObservabilityFactory from './pages/factories/ObservabilityFactory'; // Added ObservabilityFactory import

function App() {
  const [theme, setTheme] = useState('dark');

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark');
  };

  return (
    <Router>
      <div className="app">
        <Sidebar toggleTheme={toggleTheme} theme={theme} />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/compute" element={<ComputeFactory />} />
            <Route path="/data" element={<DataFactory />} />
            <Route path="/environment" element={<EnvironmentFactory />} />
            <Route path="/training" element={<TrainingFactory />} />
            <Route path="/evaluation" element={<EvaluationFactory />} />
            <Route path="/runtime" element={<RuntimeFactory />} />
            <Route path="/observability" element={<ObservabilityFactory />} /> {/* Added ObservabilityFactory route */}
          </Routes>
        </main>
      </div>
    </Router>
  );
}

function Sidebar({ toggleTheme, theme }) {
  const location = useLocation();

  const factories = [
    { path: '/', icon: LayoutDashboard, label: 'Dashboard', color: 'cyan' },
    { path: '/compute', icon: Activity, label: 'Compute', color: 'blue' },
    { path: '/data', icon: Database, label: 'Data', color: 'green' },
    { path: '/environment', icon: Globe, label: 'Environment', color: 'purple' },
    { path: '/training', icon: Brain, label: 'Training', color: 'orange' },
    { path: '/evaluation', icon: Award, label: 'Evaluation', color: 'pink' },
    { path: '/runtime', icon: Zap, label: 'Runtime', color: 'yellow' },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h1 className="logo">
          <span className="gradient-text">Agent Factory</span>
        </h1>
        <p className="tagline">From Zero to Agents</p>
      </div>

      <nav className="sidebar-nav">
        {factories.map((factory) => {
          const Icon = factory.icon;
          const isActive = location.pathname === factory.path;

          return (
            <Link
              key={factory.path}
              to={factory.path}
              className={`nav-item ${isActive ? 'active' : ''}`}
              data-color={factory.color}
            >
              <Icon size={20} />
              <span>{factory.label}</span>
            </Link>
          );
        })}
      </nav>

      <div className="sidebar-footer">
        <button className="theme-toggle" onClick={toggleTheme}>
          {theme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
          <span>{theme === 'dark' ? 'Light' : 'Dark'}</span>
        </button>
      </div>
    </aside>
  );
}

export default App;