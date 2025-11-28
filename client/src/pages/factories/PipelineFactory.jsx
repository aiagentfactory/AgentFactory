import React, { useState, useEffect } from 'react';
import { Workflow, Play, CheckCircle, Loader } from 'lucide-react';

const PipelineFactory = () => {
  const [datasets, setDatasets] = useState([]);
  const [scenarios, setScenarios] = useState([]);
  const [runs, setRuns] = useState([]);
  
  const [newPipe, setNewPipe] = useState({
      name: '',
      dataset_id: '',
      algorithm: 'sft',
      scenario_id: ''
  });

  useEffect(() => {
    fetch('http://127.0.0.1:8000/data/datasets').then(r => r.json()).then(setDatasets);
    fetch('http://127.0.0.1:8000/env/scenarios').then(r => r.json()).then(setScenarios);
    
    const loadRuns = () => {
        fetch('http://127.0.0.1:8000/pipeline/runs').then(r => r.json()).then(setRuns);
    };
    loadRuns();
    const interval = setInterval(loadRuns, 2000); // Polling for status updates
    return () => clearInterval(interval);
  }, []);

  const startPipeline = () => {
      fetch('http://127.0.0.1:8000/pipeline/runs', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify(newPipe)
      }).then(r => r.json()).then(() => {
         // Runs will update via polling
         setNewPipe({...newPipe, name: ''});
      });
  };

  return (
    <div className="page-container">
      <header className="page-header">
        <h1>Pipeline Factory</h1>
        <p>Automate the End-to-End Agent Lifecycle.</p>
      </header>

      <div className="grid-2">
          <div className="card">
              <h3><Workflow size={18}/> Design Pipeline</h3>
              <div className="form-group">
                  <label>Pipeline Name</label>
                  <input type="text" value={newPipe.name} onChange={e => setNewPipe({...newPipe, name: e.target.value})} placeholder="e.g., V2 Release Candidate" />
              </div>
              
              <div className="form-group">
                  <label>Step 1: Data Source</label>
                  <select onChange={e => setNewPipe({...newPipe, dataset_id: e.target.value})}>
                      <option value="">-- Select Dataset --</option>
                      {datasets.map(d => <option key={d.id} value={d.id}>{d.name}</option>)}
                  </select>
              </div>

              <div className="form-group">
                  <label>Step 2: Algorithm</label>
                  <select onChange={e => setNewPipe({...newPipe, algorithm: e.target.value})}>
                      <option value="sft">Supervised Finetuning (SFT)</option>
                      <option value="ppo">Reinforcement Learning (PPO)</option>
                  </select>
              </div>

              <div className="form-group">
                  <label>Step 3: Eval Scenario</label>
                  <select onChange={e => setNewPipe({...newPipe, scenario_id: e.target.value})}>
                      <option value="">-- Select Scenario --</option>
                      {scenarios.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
                  </select>
              </div>

              <button className="btn-primary" onClick={startPipeline}>Run Pipeline</button>
          </div>

          <div className="card">
              <h3>Active Pipelines</h3>
              {runs.map(run => (
                  <div key={run.id} style={{border: '1px solid #eee', borderRadius: '8px', padding: '15px', marginBottom: '10px'}}>
                      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                          <strong>{run.name}</strong>
                          <span style={{
                              padding: '4px 8px', 
                              borderRadius: '12px', 
                              background: run.status === 'completed' ? '#dcfce7' : '#e0e7ff',
                              color: run.status === 'completed' ? '#166534' : '#3730a3',
                              fontSize: '0.8rem',
                              display: 'flex',
                              alignItems: 'center',
                              gap: '5px'
                          }}>
                              {run.status === 'running' && <Loader size={12} className="animate-spin"/>}
                              {run.status === 'completed' && <CheckCircle size={12}/>}
                              {run.status}
                          </span>
                      </div>
                      <div style={{marginTop: '10px', color: '#6b7280', fontSize: '0.9rem'}}>
                          Current Stage: <strong>{run.current_stage}</strong>
                      </div>
                      
                      {run.artifacts && (
                          <div style={{marginTop: '10px', fontSize: '0.8rem', background: '#f9fafb', padding: '8px', borderRadius: '4px'}}>
                              <div>Job ID: {run.artifacts.job_id || '-'}</div>
                              <div>Model ID: {run.artifacts.model_id || '-'}</div>
                              <div>Eval ID: {run.artifacts.eval_id || '-'}</div>
                              <div>Agent ID: {run.artifacts.agent_id || '-'}</div>
                          </div>
                      )}
                  </div>
              ))}
          </div>
      </div>
    </div>
  );
};

export default PipelineFactory;
