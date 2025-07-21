const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Path to the Submissions directory and the main submissions file
const SUBMISSIONS_DIR = path.join(__dirname, '..', 'Database');
const SUBMISSIONS_FILE = path.join(SUBMISSIONS_DIR, 'all_submissions.json');

// Ensure the Submissions directory exists
if (!fs.existsSync(SUBMISSIONS_DIR)) {
  fs.mkdirSync(SUBMISSIONS_DIR, { recursive: true });
  console.log(`Created Submissions directory at: ${SUBMISSIONS_DIR}`);
}

// Initialize the submissions file if it doesn't exist
if (!fs.existsSync(SUBMISSIONS_FILE)) {
  fs.writeFileSync(SUBMISSIONS_FILE, JSON.stringify([], null, 2));
  console.log(`Created submissions file at: ${SUBMISSIONS_FILE}`);
}

// Endpoint to save user data
app.post('/api/save-user-data', (req, res) => {
  try {
    const { userId, formData } = req.body;
    
    if (!userId || !formData) {
      return res.status(400).json({ 
        error: 'Missing required fields: userId and formData' 
      });
    }

    // Transform form data to the required format
    const transformedData = {
      user_id: userId,
      first_name: formData.responses.find(r => r.question === "First Name")?.answer || "",
      last_name: formData.responses.find(r => r.question === "Last Name")?.answer || "",
      value_in: formData.responses.find(r => r.question === "What do you bring?")?.answer || "",
      value_out: formData.responses.find(r => r.question === "What are you looking for at this event?")?.answer || "",
      ice_break: formData.responses.find(r => r.question === "Help break the ice! What kind of stuff is your spice?")?.answer || "",
      linkedin_url: formData.responses.find(r => r.question === "LinkedIn Profile")?.answer || ""
    };

    // Read existing submissions
    let allSubmissions = [];
    try {
      const existingData = fs.readFileSync(SUBMISSIONS_FILE, 'utf8');
      allSubmissions = JSON.parse(existingData);
    } catch (error) {
      console.log('No existing submissions file found, starting fresh');
    }

    // Check if user already exists and update, otherwise add new
    const existingUserIndex = allSubmissions.findIndex(
      submission => submission.user_id === userId
    );

    if (existingUserIndex !== -1) {
      // Update existing user data
      allSubmissions[existingUserIndex] = transformedData;
      console.log(`Updated existing user data for ${userId}`);
    } else {
      // Add new user data
      allSubmissions.push(transformedData);
      console.log(`Added new user data for ${userId}`);
    }
    
    // Write all submissions back to file
    fs.writeFileSync(SUBMISSIONS_FILE, JSON.stringify(allSubmissions, null, 2));
    
    console.log(`User data saved successfully for ${userId} in: ${SUBMISSIONS_FILE}`);
    
    res.status(200).json({ 
      success: true, 
      message: 'User data saved successfully',
      userId: userId,
      totalSubmissions: allSubmissions.length
    });

  } catch (error) {
    console.error('Error saving user data:', error);
    res.status(500).json({ 
      error: 'Failed to save user data',
      details: error.message 
    });
  }
});

// Endpoint to get all submissions
app.get('/api/submissions', (req, res) => {
  try {
    if (!fs.existsSync(SUBMISSIONS_FILE)) {
      return res.json([]);
    }
    
    const data = fs.readFileSync(SUBMISSIONS_FILE, 'utf8');
    const allSubmissions = JSON.parse(data);
    
    res.json(allSubmissions);
  } catch (error) {
    console.error('Error reading submissions:', error);
    res.status(500).json({ 
      error: 'Failed to read submissions',
      details: error.message 
    });
  }
});

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', message: 'Backend server is running' });
});

// Start server
app.listen(PORT, () => {
  console.log(`Backend server running on http://localhost:${PORT}`);
  console.log(`Submissions file: ${SUBMISSIONS_FILE}`);
}); 