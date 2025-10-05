import React from 'react';
import BotpressChatbot from './BotpressChatbot';
import './App.css';

function App() {
  return (
    <div className="App">
      <div style={{ 
        minHeight: '100vh', 
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '20px'
      }}>
        <div style={{ 
          background: 'white', 
          padding: '40px', 
          borderRadius: '20px',
          boxShadow: '0 20px 60px rgba(0,0,0,0.3)',
          textAlign: 'center',
          maxWidth: '600px'
        }}>
          <h1 style={{ 
            fontSize: '2.5rem', 
            color: '#333',
            marginBottom: '20px'
          }}>
            Welcome to AI Chatbot
          </h1>
          <p style={{ 
            fontSize: '1.2rem', 
            color: '#666',
            marginBottom: '30px'
          }}>
            Click the chat button in the bottom right corner to start a conversation!
          </p>
          <div style={{ 
            background: '#f0f0f0', 
            padding: '20px', 
            borderRadius: '10px',
            marginTop: '20px'
          }}>
            <p style={{ fontSize: '0.9rem', color: '#888' }}>
              Powered by Botpress & React
            </p>
          </div>
        </div>
      </div>
      <BotpressChatbot />
    </div>
  );
}

export default App;