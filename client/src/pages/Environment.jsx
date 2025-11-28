import React, { useState } from 'react';
import api from '../api';

export default function Environment() {
  const [scenarioName, setScenarioName] = useState('');
  const [runLogs, setRunLogs] = useState([]);

  const createScenario = async () => {
    await api.post('/env/scenarios', {
      name: scenarioName,
      type: 'text',
      config: {}
    });
    alert('Scenario Created!');
  };

  const startRun = async () => {
    // Assuming scenario ID 1 for demo
    const res = await api.post('/env/runs?scenario_id=1');
    setRunLogs(prev => [...prev, `Run started: ${res.data.id}`]);
    
    // Simulate a step
    await api.post(`/env/runs/${res.data.id}/step`, { action: "test_action" });
    setRunLogs(prev => [...prev, `Step executed for Run ${res.data.id}`]);
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Environment Factory</h1>
      
      <div className="mb-8 bg-white p-4 rounded shadow">
        <h2 className="text-xl font-semibold mb-2">Create Scenario</h2>
        <input 
          className="border p-2 mr-2 rounded"
          value={scenarioName}
          onChange={e => setScenarioName(e.target.value)}
          placeholder="Scenario Name"
        />
        <button 
          onClick={createScenario}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Create
        </button>
      </div>

      <div className="bg-white p-4 rounded shadow">
        <h2 className="text-xl font-semibold mb-2">Run Simulation</h2>
        <button 
          onClick={startRun}
          className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
        >
          Start Run (Scenario 1)
        </button>
        <div className="mt-4 bg-gray-100 p-4 rounded h-40 overflow-y-auto">
          {runLogs.map((log, i) => <div key={i}>{log}</div>)}
        </div>
      </div>
    </div>
  );
}
