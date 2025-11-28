import React, { useState } from 'react';
import api from '../api';

export default function Algorithm() {
  const [jobStatus, setJobStatus] = useState(null);

  const startTraining = async () => {
    const res = await api.post('/algo/train/jobs', {
      model_base: "llama-2-7b",
      algorithm: "ppo",
      hyperparams: { lr: 0.001 }
    });
    setJobStatus(res.data);
    pollStatus(res.data.id);
  };

  const pollStatus = (id) => {
    const interval = setInterval(async () => {
      const res = await api.get(`/algo/train/jobs/${id}`);
      setJobStatus(res.data);
      if (res.data.status === 'completed') clearInterval(interval);
    }, 1000);
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Algorithm Factory</h1>
      <div className="bg-white p-6 rounded shadow">
        <h2 className="text-xl font-semibold mb-4">Training Control</h2>
        <button 
          onClick={startTraining}
          className="bg-purple-500 text-white px-4 py-2 rounded hover:bg-purple-600"
        >
          Start SFT Job
        </button>

        {jobStatus && (
          <div className="mt-6">
            <p><strong>Job ID:</strong> {jobStatus.id}</p>
            <p><strong>Status:</strong> <span className={`font-bold ${jobStatus.status === 'completed' ? 'text-green-600' : 'text-yellow-600'}`}>{jobStatus.status}</span></p>
            <p><strong>Progress:</strong> {jobStatus.progress}%</p>
            <div className="w-full bg-gray-200 rounded-full h-2.5 mt-2">
              <div className="bg-purple-600 h-2.5 rounded-full" style={{ width: `${jobStatus.progress}%` }}></div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
