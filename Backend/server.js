const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const app = express();
const PORT = 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Path to the Submissions directory
const SUBMISSIONS_DIR = path.join(__dirname, '..', 'Submissions');
const AGENTS_DIR = path.join(__dirname, '..', 'Agents');

// Ensure the Submissions directory exists
if (!fs.existsSync(SUBMISSIONS_DIR)) {
  fs.mkdirSync(SUBMISSIONS_DIR, { recursive: true });
  console.log(`Created Submissions directory at: ${SUBMISSIONS_DIR}`);
}

// Helper function to run Python scripts
function runPythonScript(scriptPath, args = []) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python', [scriptPath, ...args]);
    
    let stdout = '';
    let stderr = '';
    
    pythonProcess.stdout.on('data', (data) => {
      stdout += data.toString();
    });
    
    pythonProcess.stderr.on('data', (data) => {
      stderr += data.toString();
    });
    
    pythonProcess.on('close', (code) => {
      if (code === 0) {
        try {
          // Try to parse JSON from stdout
          const result = JSON.parse(stdout.trim());
          resolve(result);
        } catch (e) {
          resolve({ success: true, output: stdout.trim() });
        }
      } else {
        reject(new Error(`Python script failed with code ${code}: ${stderr}`));
      }
    });
    
    pythonProcess.on('error', (error) => {
      reject(error);
    });
  });
}

// Endpoint to save user data and process with agents
app.post('/api/save-user-data', async (req, res) => {
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
    
    // Process user data with Python agents
    try {
      const mainScriptPath = path.join(AGENTS_DIR, 'main.py');
      const result = await runPythonScript(mainScriptPath, [
        '--action', 'process_user',
        '--data', JSON.stringify(formData)
      ]);
      
      res.status(200).json({ 
        success: true, 
        message: 'User data saved and processed successfully',
        userId: userId,
        filePath: jsonFilePath,
        processingResult: result
      });
    } catch (pythonError) {
      console.error('Python processing error:', pythonError);
      res.status(200).json({ 
        success: true, 
        message: 'User data saved successfully (processing failed)',
        userId: userId,
        filePath: jsonFilePath,
        processingError: pythonError.message
      });
    }

  } catch (error) {
    console.error('Error saving user data:', error);
    res.status(500).json({ 
      error: 'Failed to save user data',
      details: error.message 
    });
  }
});

// Endpoint to generate matches for all users
app.post('/api/generate-matches', async (req, res) => {
  try {
    console.log('Generating matches for all users...');
    
    const mainScriptPath = path.join(AGENTS_DIR, 'main.py');
    const result = await runPythonScript(mainScriptPath, [
      '--action', 'generate_matches'
    ]);
    
    res.status(200).json({
      success: true,
      message: 'Matches generated successfully',
      result: result
    });
  } catch (error) {
    console.error('Error generating matches:', error);
    res.status(500).json({
      error: 'Failed to generate matches',
      details: error.message
    });
  }
});

// Endpoint to get matches for a specific user
app.get('/api/get-matches/:userId', async (req, res) => {
  try {
    const { userId } = req.params;
    
    console.log(`Getting matches for user: ${userId}`);
    
    const mainScriptPath = path.join(AGENTS_DIR, 'main.py');
    const result = await runPythonScript(mainScriptPath, [
      '--action', 'get_user_matches',
      '--user_id', userId
    ]);
    
    res.status(200).json({
      success: true,
      result: result
    });
  } catch (error) {
    console.error('Error getting user matches:', error);
    res.status(500).json({
      error: 'Failed to get user matches',
      details: error.message
    });
  }
});

// Endpoint to get all matches data
app.get('/api/get-all-matches', async (req, res) => {
  try {
    console.log('Getting all matches data...');
    
    const mainScriptPath = path.join(AGENTS_DIR, 'main.py');
    const result = await runPythonScript(mainScriptPath, [
      '--action', 'get_all_matches'
    ]);
    
    res.status(200).json({
      success: true,
      result: result
    });
  } catch (error) {
    console.error('Error getting all matches:', error);
    res.status(500).json({
      error: 'Failed to get all matches',
      details: error.message
    });
  }
});



// Endpoint to get sample data
app.get('/api/get-sample-data', async (req, res) => {
  try {
    console.log('Getting sample data...');
    
    const mainScriptPath = path.join(AGENTS_DIR, 'main.py');
    const result = await runPythonScript(mainScriptPath, [
      '--action', 'get_sample_data'
    ]);
    
    res.status(200).json({
      success: true,
      result: result
    });
  } catch (error) {
    console.error('Error getting sample data:', error);
    res.status(500).json({
      error: 'Failed to get sample data',
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
  console.log(`Agents directory: ${AGENTS_DIR}`);
}); 