import React from 'react';
import { QRCodeCanvas } from 'qrcode.react';

const MainPage = () => {
  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%)' }}>
      <div style={{ background: 'white', padding: '2.5rem 2rem', borderRadius: 16, boxShadow: '0 8px 32px rgba(60,72,100,0.12)', textAlign: 'center', maxWidth: 400, width: '100%' }}>
        <h1 style={{ color: '#6366f1', marginBottom: 24, fontWeight: 700, fontFamily: 'Inter, sans-serif', fontSize: 28 }}>Scan the QR Code</h1>
        <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 24 }}>
          <QRCodeCanvas value={window.location.origin + '/form'} size={192} bgColor="#f1f5f9" fgColor="#6366f1" style={{ borderRadius: 12, boxShadow: '0 2px 8px rgba(99,102,241,0.08)' }} />
        </div>
        <p style={{ color: '#374151', fontSize: 16, marginTop: 16 }}>Scan this QR code to fill out the networking form</p>
      </div>
    </div>
  );
};

export default MainPage; 