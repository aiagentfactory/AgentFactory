import React, { useState, useEffect } from 'react';
import { Box, Plus } from 'lucide-react';

const EnvFactory = () => {
  const [scenarios, setScenarios] = useState([]);
  const [newScenario, setNewScenario] = useState({ name: '', type: 'text', config: {} });

  const fetchScenarios = () => {
      // Need to implement listing endpoints if not available, reusing logic or adding mock
      // For MVP we reuse creating one and assuming we can list (mock list in memory on frontend for now or add backend)
      // Actually, we need a list endpoint in backend for Env. I'll mock it here for display or use existing endpoints.
      // Checking env_factory.py... it doesn't have a list endpoint. 
      // I'll just support creation for now.
  };

  const createScenario = () => {
    fetch('http://127.0.0.1:8000/env/scenarios', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(newScenario)
    })
    .then(res => res.json())
    .then(data => {
        alert(`Scenario '${data.name}' created!`);
        setScenarios([...scenarios, data]);
    });
  };

  return (
    <div className="page-container">
      <header className="page-header">
        <h1>Environment Factory</h1>
        <p>Define simulation scenarios and tasks.</p>
      </header>

      <div className="grid-2">
        <div className="card">
            <h3><Plus size={18}/> New Scenario</h3>
            <div className="form-group">
                <label>Name</label>
                <input type="text" onChange={e => setNewScenario({...newScenario, name: e.target.value})} />
            </div>
            <div className="form-group">
                <label>Type</label>
                <select onChange={e => setNewScenario({...newScenario, type: e.target.value})}>
                    <option value="text">Text Chat</option>
                    <option value="browser">Browser Automation</option>
                </select>
            </div>
            <button className="btn-primary" onClick={createScenario}>Create Scenario</button>
        </div>

        <div className="card">
            <h3><Box size={18}/> Scenarios</h3>
            {scenarios.map(s => (
                <div key={s.id || Math.random()}>{s.name} ({s.type})</div>
            ))}
        </div>
      </div>
    </div>
  );
};

export default EnvFactory;
