import React, { useState } from 'react';

const ProcessedInfoPage = () => {
  const [formData, setFormData] = useState({
    firstname: '',
    lastname: ''
  });
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setUserData(null);

    try {
      const response = await fetch('http://localhost:3001/api/submissions');
      if (!response.ok) {
        throw new Error('Failed to fetch submissions');
      }

      const submissions = await response.json();
      
      // Search for user by first and last name (case insensitive)
      const foundUser = submissions.find(user => 
        user.first_name?.toLowerCase() === formData.firstname.toLowerCase() &&
        user.last_name?.toLowerCase() === formData.lastname.toLowerCase()
      );

      if (foundUser) {
        setUserData(foundUser);
      } else {
        setError('No user found with that name. Please check your spelling and try again.');
      }
    } catch (error) {
      setError('Error fetching data. Please try again.');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%)' }}>
      <div style={{ background: 'white', padding: '2.5rem 2rem', borderRadius: 16, boxShadow: '0 8px 32px rgba(60,72,100,0.12)', textAlign: 'center', maxWidth: 500, width: '100%' }}>
        <h2 style={{ color: '#6366f1', marginBottom: 24, fontWeight: 700, fontFamily: 'Inter, sans-serif' }}>Find Your Connections</h2>
        
        {!userData ? (
          <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: 20 }}>
              <label style={{ display: 'block', marginBottom: 6, color: '#374151', fontWeight: 500, textAlign: 'left' }}>First Name</label>
              <input
                type="text"
                name="firstname"
                value={formData.firstname}
                onChange={handleChange}
                required
                style={{
                  width: '100%',
                  padding: '12px 14px',
                  border: '1.5px solid #c7d2fe',
                  borderRadius: 8,
                  fontSize: 16,
                  outline: 'none',
                  fontFamily: 'Inter, sans-serif',
                  transition: 'border 0.2s',
                  boxSizing: 'border-box',
                  background: '#f1f5f9',
                }}
                onFocus={e => e.target.style.border = '1.5px solid #6366f1'}
                onBlur={e => e.target.style.border = '1.5px solid #c7d2fe'}
              />
            </div>
            <div style={{ marginBottom: 20 }}>
              <label style={{ display: 'block', marginBottom: 6, color: '#374151', fontWeight: 500, textAlign: 'left' }}>Last Name</label>
              <input
                type="text"
                name="lastname"
                value={formData.lastname}
                onChange={handleChange}
                required
                style={{
                  width: '100%',
                  padding: '12px 14px',
                  border: '1.5px solid #c7d2fe',
                  borderRadius: 8,
                  fontSize: 16,
                  outline: 'none',
                  fontFamily: 'Inter, sans-serif',
                  transition: 'border 0.2s',
                  boxSizing: 'border-box',
                  background: '#f1f5f9',
                }}
                onFocus={e => e.target.style.border = '1.5px solid #6366f1'}
                onBlur={e => e.target.style.border = '1.5px solid #c7d2fe'}
              />
            </div>
            {error && (
              <div style={{ marginBottom: 16, color: '#ef4444', fontSize: 14, textAlign: 'left' }}>
                {error}
              </div>
            )}
            <button
              type="submit"
              disabled={loading}
              style={{
                width: '100%',
                padding: '12px 24px',
                background: loading ? '#9ca3af' : 'linear-gradient(90deg, #6366f1 0%, #818cf8 100%)',
                color: 'white',
                fontWeight: 700,
                fontSize: 16,
                border: 'none',
                borderRadius: 8,
                boxShadow: '0 2px 8px rgba(99,102,241,0.08)',
                cursor: loading ? 'not-allowed' : 'pointer',
                transition: 'background 0.2s, transform 0.1s',
                fontFamily: 'Inter, sans-serif',
              }}
            >
              {loading ? 'Finding Connections...' : 'GO!'}
            </button>
          </form>
        ) : (
          <div style={{ textAlign: 'left' }}>
            <div style={{ marginBottom: 24, textAlign: 'center' }}>
              <h3 style={{ color: '#6366f1', marginBottom: 8, fontWeight: 600 }}>👋 Say Hi To</h3>
              <p style={{ color: '#6b7280', fontSize: 14 }}>User ID: {userData.user_id}</p>
            </div>
            
            <div style={{ marginBottom: 16 }}>
              <label style={{ display: 'block', marginBottom: 4, color: '#374151', fontWeight: 600, fontSize: 14 }}>Name</label>
              <p style={{ color: '#1f2937', fontSize: 16, margin: 0 }}>
                {userData.first_name} {userData.last_name}
              </p>
            </div>

            <div style={{ marginBottom: 16 }}>
              <label style={{ display: 'block', marginBottom: 4, color: '#374151', fontWeight: 600, fontSize: 14 }}>What You Bring</label>
              <p style={{ color: '#1f2937', fontSize: 16, margin: 0, fontStyle: 'italic' }}>
                {userData.value_in || 'Not specified'}
              </p>
            </div>

            <div style={{ marginBottom: 16 }}>
              <label style={{ display: 'block', marginBottom: 4, color: '#374151', fontWeight: 600, fontSize: 14 }}>What You're Looking For</label>
              <p style={{ color: '#1f2937', fontSize: 16, margin: 0, fontStyle: 'italic' }}>
                {userData.value_out || 'Not specified'}
              </p>
            </div>

            <div style={{ marginBottom: 16 }}>
              <label style={{ display: 'block', marginBottom: 4, color: '#374151', fontWeight: 600, fontSize: 14 }}>Ice Breaker</label>
              <p style={{ color: '#1f2937', fontSize: 16, margin: 0, fontStyle: 'italic' }}>
                {userData.ice_break || 'Not specified'}
              </p>
            </div>

            <div style={{ marginBottom: 24 }}>
              <label style={{ display: 'block', marginBottom: 4, color: '#374151', fontWeight: 600, fontSize: 14 }}>LinkedIn Profile</label>
              <a 
                href={userData.linkedin_url} 
                target="_blank" 
                rel="noopener noreferrer"
                style={{ 
                  color: '#6366f1', 
                  fontSize: 16, 
                  textDecoration: 'none',
                  wordBreak: 'break-all'
                }}
              >
                {userData.linkedin_url || 'Not provided'}
              </a>
            </div>

            <button
              onClick={() => {
                setUserData(null);
                setFormData({ firstname: '', lastname: '' });
                setError('');
              }}
              style={{
                width: '100%',
                padding: '12px 24px',
                background: '#f1f5f9',
                color: '#6366f1',
                fontWeight: 700,
                fontSize: 16,
                border: '1.5px solid #c7d2fe',
                borderRadius: 8,
                cursor: 'pointer',
                fontFamily: 'Inter, sans-serif',
              }}
            >
              Find Another Connection
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProcessedInfoPage; 