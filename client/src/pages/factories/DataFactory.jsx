import React, { useState, useEffect } from 'react';
import { Database, Plus, FileText } from 'lucide-react';

const DataFactory = () => {
  const [events, setEvents] = useState([]);
  const [datasets, setDatasets] = useState([]);
  const [newDataset, setNewDataset] = useState({ name: '', description: '' });

  useEffect(() => {
    fetch('http://127.0.0.1:8000/data/events').then(r => r.json()).then(setEvents);
    fetch('http://127.0.0.1:8000/data/datasets').then(r => r.json()).then(setDatasets);
  }, []);

  const createDataset = () => {
    fetch('http://127.0.0.1:8000/data/datasets', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newDataset)
    }).then(r => r.json()).then(ds => {
      setDatasets([...datasets, ds]);
      setNewDataset({ name: '', description: '' });
    });
  };

  return (
    <div className="page-container">
      <header className="page-header">
        <h1>Data Factory</h1>
        <p>Ingest events and curate datasets for training.</p>
      </header>

      <div className="grid-2">
        <div className="card">
          <h3><Plus size={18}/> Create Dataset from Events</h3>
          <div className="form-group">
            <label>Dataset Name</label>
            <input 
                type="text" 
                value={newDataset.name} 
                onChange={e => setNewDataset({...newDataset, name: e.target.value})} 
            />
          </div>
          <div className="form-group">
            <label>Description</label>
            <input 
                type="text" 
                value={newDataset.description} 
                onChange={e => setNewDataset({...newDataset, description: e.target.value})} 
            />
          </div>
          <button className="btn-primary" onClick={createDataset}>Snapshot Current Events</button>
        </div>

        <div className="card">
            <h3><Database size={18}/> Available Datasets</h3>
            <ul>
                {datasets.map(ds => (
                    <li key={ds.id} style={{marginBottom: '10px', borderBottom: '1px solid #eee', paddingBottom: '5px'}}>
                        <strong>{ds.name}</strong> <br/>
                        <small>{ds.description}</small> <br/>
                        <small>Events: {ds.event_count}</small>
                    </li>
                ))}
            </ul>
        </div>
      </div>
      
      <div className="card" style={{marginTop: '20px'}}>
        <h3><FileText size={18}/> Event Stream</h3>
        <div style={{maxHeight: '300px', overflowY: 'auto'}}>
            {events.slice(0, 20).map(ev => (
                <div key={ev.id} style={{fontSize: '0.85rem', borderBottom: '1px solid #eee', padding: '5px 0'}}>
                    [{ev.event_type}] {JSON.stringify(ev.content)}
                </div>
            ))}
        </div>
      </div>
    </div>
  );
};

export default DataFactory;
