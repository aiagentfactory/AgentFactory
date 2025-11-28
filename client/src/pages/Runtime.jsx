import React, { useState, useEffect } from 'react';
import api from '../api';

export default function Runtime() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [agent, setAgent] = useState(null);

  useEffect(() => {
    deployAgent();
  }, []);

  const deployAgent = async () => {
    // Check if agent exists or deploy one
    const res = await api.get('/runtime/agents');
    if (res.data.length === 0) {
      const newAgent = await api.post('/runtime/agents', {
        name: "Assistant-V1",
        version: "1.0.0",
        config: {}
      });
      setAgent(newAgent.data);
    } else {
      setAgent(res.data[0]);
    }
  };

  const sendMessage = async () => {
    if (!input.trim() || !agent) return;

    const newMsg = { role: 'user', text: input };
    setMessages(prev => [...prev, newMsg]);
    setInput('');

    try {
      const res = await api.post('/runtime/chat', {
        agent_id: agent.id,
        message: input,
        session_id: "session-1"
      });
      
      setMessages(prev => [...prev, { role: 'agent', text: res.data.response }]);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="p-6 h-screen flex flex-col">
      <h1 className="text-2xl font-bold mb-4">Runtime Factory - Agent Chat</h1>
      <div className="flex-1 bg-white p-4 rounded shadow overflow-y-auto mb-4 border">
        {messages.map((msg, idx) => (
          <div key={idx} className={`mb-2 p-2 rounded ${msg.role === 'user' ? 'bg-blue-100 text-right' : 'bg-gray-100 text-left'}`}>
            <span className="font-bold text-xs block text-gray-500">{msg.role.toUpperCase()}</span>
            {msg.text}
          </div>
        ))}
      </div>
      <div className="flex">
        <input 
          className="flex-1 border p-2 rounded-l"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyPress={e => e.key === 'Enter' && sendMessage()}
          placeholder="Type a message..."
        />
        <button 
          onClick={sendMessage}
          className="bg-blue-500 text-white px-6 py-2 rounded-r hover:bg-blue-600"
        >
          Send
        </button>
      </div>
    </div>
  );
}
