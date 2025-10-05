import React, { useState } from 'react';
import { X } from 'lucide-react';
import kataraLogo from './imagenes/katara-logo.svg'; 

export default function KataraChatbot() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div style={{ position: 'fixed', bottom: '24px', right: '24px', zIndex: 9999 }}>
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          style={{
            background: 'linear-gradient(to right, #2563EB, #06B6D4)',
            color: 'white',
            borderRadius: '50px',
            padding: '12px 20px',
            border: 'none',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            fontSize: '18px',
            fontWeight: '600',
            boxShadow: '0 10px 30px rgba(0,0,0,0.25)',
            transition: 'all 0.3s ease',
          }}
        >
          <img
            src={kataraLogo}
            alt="Katara Logo"
            style={{
              width: '65px',
              height: '65px',
              borderRadius: '50%',
            }}
          />
          <span>Katara</span>
        </button>
      )}

      {isOpen && (
        <div
          style={{
            position: 'fixed',
            bottom: '24px',
            right: '24px',
            width: '400px',
            height: '600px',
            borderRadius: '20px',
            overflow: 'hidden',
            boxShadow: '0 20px 60px rgba(0,0,0,0.2)',
            display: 'flex',
            flexDirection: 'column',
            background: '#BBE0F4', 
          }}
        >
          <div
            style={{
              background: 'linear-gradient(to right, #2563EB, #1D4ED8)',
              color: 'white',
              padding: '15px 20px',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <img
                src={kataraLogo}
                alt="Katara Logo"
                style={{ width: '50x', height: '75px', borderRadius: '75%' }}
              />
              <div>
                <h3 style={{ margin: 0, fontSize: '23px', fontWeight: '600' }}>Katara</h3>
                <p style={{ margin: 0, fontSize: '13px', opacity: 0.9 }}>En línea</p>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              style={{
                background: 'rgba(255,255,255,0.2)',
                border: 'none',
                color: 'white',
                borderRadius: '50%',
                width: '40px',
                height: '40px',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <X size={22} />
            </button>
          </div>

          <iframe
            src="https://cdn.botpress.cloud/webchat/v3.3/shareable.html?configUrl=https://files.bpcontent.cloud/2025/10/04/20/20251004200934-KPRPG09B.json"
            style={{ width: '100%', height: '100%', border: 'none' }}
            title="Katara - Weather Benders"
          />
        </div>
      )}
    </div>
  );
}