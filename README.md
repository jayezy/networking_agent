# Networking Agent System

A comprehensive networking matchmaking system that uses AI agents to process user data, extract LinkedIn information, and generate intelligent matches based on give/take preferences.

## 🚀 Complete Workflow

### 1. User Input Collection (Frontend)
- Users fill out a form with their name, LinkedIn URL, what they're looking for, and what they bring
- Form data is sent to the backend and saved to JSON files

### 2. LinkedIn Data Processing (Python Agents)
- **LinkedIn Connector**: Scrapes LinkedIn profiles using Exa API and GMICloud
- **LinkedIn Processor**: Generates summaries and tags from LinkedIn data
- **Profile Analyzer**: Creates comprehensive profile analysis with networking insights

### 3. Match Generation (AI Agents)
- **Matchmaking Agent**: Uses semantic similarity and LLM scoring to find matches
- **Give/Take Evaluator**: Assesses the quality of user give/take statements
- **Orchestrator**: Coordinates all agents and manages the workflow

### 4. Results Display (Frontend)
- Match results are displayed with user information, match scores, LinkedIn summaries, and tags
- Results are sorted by match percentage in descending order

## 📁 Project Structure

```
networking_agent/
├── Agents/                    # Python AI agents
│   ├── main.py               # Main orchestration script
│   ├── data_manager.py       # JSON file operations
│   ├── linkedin_connector.py # LinkedIn scraping
│   ├── linkedin_processor_agent.py # LinkedIn data processing
│   ├── profile_analyzer_agent.py # Profile analysis
│   ├── matchmaking_agent.py  # Match generation
│   ├── orchestrator.py       # Workflow coordination
│   └── api_handler.py        # Backend integration
├── Backend/                  # Node.js server
│   └── server.js            # Express server with API endpoints
├── UI/                      # React frontend
│   └── src/
│       ├── FormPage.jsx     # User input form
│       └── ProcessedInfoPage.jsx # Match results display
└── Database/                # Data storage
    ├── sample_data.json     # User data
    ├── processed_data.json  # Processed user data
    └── matches_data.json    # Match results
```

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 14+
- Required API keys (GMICloud, Exa, OpenAI)

### 1. Install Python Dependencies
```bash
cd networking_agent/Agents
pip install -r requirements.txt
```

### 2. Install Node.js Dependencies
```bash
cd networking_agent/Backend
npm install

cd ../UI
npm install
```

### 3. Configure Environment Variables
Create a `.env` file in the `Agents` directory:
```
OPENAI_API_KEY=your_openai_api_key
GMICLOUD_API_KEY=your_gmicloud_api_key
EXA_API_KEY=your_exa_api_key
```

### 4. Start the Services

#### Backend Server
```bash
cd networking_agent/Backend
npm start
```

#### Frontend Development Server
```bash
cd networking_agent/UI
npm start
```

## 🔄 API Endpoints

### Backend Endpoints

#### POST `/api/save-user-data`
Process new user registration and LinkedIn data
```json
{
  "userId": "user_123",
  "formData": {
    "responses": [
      {"question": "First Name", "answer": "John"},
      {"question": "LinkedIn Profile", "answer": "https://linkedin.com/in/john"},
      {"question": "What are you looking for?", "answer": "mentorship"},
      {"question": "What do you bring?", "answer": "technical expertise"}
    ]
  }
}
```

#### POST `/api/generate-matches`
Generate matches for all users in the system

#### GET `/api/get-matches/:userId`
Get matches for a specific user

#### GET `/api/get-all-matches`
Get all match results

#### GET `/api/get-dashboard/:userId`
Get comprehensive dashboard data for a user

#### GET `/api/get-sample-data`
Get current sample data

## 🤖 Agent Workflow

### 1. Data Manager
- Manages JSON file operations
- Converts form data to user data format
- Handles user data persistence

### 2. LinkedIn Connector
- Scrapes LinkedIn profiles using Exa API
- Extracts structured data using GMICloud LLM
- Returns comprehensive profile information

### 3. LinkedIn Processor
- Generates professional summaries
- Creates relevant tags
- Analyzes profile content

### 4. Profile Analyzer
- Creates comprehensive profile analysis
- Generates networking insights
- Provides career stage and persona assessment

### 5. Matchmaking Agent
- Uses semantic similarity for initial scoring
- Applies LLM-based evaluation
- Implements reflection validation
- Returns ranked match list

### 6. Orchestrator
- Coordinates all agents
- Manages async operations
- Handles error recovery

## 📊 Data Flow

1. **User Input** → Frontend Form
2. **Form Data** → Backend API
3. **Backend** → Python Agents (via subprocess)
4. **LinkedIn Scraping** → Profile Data Extraction
5. **Profile Analysis** → Comprehensive Insights
6. **Match Generation** → Semantic + LLM Scoring
7. **Results** → JSON Storage
8. **Frontend Display** → Match Cards with Details

## 🎯 Match Generation Algorithm

### Scoring Components
1. **Semantic Similarity** (30%): Cosine similarity between give/take embeddings
2. **LLM Evaluation** (70%): GPT-4 based match quality assessment

### Match Criteria
- User's "take" matches other's "give"
- User's "give" matches other's "take"
- Complementary skills and interests
- Career stage compatibility
- Networking persona alignment

### Output Format
```json
{
  "name": "John Doe",
  "linkedin_url": "https://linkedin.com/in/john",
  "title": "Senior Software Engineer",
  "summary": "Experienced developer with expertise in...",
  "tags": ["Python", "Cloud", "AI"],
  "match_percentage": 85,
  "match_score": 0.85,
  "reasoning": "Strong technical complementarity..."
}
```

## 🚀 Usage Example

### 1. Start the System
```bash
# Terminal 1: Backend
cd networking_agent/Backend && npm start

# Terminal 2: Frontend
cd networking_agent/UI && npm start
```

### 2. Add Users
- Navigate to `http://localhost:3000`
- Fill out the form with user information
- Submit to process LinkedIn data

### 3. Generate Matches
- Use the "Generate Matches" button or call the API
- View results in the ProcessedInfoPage

### 4. View Results
- Match cards show user information, scores, and reasoning
- Click LinkedIn profiles to view full details
- Tags help identify key skills and interests

## 🔧 Configuration

### API Keys
Update the API keys in the respective agent files:
- `linkedin_connector.py`: GMICloud and Exa API keys
- `matchmaking_agent.py`: OpenAI API key

### Model Settings
- LinkedIn processing: GPT-4 for structured extraction
- Matchmaking: GPT-4o for evaluation
- Embeddings: OpenAI text-embedding-ada-002

## 🐛 Troubleshooting

### Common Issues
1. **API Key Errors**: Ensure all API keys are properly configured
2. **LinkedIn Scraping**: Check Exa API quota and profile accessibility
3. **Python Dependencies**: Verify all packages are installed
4. **Backend Connection**: Ensure Node.js server is running on port 3001

### Debug Mode
Run the main script directly for debugging:
```bash
cd networking_agent/Agents
python main.py --action generate_matches
```

## 📈 Future Enhancements

- Real-time match updates
- Advanced filtering options
- Match history tracking
- Integration with calendar systems
- Mobile app development
- Advanced analytics dashboard

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details. 