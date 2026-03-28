import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  Activity, Users, Palette, TrendingUp, Settings, 
  Sparkles, Key, Search, Package 
} from 'lucide-react';

const Layout = ({ children, onShowAIAssistant, onShowKeyVault, onShowOpportunityHunter, onShowProjectFiles }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  return (
    <div className="app-container">
      {/* Mobile Menu Button */}
      <button 
        className="mobile-menu-btn"
        onClick={() => setSidebarOpen(!sidebarOpen)}
      >
        <Settings size={24} />
      </button>

      {/* Quantum Sidebar */}
      <div className={`quantum-sidebar ${sidebarOpen ? 'sidebar-open' : ''}`}>
        <div className="sidebar-logo">
          <div className="logo-content">
            <h1>
              <Sparkles size={24} />
              FIILTHY.AI
            </h1>
            <p className="logo-subtitle">Entertainment System</p>
          </div>
        </div>

        <nav className="sidebar-nav">
          <div className="nav-section">
            <div className="nav-section-title">Main</div>
            <Link 
              to="/" 
              className={`nav-item ${isActive('/') ? 'active' : ''}`}
              style={{ textDecoration: 'none' }}
              onClick={() => setSidebarOpen(false)}
            >
              <Activity size={18} />
              <span>Dashboard</span>
            </Link>
            <Link 
              to="/agent-teams" 
              className={`nav-item ${isActive('/agent-teams') ? 'active' : ''}`}
              style={{ textDecoration: 'none' }}
              onClick={() => setSidebarOpen(false)}
            >
              <Users size={18} />
              <span>Agent Teams</span>
            </Link>
            <Link 
              to="/product-studio" 
              className={`nav-item ${isActive('/product-studio') ? 'active' : ''}`}
              style={{ textDecoration: 'none' }}
              onClick={() => setSidebarOpen(false)}
            >
              <Palette size={18} />
              <span>Product Studio</span>
            </Link>
          </div>

          <div className="nav-section">
            <div className="nav-section-title">Tools</div>
            <button
              onClick={() => { onShowAIAssistant?.(); setSidebarOpen(false); }}
              className="nav-item"
            >
              <Sparkles size={18} />
              <span>AI Assistant</span>
            </button>
            <button
              onClick={() => { onShowKeyVault?.(); setSidebarOpen(false); }}
              className="nav-item"
            >
              <Key size={18} />
              <span>Key Vault</span>
            </button>
            <button
              onClick={() => { onShowOpportunityHunter?.(); setSidebarOpen(false); }}
              className="nav-item"
            >
              <Search size={18} />
              <span>Opportunities</span>
            </button>
            <button
              onClick={() => { onShowProjectFiles?.(); setSidebarOpen(false); }}
              className="nav-item"
            >
              <Package size={18} />
              <span>Project Files</span>
            </button>
          </div>
        </nav>

        <div className="sidebar-footer">
          <div className="system-status-sidebar">
            <div className="status-pulse"></div>
            <span className="status-text">Online</span>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="main-content">
        <div className="content">
          {children}
        </div>
      </div>
    </div>
  );
};

export default Layout;
