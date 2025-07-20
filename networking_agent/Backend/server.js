const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Path to the Submissions directory
const SUBMISSIONS_DIR = path.join(__dirname, '..', 'Submissions');

// Ensure the Submissions directory exists
if (!fs.existsSync(SUBMISSIONS_DIR)) {
  fs.mkdirSync(SUBMISSIONS_DIR, { recursive: true });
  console.log(`Created Submissions directory at: ${SUBMISSIONS_DIR}`);
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

    // Create user directory
    const userDir = path.join(SUBMISSIONS_DIR, userId);
    if (!fs.existsSync(userDir)) {
      fs.mkdirSync(userDir, { recursive: true });
      console.log(`Created user directory: ${userDir}`);
    }

    // Create the JSON file path
    const jsonFilePath = path.join(userDir, 'submission.json');
    
    // Write the JSON data to file
    fs.writeFileSync(jsonFilePath, JSON.stringify(formData, null, 2));
    
    console.log(`User data saved successfully for ${userId} at: ${jsonFilePath}`);
    
    res.status(200).json({ 
      success: true, 
      message: 'User data saved successfully',
      userId: userId,
      filePath: jsonFilePath
    });

  } catch (error) {
    console.error('Error saving user data:', error);
    res.status(500).json({ 
      error: 'Failed to save user data',
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
  console.log(`Submissions directory: ${SUBMISSIONS_DIR}`);
}); 