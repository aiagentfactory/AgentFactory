import React, { useState, useEffect } from 'react';
import { Award, CheckCircle } from 'lucide-react';

const RewardFactory = () => {
  const [models, setModels] = useState([]);
  const [evals, setEvals] = useState([]);
  const [selectedModel, setSelectedModel] = useState('');

  useEffect(() => {
    fetch('http://127.0.0.1:8000/algo/models').then(r => r.json()).then(setModels);
    fetch('http://127.0.0.1:8000/reward/evaluations').then(r => r.json()).then(setEvals);
  }, []);

  const runEval = () => {
      fetch('http://127.0.0.1:8000/reward/evaluations', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ model_id: selectedModel, scenario_id: 1 }) // Hardcoded scenario for MVP
      }).then(r => r.json()).then(ev => {
          setEvals([ev, ...evals]);
      });
  };

  return (
    <div className="page-container">
      <header className="page-header">
        <h1>Reward Factory</h1>
        <p>Evaluate model performance and safety.</p>
      </header>

      <div className="grid-2">
          <div className="card">
              <h3><Award size={18}/> Run Evaluation</h3>
              <div className="form-group">
                  <label>Select Model to Evaluate</label>
                  <select onChange={e => setSelectedModel(e.target.value)}>
                      <option value="">-- Select Model --</option>
                      {models.map(m => <option key={m.id} value={m.id}>{m.name}</option>)}
                  </select>
              </div>
              <button className="btn-primary" onClick={runEval} disabled={!selectedModel}>
                  Run Safety & Performance Eval
              </button>
          </div>

          <div className="card">
              <h3>Evaluation Reports</h3>
              {evals.map(e => (
                  <div key={e.id} style={{padding: '10px', borderBottom: '1px solid #eee'}}>
                      <strong>Eval #{e.id}</strong> - Status: {e.status} <br/>
                      {e.status === 'completed' && (
                          <div style={{color: 'green'}}>
                              Score: {e.score.toFixed(2)} <br/>
                              Safety: {e.report.safety_score}
                          </div>
                      )}
                  </div>
              ))}
          </div>
      </div>
    </div>
  );
};

export default RewardFactory;
