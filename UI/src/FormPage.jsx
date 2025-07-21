import React, { useState } from 'react';

const WELCOME_STATEMENTS = [
  "Let's make networking less awkward and more awesome!",
  "Ready to meet your next collaborator, co-founder, or coffee buddy?",
  "Answer a few questions, and we'll introduce you to your next great connection!",
  "Networking, but smarter. Tell us about yourself and get matched!",
  "No more wandering aimlessly—let us help you find your people!",
  "Fill this out and let the serendipity begin!",
  "Your next big opportunity could be one answer away.",
  "Let's turn small talk into big connections.",
  "Who will you meet tonight? Let's find out!",
  "Networking, upgraded. Ready to connect?",
  "Don't just mingle—match!",
  "Tell us a bit about you, and we'll handle the intros.",
  "The best connections start with a good question. Or three.",
  "Let's skip the awkward intros and get you matched!",
  "Welcome! Your next meaningful conversation starts here."
];

const LOOKING_FOR_EXAMPLES = [
  "meeting my next co-founder",
  "looking for my next opportunity/mentor",
  "looking for talented engineers",
  "finding investors for my startup",
  "connecting with industry experts",
  "hiring for my team",
  "learning about new technologies",
  "building partnerships",
  "finding a new job opportunity",
  "getting advice on scaling my business"
];

const INTERESTS_EXAMPLES = [
  "running, reading, cooking",
  "hiking, photography, music",
  "yoga, travel, coffee",
  "cycling, painting, movies",
  "swimming, writing, gardening",
  "rock climbing, podcasts, baking",
  "tennis, meditation, wine tasting",
  "soccer, chess, craft beer",
  "volleyball, poetry, woodworking",
  "basketball, astronomy, pottery"
];

const WHAT_YOU_BRING_EXAMPLES = [
  "10 years experience working with AI/ML",
  "5 years building scalable web applications",
  "Expertise in product management and go-to-market strategy",
  "Deep knowledge of cloud infrastructure and DevOps",
  "Experience leading engineering teams of 20+ people",
  "Background in data science and analytics",
  "Skills in UI/UX design and user research",
  "Network of 500+ industry professionals",
  "Experience raising $2M+ in venture capital",
  "Expertise in blockchain and DeFi protocols",
  "Background in marketing and growth hacking",
  "Experience scaling startups from 0 to 1000+ users",
  "Skills in mobile app development (iOS/Android)",
  "Knowledge of cybersecurity and compliance",
  "Experience in sales and business development"
];

function getRandomWelcome() {
  const idx = Math.floor(Math.random() * WELCOME_STATEMENTS.length);
  return WELCOME_STATEMENTS[idx] + ' 🤝🔗';
}

function getRandomExample(examples) {
  const idx = Math.floor(Math.random() * examples.length);
  return examples[idx];
}

const Confetti = () => (
  <div style={{ position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh', pointerEvents: 'none', zIndex: 1000 }}>
    <div style={{ fontSize: 48, textAlign: 'center', marginTop: '20vh' }}>
      🎉🎊✨🎉🎊✨
    </div>
  </div>
);

const FormPage = () => {
  const [step, setStep] = useState(1);
  const [form, setForm] = useState({
    firstname: '',
    lastname: '',
    linkedin: '',
    lookingFor: '',
    interests: '',
    whatYouBring: '',
  });
  const [welcome] = useState(getRandomWelcome());
  const [lookingForExample] = useState(getRandomExample(LOOKING_FOR_EXAMPLES));
  const [interestsExample] = useState(getRandomExample(INTERESTS_EXAMPLES));
  const [whatYouBringExample] = useState(getRandomExample(WHAT_YOU_BRING_EXAMPLES));
  const [submitted, setSubmitted] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleNext = (e) => {
    e && e.preventDefault();
    setStep(step + 1);
  };

  const handleBack = (e) => {
    e && e.preventDefault();
    setStep(step - 1);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Generate unique user ID
    const userId = 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    
    // Create JSON with question-answer tuples
    const formData = {
      userId: userId,
      timestamp: new Date().toISOString(),
      responses: [
        {
          question: "First Name",
          answer: form.firstname
        },
        {
          question: "Last Name", 
          answer: form.lastname
        },
        {
          question: "LinkedIn Profile",
          answer: form.linkedin
        },
        {
          question: "What are you looking for at this event?",
          answer: form.lookingFor
        },
        {
          question: "Help break the ice! What kind of stuff is your spice?",
          answer: form.interests
        },
        {
          question: "What do you bring?",
          answer: form.whatYouBring
        }
      ]
    };
    
    // Log the JSON to console
    console.log('Form Submission JSON:', JSON.stringify(formData, null, 2));
    
    // Store in localStorage for demo purposes
    localStorage.setItem('formSubmission_' + userId, JSON.stringify(formData));
    
    // Send data to backend to save in submission directory
    saveUserData(userId, formData);
    
    setSubmitted(true);
    setTimeout(() => {}, 500);
  };

  const saveUserData = async (userId, formData) => {
    try {
      const response = await fetch('http://localhost:3001/api/save-user-data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          userId: userId,
          formData: formData
        })
      });
      
      if (response.ok) {
        console.log(`User data saved successfully for ${userId}`);
      } else {
        console.error('Failed to save user data');
      }
    } catch (error) {
      console.error('Error saving user data:', error);
    }
  };

  if (submitted) {
    return (
      <>
        <Confetti />
        <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%)' }}>
          <div style={{ background: 'white', padding: '2.5rem 2rem', borderRadius: 16, boxShadow: '0 8px 32px rgba(60,72,100,0.12)', textAlign: 'center', maxWidth: 400 }}>
            <h2 style={{ color: '#6366f1', marginBottom: 16 }}>Success!</h2>
            <p style={{ color: '#374151', fontSize: 18 }}>Thank you for submitting! Enjoy the event and your new connections!</p>
          </div>
        </div>
      </>
    );
  }

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%)' }}>
      <div style={{ background: 'white', padding: '2.5rem 2rem', borderRadius: 16, boxShadow: '0 8px 32px rgba(60,72,100,0.12)', maxWidth: 400, width: '100%' }}>
        {step === 1 && (
          <form onSubmit={handleNext}>
            <h3 style={{ color: '#6366f1', marginBottom: 24, fontWeight: 700, fontFamily: 'Inter, sans-serif', textAlign: 'center' }}>Tell us about yourself 👤</h3>
            <div style={{ marginBottom: 20 }}>
              <label style={{ display: 'block', marginBottom: 6, color: '#374151', fontWeight: 500 }}>First Name</label>
              <input
                type="text"
                name="firstname"
                value={form.firstname}
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
              <label style={{ display: 'block', marginBottom: 6, color: '#374151', fontWeight: 500 }}>Last Name</label>
              <input
                type="text"
                name="lastname"
                value={form.lastname}
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
              <label style={{ display: 'block', marginBottom: 6, color: '#374151', fontWeight: 500 }}>LinkedIn Profile <span style={{ color: '#6366f1', fontWeight: 400 }}>(info from your LinkedIn will be used)</span></label>
              <input
                type="url"
                name="linkedin"
                value={form.linkedin}
                onChange={handleChange}
                required
                placeholder="https://linkedin.com/in/yourprofile"
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
              <div style={{ fontSize: 12, color: '#6366f1', marginTop: 4 }}>
                Disclaimer: Information from your LinkedIn page will be used to help match you with others.
              </div>
            </div>
            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 8 }}>
              <button
                type="submit"
                style={{
                  padding: '12px 24px',
                  background: 'linear-gradient(90deg, #6366f1 0%, #818cf8 100%)',
                  color: 'white',
                  fontWeight: 700,
                  fontSize: 16,
                  border: 'none',
                  borderRadius: 8,
                  boxShadow: '0 2px 8px rgba(99,102,241,0.08)',
                  cursor: 'pointer',
                  transition: 'background 0.2s, transform 0.1s',
                  fontFamily: 'Inter, sans-serif',
                }}
              >
                Next
              </button>
            </div>
          </form>
        )}
        {step === 2 && (
          <form onSubmit={handleNext}>
            <h3 style={{ color: '#6366f1', marginBottom: 24, fontWeight: 700, fontFamily: 'Inter, sans-serif', textAlign: 'center' }}>What brings you here? 🎯</h3>
            <div style={{ marginBottom: 20 }}>
              <label style={{ display: 'block', marginBottom: 6, color: '#374151', fontWeight: 500 }}>What are you looking for at this event?</label>
              <input
                type="text"
                name="lookingFor"
                value={form.lookingFor}
                onChange={handleChange}
                required
                placeholder={`e.g. ${lookingForExample}`}
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
              <label style={{ display: 'block', marginBottom: 6, color: '#374151', fontWeight: 500 }}>What do you bring?</label>
              <input
                type="text"
                name="whatYouBring"
                value={form.whatYouBring}
                onChange={handleChange}
                required
                placeholder={`e.g. ${whatYouBringExample}`}
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
              <label style={{ display: 'block', marginBottom: 6, color: '#374151', fontWeight: 500 }}>Help break the ice! What kind of stuff is your spice?</label>
              <input
                type="text"
                name="interests"
                value={form.interests}
                onChange={handleChange}
                required
                placeholder={`e.g. ${interestsExample}`}
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
            <div style={{ display: 'flex', justifyContent: 'space-between', gap: 8 }}>
              <button
                onClick={handleBack}
                style={{
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
                type="button"
              >
                Back
              </button>
              <button
                type="submit"
                style={{
                  padding: '12px 24px',
                  background: 'linear-gradient(90deg, #6366f1 0%, #818cf8 100%)',
                  color: 'white',
                  fontWeight: 700,
                  fontSize: 16,
                  border: 'none',
                  borderRadius: 8,
                  boxShadow: '0 2px 8px rgba(99,102,241,0.08)',
                  cursor: 'pointer',
                  fontFamily: 'Inter, sans-serif',
                }}
              >
                Next
              </button>
            </div>
          </form>
        )}
        {step === 3 && (
          <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: 32, textAlign: 'center' }}>
              <span style={{ fontSize: 32, color: '#6366f1' }}>🎉</span>
              <h3 style={{ color: '#6366f1', margin: '16px 0 8px', fontWeight: 700 }}>You're all set!</h3>
              <p style={{ color: '#374151', fontSize: 16 }}>Press submit to send your answers and get matched.</p>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', gap: 8 }}>
              <button
                onClick={handleBack}
                style={{
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
                type="button"
              >
                Back
              </button>
              <button
                type="submit"
                style={{
                  padding: '12px 24px',
                  background: 'linear-gradient(90deg, #6366f1 0%, #818cf8 100%)',
                  color: 'white',
                  fontWeight: 700,
                  fontSize: 16,
                  border: 'none',
                  borderRadius: 8,
                  boxShadow: '0 2px 8px rgba(99,102,241,0.08)',
                  cursor: 'pointer',
                  fontFamily: 'Inter, sans-serif',
                }}
              >
                Submit
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};

export default FormPage; 