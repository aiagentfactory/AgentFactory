import React, { useState, useEffect } from 'react';
import { Play, CheckCircle, Loader2 } from 'lucide-react';
import './Training.css';

const Training = () => {
  const [activeJob, setActiveJob] = useState(null);
  const [trainingConfig, setTrainingConfig] = useState({
    model_base: 'gpt-2-medium',
    algorithm: 'sft',
    epochs: 3,
    learning_rate: 0.0001
  });
  const [logs, setLogs] = useState([]);
  
  // Poll for job status if a job is active
  useEffect(() => {
    if (!activeJob || activeJob.status === 'completed') return;

    const interval = setInterval(() => {
      fetch(`http://127.0.0.1:8000/algo/train/jobs/${activeJob.id}`)
        .then(res => res.json())
        .then(data => {
            setActiveJob(data);
            // Mock log streaming
            if (data.progress > 0) {
                setLogs(prev => [...prev, `Step ${data.metrics.step || '?'}: Loss ${data.metrics.loss?.toFixed(4) || '...'}`]);
            }
        });
    }, 2000);

    return () => clearInterval(interval);
  }, [activeJob]);

  const startTraining = () => {
    const payload = {
        model_base: trainingConfig.model_base,
        algorithm: trainingConfig.algorithm,
        hyperparams: {
            epochs: trainingConfig.epochs,
            lr: trainingConfig.learning_rate
        }
    };

    fetch('http://127.0.0.1:8000/algo/train/jobs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
        setActiveJob(data);
        setLogs(['Initializing training environment...', 'Allocating Compute Factory resources...']);
    })
    .catch(err => alert('Failed to start training: ' + err));
  };

  return (
    <div className="page-container">
      <header className="page-header">
        <h1>Training Center</h1>
        <p>Train your agents using guided workflows.</p>
      </header>

      <div className="training-grid">
        {/* Left: Configuration Wizard */}
        <div className="card config-card">
            <h3>1. Configure Strategy</h3>
            
            <div className="form-group">
                <label>Base Model</label>
                <select 
                    value={trainingConfig.model_base}
                    onChange={(e) => setTrainingConfig({...trainingConfig, model_base: e.target.value})}
                >
                    <option value="gpt-2-medium">GPT-2 Medium (Fast)</option>
                    <option value="llama-3-8b">Llama 3 8B (High Quality)</option>
                    <option value="mistral-7b">Mistral 7B (Balanced)</option>
                </select>
            </div>

            <div className="form-group">
                <label>Algorithm</label>
                <div className="radio-group">
                    <div 
                        className={`radio-card ${trainingConfig.algorithm === 'sft' ? 'selected' : ''}`}
                        onClick={() => setTrainingConfig({...trainingConfig, algorithm: 'sft'})}
                    >
                        <strong>SFT</strong>
                        <span>Supervised Fine-Tuning</span>
                    </div>
                    <div 
                        className={`radio-card ${trainingConfig.algorithm === 'rft' ? 'selected' : ''}`}
                        onClick={() => setTrainingConfig({...trainingConfig, algorithm: 'rft'})}
                    >
                        <strong>RFT</strong>
                        <span>Reinforcement Tuning</span>
                    </div>
                </div>
            </div>

            <div className="form-group">
                <label>Training Intensity (Epochs): {trainingConfig.epochs}</label>
                <input 
                    type="range" 
                    min="1" max="10" 
                    value={trainingConfig.epochs} 
                    onChange={(e) => setTrainingConfig({...trainingConfig, epochs: parseInt(e.target.value)})} 
                />
            </div>

            <button 
                className="btn-primary" 
                onClick={startTraining}
                disabled={activeJob && activeJob.status !== 'completed'}
            >
                {activeJob && activeJob.status === 'training' ? (
                    <><Loader2 className="spin" size={18}/> Training...</>
                ) : (
                    <><Play size={18}/> Start Training Job</>
                )}
            </button>
        </div>

        {/* Right: Status & Logs */}
        <div className="card status-card">
            <h3>2. Real-time Monitor</h3>
            
            {!activeJob ? (
                <div className="empty-state">
                    <p>Select a strategy and click Start to begin training.</p>
                </div>
            ) : (
                <div className="monitor-content">
                    <div className="progress-section">
                        <div className="progress-labels">
                            <span>Status: <strong>{activeJob.status.toUpperCase()}</strong></span>
                            <span>{activeJob.progress}%</span>
                        </div>
                        <div className="progress-bar-bg">
                            <div 
                                className="progress-bar-fill" 
                                style={{width: `${activeJob.progress}%`}}
                            ></div>
                        </div>
                    </div>

                    <div className="logs-console">
                        {logs.map((log, i) => (
                            <div key={i} className="log-line">{log}</div>
                        ))}
                        {activeJob.status === 'completed' && (
                             <div className="log-line success">
                                <CheckCircle size={14}/> Training Successfully Completed!
                             </div>
                        )}
                    </div>
                </div>
            )}
        </div>
      </div>
    </div>
  );
};

export default Training;
