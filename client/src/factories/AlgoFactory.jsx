import React, { useState, useEffect } from 'react';
import { BrainCircuit, Play, Loader2, Box } from 'lucide-react';

const AlgoFactory = () => {
  const [datasets, setDatasets] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [models, setModels] = useState([]);
  const [config, setConfig] = useState({ dataset_id: '', model_base: 'gpt-2', algorithm: 'sft', epochs: 3 });

  useEffect(() => {
    fetch('http://127.0.0.1:8000/data/datasets').then(r => r.json()).then(setDatasets);
    fetch('http://127.0.0.1:8000/algo/train/jobs').then(r => r.json()).then(setJobs);
    fetch('http://127.0.0.1:8000/algo/models').then(r => r.json()).then(setModels);
  }, []);

  const startTraining = () => {
    fetch('http://127.0.0.1:8000/algo/train/jobs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(config)
    }).then(r => r.json()).then(job => {
        setJobs([job, ...jobs]);
    });
  };

  return (
    <div className="page-container">
      <header className="page-header">
        <h1>Algorithm Factory</h1>
        <p>Train models using datasets and specific algorithms.</p>
      </header>

      <div className="grid-2">
        <div className="card">
            <h3><Play size={18}/> Configure Training Job</h3>
            <div className="form-group">
                <label>Select Dataset</label>
                <select onChange={e => setConfig({...config, dataset_id: e.target.value})}>
                    <option value="">-- Select --</option>
                    {datasets.map(d => <option key={d.id} value={d.id}>{d.name}</option>)}
                </select>
            </div>
            <div className="form-group">
                <label>Algorithm</label>
                <select onChange={e => setConfig({...config, algorithm: e.target.value})}>
                    <option value="sft">SFT</option>
                    <option value="rft">RFT</option>
                    <option value="ppo">PPO</option>
                </select>
            </div>
            <button className="btn-primary" onClick={startTraining}>Start Training</button>
        </div>

        <div className="card">
            <h3><BrainCircuit size={18}/> Training Jobs</h3>
            <div style={{maxHeight: '300px', overflowY: 'auto'}}>
                {jobs.map(job => (
                    <div key={job.id} style={{borderBottom: '1px solid #eee', padding: '10px'}}>
                        <strong>Job #{job.id}</strong> ({job.status}) <br/>
                        <small>Algo: {job.algorithm} | Progress: {job.progress}%</small>
                    </div>
                ))}
            </div>
        </div>
      </div>

      <div className="card" style={{marginTop: '20px'}}>
          <h3><Box size={18}/> Generated Models</h3>
          <ul>
              {models.map(m => (
                  <li key={m.id}>
                      <strong>{m.name}</strong> (v{m.version}) - Source Job: #{m.source_job_id}
                  </li>
              ))}
          </ul>
      </div>
    </div>
  );
};

export default AlgoFactory;
