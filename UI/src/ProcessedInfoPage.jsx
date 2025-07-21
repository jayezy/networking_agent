import React, { useState, useEffect } from 'react';

const ProcessedInfoPage = () => {
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedUser, setSelectedUser] = useState(null);

  useEffect(() => {
    fetchMatches();
  }, []);

  const fetchMatches = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:3001/api/get-all-matches');
      const data = await response.json();
      
      if (data.success && data.result) {
        // Extract matches from the result
        const allMatches = data.result.all_matches || {};
        const matchesList = Object.values(allMatches).flatMap(userMatches => 
          userMatches.matches || []
        );
        setMatches(matchesList);
      } else {
        setError('No matches found');
      }
    } catch (err) {
      setError('Failed to fetch matches');
      console.error('Error fetching matches:', err);
    } finally {
      setLoading(false);
    }
  };

  const generateMatches = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:3001/api/generate-matches', {
        method: 'POST'
      });
      const data = await response.json();
      
      if (data.success) {
        await fetchMatches(); // Refresh matches after generation
      } else {
        setError('Failed to generate matches');
      }
    } catch (err) {
      setError('Failed to generate matches');
      console.error('Error generating matches:', err);
    } finally {
      setLoading(false);
    }
  };

  const MatchCard = ({ match }) => (
    <div style={{
      background: 'white',
      borderRadius: 12,
      padding: 20,
      marginBottom: 16,
      boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
      border: '1px solid #e5e7eb'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 12 }}>
        <div>
          <h3 style={{ margin: 0, color: '#1f2937', fontSize: 18, fontWeight: 600 }}>
            {match.name}
          </h3>
          <p style={{ margin: '4px 0', color: '#6b7280', fontSize: 14 }}>
            {match.title || 'Professional'}
          </p>
        </div>
        <div style={{
          background: `linear-gradient(90deg, #10b981 0%, #059669 100%)`,
          color: 'white',
          padding: '8px 12px',
          borderRadius: 20,
          fontSize: 14,
          fontWeight: 600
        }}>
          {match.match_percentage || Math.round(match.match_score * 100)}% Match
        </div>
      </div>
      
      <p style={{ 
        margin: '12px 0', 
        color: '#374151', 
        fontSize: 14, 
        lineHeight: 1.5 
      }}>
        {match.summary || 'No summary available'}
      </p>
      
      {match.tags && match.tags.length > 0 && (
        <div style={{ marginBottom: 12 }}>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
            {match.tags.slice(0, 5).map((tag, index) => (
              <span key={index} style={{
                background: '#f3f4f6',
                color: '#374151',
                padding: '4px 8px',
                borderRadius: 12,
                fontSize: 12,
                fontWeight: 500
              }}>
                {tag}
              </span>
            ))}
          </div>
        </div>
      )}
      
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <a 
          href={match.linkedin_url} 
          target="_blank" 
          rel="noopener noreferrer"
          style={{
            color: '#6366f1',
            textDecoration: 'none',
            fontSize: 14,
            fontWeight: 500
          }}
        >
          View LinkedIn Profile →
        </a>
        <div style={{ fontSize: 12, color: '#6b7280' }}>
          Score: {match.match_score ? match.match_score.toFixed(2) : 'N/A'}
        </div>
      </div>
    </div>
  );

  if (loading) {
    return (
      <div style={{ 
        minHeight: '100vh', 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center', 
        background: 'linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%)' 
      }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: 24, marginBottom: 16 }}>🔄</div>
          <p style={{ color: '#374151', fontSize: 18 }}>Loading matches...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ 
        minHeight: '100vh', 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center', 
        background: 'linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%)' 
      }}>
        <div style={{ 
          background: 'white', 
          padding: '2.5rem 2rem', 
          borderRadius: 16, 
          boxShadow: '0 8px 32px rgba(60,72,100,0.12)', 
          textAlign: 'center', 
          maxWidth: 400 
        }}>
          <h2 style={{ color: '#ef4444', marginBottom: 16 }}>Error</h2>
          <p style={{ color: '#374151', fontSize: 18, marginBottom: 20 }}>{error}</p>
          <button
            onClick={generateMatches}
            style={{
              padding: '12px 24px',
              background: 'linear-gradient(90deg, #6366f1 0%, #818cf8 100%)',
              color: 'white',
              fontWeight: 700,
              fontSize: 16,
              border: 'none',
              borderRadius: 8,
              cursor: 'pointer',
              marginRight: 12
            }}
          >
            Generate Matches
          </button>
          <button
            onClick={fetchMatches}
            style={{
              padding: '12px 24px',
              background: '#f3f4f6',
              color: '#374151',
              fontWeight: 700,
              fontSize: 16,
              border: '1px solid #d1d5db',
              borderRadius: 8,
              cursor: 'pointer'
            }}
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div style={{ 
      minHeight: '100vh', 
      background: 'linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%)',
      padding: '20px'
    }}>
      <div style={{ maxWidth: 800, margin: '0 auto' }}>
        <div style={{ 
          background: 'white', 
          padding: '2rem', 
          borderRadius: 16, 
          boxShadow: '0 8px 32px rgba(60,72,100,0.12)',
          marginBottom: 24
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
            <div>
              <h1 style={{ 
                color: '#1f2937', 
                margin: 0, 
                fontSize: 28, 
                fontWeight: 700 
              }}>
                Networking Matches
              </h1>
              <p style={{ 
                color: '#6b7280', 
                margin: '8px 0 0 0', 
                fontSize: 16 
              }}>
                {matches.length} matches found
              </p>
            </div>
            <button
              onClick={generateMatches}
              style={{
                padding: '12px 24px',
                background: 'linear-gradient(90deg, #6366f1 0%, #818cf8 100%)',
                color: 'white',
                fontWeight: 700,
                fontSize: 16,
                border: 'none',
                borderRadius: 8,
                cursor: 'pointer',
                boxShadow: '0 2px 8px rgba(99,102,241,0.2)'
              }}
            >
              Generate New Matches
            </button>
          </div>
        </div>

        {matches.length === 0 ? (
          <div style={{ 
            background: 'white', 
            padding: '3rem 2rem', 
            borderRadius: 16, 
            boxShadow: '0 8px 32px rgba(60,72,100,0.12)', 
            textAlign: 'center' 
          }}>
            <div style={{ fontSize: 48, marginBottom: 16 }}>🤝</div>
            <h2 style={{ color: '#1f2937', marginBottom: 16 }}>No Matches Yet</h2>
            <p style={{ color: '#6b7280', fontSize: 18, marginBottom: 24 }}>
              Generate matches to see your networking recommendations
            </p>
            <button
              onClick={generateMatches}
              style={{
                padding: '12px 24px',
                background: 'linear-gradient(90deg, #6366f1 0%, #818cf8 100%)',
                color: 'white',
                fontWeight: 700,
                fontSize: 16,
                border: 'none',
                borderRadius: 8,
                cursor: 'pointer'
              }}
            >
              Generate Matches
            </button>
          </div>
        ) : (
          <div>
            {matches.map((match, index) => (
              <MatchCard key={index} match={match} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ProcessedInfoPage; 