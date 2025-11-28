import React, { useState, useEffect } from 'react';
import { MessageSquare, Rocket } from 'lucide-react';

const RuntimeFactory = () => {
  const [models, setModels] = useState([]);
  const [agents, setAgents] = useState([]);
  const [deployConfig, setDeployConfig] = useState({ name: '', model_id: '' });
  
  // Chat State
  const [chatInput, setChatInput] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [activeAgentId, setActiveAgentId] = useState(null);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/algo/models').then(r => r.json()).then(setModels);
    fetch('http://127.0.0.1:8000/runtime/agents').then(r => r.json()).then(setAgents);
  }, []);

  const deployAgent = () => {
      fetch('http://127.0.0.1:8000/runtime/agents', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify(deployConfig)
      }).then(r => r.json()).then(a => setAgents([...agents, a]));
  };

  const sendMessage = () => {
      if(!activeAgentId) return;
      const userMsg = chatInput;
      setChatHistory([...chatHistory, { role: 'user', content: userMsg }]);
      setChatInput('');

      fetch('http://127.0.0.1:8000/runtime/chat', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ agent_id: activeAgentId, message: userMsg, session_id: 'web-1' })
      }).then(r => r.json()).then(res => {
          setChatHistory(prev => [...prev, { role: 'agent', content: res.response }]);
      });
  };

  return (
    <div className="page-container">
      <header className="page-header">
        <h1>Runtime Factory</h1>
        <p>Deploy and interact with Agents.</p>
      </header>

      <div className="grid-2">
          <div className="card">
              <h3><Rocket size={18}/> Deploy New Agent</h3>
              <div className="form-group">
                  <label>Agent Name</label>
                  <input type="text" onChange={e => setDeployConfig({...deployConfig, name: e.target.value})} />
              </div>
              <div className="form-group">
                  <label>Select Model</label>
                  <select onChange={e => setDeployConfig({...deployConfig, model_id: e.target.value})}>
                      <option value="">-- Select Model --</option>
                      {models.map(m => <option key={m.id} value={m.id}>{m.name}</option>)}
                  </select>
              </div>
              <button className="btn-primary" onClick={deployAgent}>Deploy Agent</button>
          </div>

          <div className="card">
              <h3>Active Agents</h3>
              <ul>
                  {agents.map(a => (
                      <li key={a.id} 
                          style={{
                              padding: '5px', 
                              cursor: 'pointer', 
                              background: activeAgentId === a.id ? '#eef2ff' : 'transparent',
                              borderRadius: '4px'
                          }}
                          onClick={() => setActiveAgentId(a.id)}
                      >
                          <strong>{a.name}</strong> (Model ID: {a.model_id})
                      </li>
                  ))}
              </ul>
          </div>
      </div>

      <div className="card" style={{marginTop: '20px', height: '300px', display: 'flex', flexDirection: 'column'}}>
          <h3><MessageSquare size={18}/> Chat Interface</h3>
          <div style={{flex: 1, overflowY: 'auto', marginBottom: '10px', border: '1px solid #eee', padding: '10px'}}>
              {chatHistory.map((msg, i) => (
                  <div key={i} style={{textAlign: msg.role === 'user' ? 'right' : 'left', margin: '5px 0'}}>
                      <span style={{
                          background: msg.role === 'user' ? '#4f46e5' : '#f3f4f6',
                          color: msg.role === 'user' ? 'white' : 'black',
                          padding: '5px 10px',
                          borderRadius: '10px'
                      }}>
                          {msg.content}
                      </span>
                  </div>
              ))}
          </div>
          <div style={{display: 'flex', gap: '10px'}}>
              <input 
                  type="text" 
                  style={{flex: 1}} 
                  value={chatInput}
                  onChange={e => setChatInput(e.target.value)}
                  placeholder="Type a message..."
                  disabled={!activeAgentId}
              />
              <button className="btn-primary" onClick={sendMessage} disabled={!activeAgentId}>Send</button>
          </div>
      </div>
    </div>
  );
};

export default RuntimeFactory;
