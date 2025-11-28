import React, { useState, useEffect } from 'react';
import { FileText, Box, Plus } from 'lucide-react';
import './DataEnv.css';

const DataEnv = () => {
  const [events, setEvents] = useState([]);
  const [newScenario, setNewScenario] = useState({ name: '', type: 'text', config: {} });

  useEffect(() => {
    // Fetch recent data events
    fetch('http://127.0.0.1:8000/data/events?limit=10')
      .then(res => res.json())
      .then(setEvents)
      .catch(console.error);
  }, []);

  const createScenario = () => {
    if (!newScenario.name) return;
    
    fetch('http://127.0.0.1:8000/env/scenarios', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(newScenario)
    })
    .then(res => res.json())
    .then(data => {
        alert(`Scenario '${data.name}' created!`);
        setNewScenario({ name: '', type: 'text', config: {} });
    })
    .catch(err => alert('Error: ' + err));
  };

  return (
    <div className="page-container">
        <header className="page-header">
            <h1>Data & Environment Factory</h1>
            <p>Manage datasets, events, and simulation environments.</p>
        </header>

        <div className="grid-2">
            <section className="card">
                <h3><Box size={18}/> Environment Scenarios</h3>
                <div className="create-box">
                    <input 
                        type="text" 
                        placeholder="Scenario Name (e.g., 'CustomerSupport_L1')" 
                        value={newScenario.name}
                        onChange={e => setNewScenario({...newScenario, name: e.target.value})}
                    />
                    <select 
                        value={newScenario.type}
                        onChange={e => setNewScenario({...newScenario, type: e.target.value})}
                    >
                        <option value="text">Text Completion</option>
                        <option value="browser">Web Browser</option>
                        <option value="api">API Tool Use</option>
                    </select>
                    <button className="btn-secondary" onClick={createScenario}>
                        <Plus size={16}/> Create
                    </button>
                </div>
                <div className="list-placeholder">
                    <p>No complex scenarios configured yet. Use the form above to create one.</p>
                </div>
            </section>

            <section className="card">
                <h3><FileText size={18}/> Recent Data Events</h3>
                <div className="events-list">
                    {events.length === 0 ? (
                        <p className="empty-text">No events logged yet.</p>
                    ) : (
                        events.map(ev => (
                            <div key={ev.id} className="event-item">
                                <span className="badge">{ev.event_type}</span>
                                <span className="date">{new Date(ev.timestamp).toLocaleTimeString()}</span>
                                <pre>{JSON.stringify(ev.content).substring(0, 50)}...</pre>
                            </div>
                        ))
                    )}
                </div>
            </section>
        </div>
    </div>
  );
};

export default DataEnv;
