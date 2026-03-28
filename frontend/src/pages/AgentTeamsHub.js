import React, { useState, useEffect } from 'react';
import { Sparkles, MessageCircle, Activity, Zap, Brain, Users, TrendingUp, Clock, CheckCircle } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

const AgentTeamsHub = () => {
  const [activeAgent, setActiveAgent] = useState(null);
  const [chatMessages, setChatMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [agentStats, setAgentStats] = useState({});
  const [isTyping, setIsTyping] = useState(false);

  const aiAgents = [
    {
      id: 'scout',
      name: 'Scout Agent',
      role: 'Opportunity Hunter',
      icon: '🎯',
      color: 'cyan',
      status: 'active',
      tasks: 24,
      success: '94%',
      description: 'Continuously scans markets for profitable opportunities',
      capabilities: ['Market Research', 'Trend Analysis', 'Niche Discovery', 'Competitor Analysis']
    },
    {
      id: 'creator',
      name: 'Creator Agent',
      role: 'Product Generator',
      icon: '🎨',
      color: 'purple',
      status: 'active',
      tasks: 18,
      success: '91%',
      description: 'Creates high-quality digital products autonomously',
      capabilities: ['eBook Writing', 'Course Creation', 'Template Design', 'Content Generation']
    },
    {
      id: 'publisher',
      name: 'Publisher Agent',
      role: 'Marketplace Integration',
      icon: '🚀',
      color: 'green',
      status: 'active',
      tasks: 32,
      success: '97%',
      description: 'Publishes and optimizes listings across platforms',
      capabilities: ['Gumroad Publishing', 'SEO Optimization', 'Pricing Strategy', 'Auto-Updates']
    },
    {
      id: 'marketer',
      name: 'Marketer Agent',
      role: 'Campaign Manager',
      icon: '📈',
      color: 'pink',
      status: 'active',
      tasks: 41,
      success: '89%',
      description: 'Creates and manages multi-platform marketing campaigns',
      capabilities: ['Social Media Posts', 'Email Campaigns', 'Ad Copy', 'Influencer Outreach']
    },
    {
      id: 'analyst',
      name: 'Analyst Agent',
      role: 'Data Intelligence',
      icon: '📊',
      color: 'blue',
      status: 'active',
      tasks: 56,
      success: '96%',
      description: 'Analyzes performance and optimizes strategies',
      capabilities: ['Revenue Analysis', 'Performance Tracking', 'A/B Testing', 'Predictive Modeling']
    },
    {
      id: 'optimizer',
      name: 'Optimizer Agent',
      role: 'Revenue Maximizer',
      icon: '💰',
      color: 'yellow',
      status: 'active',
      tasks: 15,
      success: '92%',
      description: 'Maximizes revenue through intelligent pricing and upsells',
      capabilities: ['Dynamic Pricing', 'Upsell Sequences', 'Bundle Creation', 'Discount Strategy']
    }
  ];

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || !activeAgent) return;

    const userMessage = {
      role: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString()
    };

    setChatMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsTyping(true);

    // Simulate AI response
    setTimeout(() => {
      const agentMessage = {
        role: 'assistant',
        content: `I'm ${activeAgent.name}. I understand you want to ${inputMessage}. Let me process this request and get back to you with actionable insights.`,
        timestamp: new Date().toISOString()
      };
      setChatMessages(prev => [...prev, agentMessage]);
      setIsTyping(false);
    }, 1500);
  };

  const selectAgent = (agent) => {
    setActiveAgent(agent);
    setChatMessages([
      {
        role: 'assistant',
        content: `Hello! I'm ${agent.name}, your ${agent.role}. ${agent.description} How can I assist you today?`,
        timestamp: new Date().toISOString()
      }
    ]);
  };

  return (
    <div style={{ padding: 'var(--spacing-2xl)' }}>
      {/* Header */}
      <div style={{ marginBottom: 'var(--spacing-2xl)' }}>
        <h1 style={{
          fontSize: 'var(--font-size-4xl)',
          fontWeight: '900',
          background: 'var(--gradient-holographic)',
          backgroundSize: '200% 200%',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text',
          animation: 'holographicShift 4s ease infinite',
          marginBottom: 'var(--spacing-sm)'
        }}>
          <Users size={36} style={{ display: 'inline-block', marginRight: '1rem', color: '#06b6d4' }} />
          AI AGENT TEAMS
        </h1>
        <p style={{ color: 'var(--color-text-secondary)', fontSize: 'var(--font-size-lg)' }}>
          Interact with autonomous AI agents powering your entertainment empire
        </p>
      </div>

      {/* Agent Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
        gap: 'var(--spacing-lg)',
        marginBottom: 'var(--spacing-2xl)'
      }}>
        {aiAgents.map((agent) => (
          <div
            key={agent.id}
            onClick={() => selectAgent(agent)}
            className="glass"
            style={{
              padding: 'var(--spacing-xl)',
              borderRadius: 'var(--radius-xl)',
              cursor: 'pointer',
              transition: 'all var(--transition-normal)',
              border: activeAgent?.id === agent.id 
                ? '2px solid var(--color-electric-cyan)' 
                : '1px solid var(--color-glass-border)',
              boxShadow: activeAgent?.id === agent.id ? 'var(--glow-cyan)' : 'none',
              position: 'relative',
              overflow: 'hidden'
            }}
          >
            {/* Agent Header */}
            <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-md)', marginBottom: 'var(--spacing-lg)' }}>
              <div style={{
                width: '64px',
                height: '64px',
                borderRadius: 'var(--radius-md)',
                background: `linear-gradient(135deg, rgba(6, 182, 212, 0.2), rgba(168, 85, 247, 0.2))`,
                border: '1px solid rgba(6, 182, 212, 0.4)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '2rem',
                boxShadow: 'var(--glow-cyan)'
              }}>
                {agent.icon}
              </div>
              <div style={{ flex: 1 }}>
                <h3 style={{
                  fontSize: 'var(--font-size-xl)',
                  fontWeight: '700',
                  color: 'var(--color-text-primary)',
                  marginBottom: '0.25rem'
                }}>
                  {agent.name}
                </h3>
                <p style={{
                  fontSize: 'var(--font-size-sm)',
                  color: 'var(--color-electric-cyan)',
                  textTransform: 'uppercase',
                  letterSpacing: '1px'
                }}>
                  {agent.role}
                </p>
              </div>
              <div style={{
                background: 'rgba(16, 185, 129, 0.2)',
                color: '#10b981',
                padding: '4px 12px',
                borderRadius: 'var(--radius-full)',
                fontSize: 'var(--font-size-xs)',
                fontWeight: '700',
                textTransform: 'uppercase',
                border: '1px solid rgba(16, 185, 129, 0.3)'
              }}>
                {agent.status}
              </div>
            </div>

            {/* Agent Description */}
            <p style={{
              fontSize: 'var(--font-size-sm)',
              color: 'var(--color-text-secondary)',
              marginBottom: 'var(--spacing-lg)',
              lineHeight: '1.6'
            }}>
              {agent.description}
            </p>

            {/* Agent Stats */}
            <div style={{
              display: 'grid',
              gridTemplateColumns: '1fr 1fr',
              gap: 'var(--spacing-md)',
              marginBottom: 'var(--spacing-lg)'
            }}>
              <div style={{
                background: 'rgba(6, 182, 212, 0.1)',
                padding: 'var(--spacing-md)',
                borderRadius: 'var(--radius-md)',
                border: '1px solid rgba(6, 182, 212, 0.2)'
              }}>
                <div style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-tertiary)', marginBottom: '0.25rem' }}>
                  Active Tasks
                </div>
                <div style={{ fontSize: 'var(--font-size-xl)', fontWeight: '700', color: 'var(--color-electric-cyan)' }}>
                  {agent.tasks}
                </div>
              </div>
              <div style={{
                background: 'rgba(16, 185, 129, 0.1)',
                padding: 'var(--spacing-md)',
                borderRadius: 'var(--radius-md)',
                border: '1px solid rgba(16, 185, 129, 0.2)'
              }}>
                <div style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-tertiary)', marginBottom: '0.25rem' }}>
                  Success Rate
                </div>
                <div style={{ fontSize: 'var(--font-size-xl)', fontWeight: '700', color: '#10b981' }}>
                  {agent.success}
                </div>
              </div>
            </div>

            {/* Capabilities */}
            <div>
              <div style={{
                fontSize: 'var(--font-size-xs)',
                color: 'var(--color-text-tertiary)',
                textTransform: 'uppercase',
                letterSpacing: '1px',
                marginBottom: 'var(--spacing-sm)'
              }}>
                Capabilities
              </div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                {agent.capabilities.map((cap, idx) => (
                  <span
                    key={idx}
                    style={{
                      fontSize: 'var(--font-size-xs)',
                      padding: '4px 10px',
                      background: 'rgba(168, 85, 247, 0.1)',
                      border: '1px solid rgba(168, 85, 247, 0.3)',
                      borderRadius: 'var(--radius-sm)',
                      color: '#a855f7'
                    }}
                  >
                    {cap}
                  </span>
                ))}
              </div>
            </div>

            {/* Chat Button */}
            <button
              className="btn-primary"
              style={{
                width: '100%',
                marginTop: 'var(--spacing-lg)',
                justifyContent: 'center'
              }}
            >
              <MessageCircle size={18} />
              <span>Chat with Agent</span>
            </button>
          </div>
        ))}
      </div>

      {/* Active Agent Chat Interface */}
      {activeAgent && (
        <div className="glass" style={{
          borderRadius: 'var(--radius-xl)',
          padding: 'var(--spacing-xl)',
          border: '1px solid var(--color-electric-cyan)',
          boxShadow: 'var(--glow-cyan)'
        }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            marginBottom: 'var(--spacing-xl)',
            paddingBottom: 'var(--spacing-lg)',
            borderBottom: '1px solid rgba(6, 182, 212, 0.3)'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-md)' }}>
              <div style={{ fontSize: '2.5rem' }}>{activeAgent.icon}</div>
              <div>
                <h2 style={{
                  fontSize: 'var(--font-size-2xl)',
                  fontWeight: '800',
                  color: 'var(--color-text-primary)',
                  marginBottom: '0.25rem'
                }}>
                  {activeAgent.name}
                </h2>
                <p style={{ fontSize: 'var(--font-size-sm)', color: 'var(--color-electric-cyan)' }}>
                  {activeAgent.role}
                </p>
              </div>
            </div>
            <div style={{
              background: 'rgba(16, 185, 129, 0.2)',
              color: '#10b981',
              padding: '8px 16px',
              borderRadius: 'var(--radius-full)',
              fontSize: 'var(--font-size-sm)',
              fontWeight: '700',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem'
            }}>
              <div style={{
                width: '8px',
                height: '8px',
                background: '#10b981',
                borderRadius: '50%',
                boxShadow: '0 0 10px #10b981',
                animation: 'pulse 2s infinite'
              }}></div>
              ONLINE
            </div>
          </div>

          {/* Chat Messages */}
          <div style={{
            height: '400px',
            overflowY: 'auto',
            marginBottom: 'var(--spacing-lg)',
            padding: 'var(--spacing-md)',
            background: 'rgba(0, 0, 0, 0.2)',
            borderRadius: 'var(--radius-md)'
          }}>
            {chatMessages.map((msg, idx) => (
              <div
                key={idx}
                style={{
                  display: 'flex',
                  justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start',
                  marginBottom: 'var(--spacing-md)'
                }}
              >
                <div style={{
                  maxWidth: '70%',
                  padding: 'var(--spacing-md)',
                  borderRadius: 'var(--radius-md)',
                  background: msg.role === 'user' 
                    ? 'linear-gradient(135deg, #06b6d4, #a855f7)'
                    : 'rgba(15, 23, 42, 0.8)',
                  border: msg.role === 'user'
                    ? 'none'
                    : '1px solid rgba(6, 182, 212, 0.3)',
                  color: 'white'
                }}>
                  <div style={{
                    fontSize: 'var(--font-size-sm)',
                    lineHeight: '1.6'
                  }}>
                    {msg.content}
                  </div>
                  <div style={{
                    fontSize: 'var(--font-size-xs)',
                    color: 'rgba(255, 255, 255, 0.6)',
                    marginTop: '0.5rem'
                  }}>
                    {new Date(msg.timestamp).toLocaleTimeString()}
                  </div>
                </div>
              </div>
            ))}
            {isTyping && (
              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                color: 'var(--color-electric-cyan)',
                fontSize: 'var(--font-size-sm)'
              }}>
                <Activity className="animate-spin" size={16} />
                {activeAgent.name} is typing...
              </div>
            )}
          </div>

          {/* Chat Input */}
          <div style={{ display: 'flex', gap: 'var(--spacing-md)' }}>
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder={`Message ${activeAgent.name}...`}
              style={{
                flex: 1,
                padding: 'var(--spacing-md)',
                background: 'rgba(15, 23, 42, 0.6)',
                border: '1px solid rgba(6, 182, 212, 0.3)',
                borderRadius: 'var(--radius-md)',
                color: 'var(--color-text-primary)',
                fontSize: 'var(--font-size-sm)',
                outline: 'none'
              }}
            />
            <button
              onClick={handleSendMessage}
              className="btn-primary"
              disabled={!inputMessage.trim()}
            >
              <Zap size={18} />
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default AgentTeamsHub;
