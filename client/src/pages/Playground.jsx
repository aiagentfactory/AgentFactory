import React, { useState, useEffect, useRef } from 'react';
import { Send, Bot, User } from 'lucide-react';
import './Playground.css';

const Playground = () => {
  const [agents, setAgents] = useState([]);
  const [selectedAgentId, setSelectedAgentId] = useState('');
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const chatEndRef = useRef(null);

  // Fetch available agents on mount
  useEffect(() => {
    fetch('http://127.0.0.1:8000/runtime/agents')
      .then(res => res.json())
      .then(data => {
        setAgents(data);
        if (data.length > 0) setSelectedAgentId(data[0].id);
      })
      .catch(console.error);
  }, []);

  // Scroll to bottom
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || !selectedAgentId) return;

    const userMsg = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');

    try {
        const res = await fetch('http://127.0.0.1:8000/runtime/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                agent_id: selectedAgentId,
                message: userMsg.content,
                session_id: "demo-session"
            })
        });
        const data = await res.json();
        setMessages(prev => [...prev, { role: 'agent', content: data.response }]);
    } catch (err) {
        setMessages(prev => [...prev, { role: 'system', content: "Error: Failed to connect to agent." }]);
    }
  };

  return (
    <div className="page-container chat-page">
        <div className="chat-sidebar">
            <h3>Select Agent</h3>
            {agents.length === 0 ? <p className="no-agents">No active agents.</p> : (
                <div className="agent-list">
                    {agents.map(agent => (
                        <div 
                            key={agent.id} 
                            className={`agent-item ${selectedAgentId === agent.id ? 'active' : ''}`}
                            onClick={() => setSelectedAgentId(agent.id)}
                        >
                            <Bot size={20}/>
                            <div className="agent-info">
                                <span className="name">{agent.name}</span>
                                <span className="ver">v{agent.version}</span>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>

        <div className="chat-main">
            <div className="chat-history">
                {messages.length === 0 && (
                    <div className="welcome-msg">
                        <Bot size={48} />
                        <h2>Welcome to the Playground</h2>
                        <p>Select an agent and start testing its capabilities.</p>
                    </div>
                )}
                {messages.map((msg, i) => (
                    <div key={i} className={`message ${msg.role}`}>
                        <div className="avatar">
                            {msg.role === 'agent' ? <Bot size={16} /> : <User size={16} />}
                        </div>
                        <div className="bubble">{msg.content}</div>
                    </div>
                ))}
                <div ref={chatEndRef} />
            </div>
            <div className="chat-input">
                <input 
                    type="text" 
                    placeholder="Type your message..." 
                    value={input}
                    onChange={e => setInput(e.target.value)}
                    onKeyDown={e => e.key === 'Enter' && handleSend()}
                    disabled={!selectedAgentId}
                />
                <button onClick={handleSend} disabled={!selectedAgentId || !input.trim()}>
                    <Send size={18} />
                </button>
            </div>
        </div>
    </div>
  );
};

export default Playground;
