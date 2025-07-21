# Backend Server

This is the backend server for the networking event matching application.

## Features

- **POST /api/save-user-data**: Saves user form submissions to individual directories
- **GET /api/health**: Health check endpoint

## Directory Structure

User submissions are saved to:
```
networking_agent/networking_agent/Submissions/
├── user_1703123456789_abc123def/
│   └── submission.json
├── user_1703123456790_def456ghi/
│   └── submission.json
└── ...
```

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start the server:
```bash
npm start
```

The server will run on `http://localhost:3001`

## API Endpoints

### POST /api/save-user-data
Saves user form data to a JSON file.

**Request Body:**
```json
{
  "userId": "user_1703123456789_abc123def",
  "formData": {
    "userId": "user_1703123456789_abc123def",
    "timestamp": "2023-12-21T10:30:45.123Z",
    "responses": [
      {"question": "First Name", "answer": "John"},
      {"question": "Last Name", "answer": "Doe"}
    ]
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "User data saved successfully",
  "userId": "user_1703123456789_abc123def",
  "filePath": "/path/to/submission.json"
}
```

### GET /api/health
Health check endpoint.

**Response:**
```json
{
  "status": "OK",
  "message": "Backend server is running"
}
``` 