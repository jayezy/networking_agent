import React from 'react';

const ProcessedInfoPage = () => {
  // Placeholder for processed info
  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%)' }}>
      <div style={{ background: 'white', padding: '2.5rem 2rem', borderRadius: 16, boxShadow: '0 8px 32px rgba(60,72,100,0.12)', textAlign: 'center', maxWidth: 400 }}>
        <h2 style={{ color: '#6366f1', marginBottom: 16 }}>Processed Information</h2>
        <p style={{ color: '#374151', fontSize: 18 }}>This is where the processed information from the backend will be displayed.</p>
      </div>
    </div>
  );
};

export default ProcessedInfoPage; 