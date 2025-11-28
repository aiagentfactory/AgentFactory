import React, { useState, useEffect } from 'react';
import { Server, Cpu, Activity } from 'lucide-react';

const ComputeFactory = () => {
  const [nodes, setNodes] = useState([]);
  const [newNode, setNewNode] = useState({ name: '', type: 'gpu' });

  useEffect(() => {
    fetch('http://127.0.0.1:8000/compute/nodes').then(r => r.json()).then(setNodes);
  }, []);

  const addNode = () => {
    fetch('http://127.0.0.1:8000/compute/nodes', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(newNode)
    }).then(r => r.json()).then(n => setNodes([...nodes, n]));
  };

  return (
    <div className="page-container">
      <header className="page-header">
        <h1>Compute Factory</h1>
        <p>Manage compute clusters and resources.</p>
      </header>

      <div className="grid-2">
          <div className="card">
              <h3><Server size={18}/> Provision Resource</h3>
              <div className="form-group">
                  <label>Node Name</label>
                  <input type="text" onChange={e => setNewNode({...newNode, name: e.target.value})} />
              </div>
              <div className="form-group">
                  <label>Type</label>
                  <select onChange={e => setNewNode({...newNode, type: e.target.value})}>
                      <option value="gpu">GPU Node (H100)</option>
                      <option value="cpu">CPU Node (x86)</option>
                  </select>
              </div>
              <button className="btn-primary" onClick={addNode}>Provision Node</button>
          </div>

          <div className="card">
              <h3>Cluster Status</h3>
              <div style={{display: 'flex', flexWrap: 'wrap', gap: '10px'}}>
                  {nodes.map(n => (
                      <div key={n.id} style={{
                          border: '1px solid #e5e7eb', 
                          padding: '15px', 
                          borderRadius: '8px',
                          width: '100px',
                          textAlign: 'center'
                      }}>
                          {n.type === 'gpu' ? <Activity color="#4f46e5"/> : <Cpu color="#10b981"/>}
                          <div style={{marginTop: '5px', fontWeight: 'bold'}}>{n.name}</div>
                          <small>{n.status}</small>
                      </div>
                  ))}
              </div>
          </div>
      </div>
    </div>
  );
};

export default ComputeFactory;
