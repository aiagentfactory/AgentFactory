import React from 'react';

export default function Dashboard() {
  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Factory Overview</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-2">Data Factory</h2>
          <p className="text-gray-600">Ingest events and manage datasets.</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-2">Environment Factory</h2>
          <p className="text-gray-600">Run simulations and generate trajectories.</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-2">Algorithm Factory</h2>
          <p className="text-gray-600">Train and refine agent models.</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-2">Reward Factory</h2>
          <p className="text-gray-600">Evaluate performance and safety.</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-2">Compute Factory</h2>
          <p className="text-gray-600">Manage GPU/CPU resources.</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-2">Runtime Factory</h2>
          <p className="text-gray-600">Deploy and interact with agents.</p>
        </div>
      </div>
    </div>
  );
}