# Networking Matchmaking System

A sophisticated AI-powered networking matchmaking system that processes LinkedIn profiles and finds optimal connections between professionals based on their skills, experience, and networking goals.

## 🚀 Features

- **LinkedIn Profile Processing**: Automatically extracts and analyzes LinkedIn profile data
- **AI-Generated Summaries**: Creates concise professional summaries and relevant tags
- **Semantic Matching**: Uses OpenAI embeddings for partial/semantic matching
- **Reflection-Based Validation**: LLM-powered validation of match quality
- **LangGraph Workflow**: Modular, agentic workflow for robust matchmaking
- **Rich Match Output**: Detailed recommendations with scores and reasoning

## 🏗️ Architecture

The system is built with a modular, agent-based architecture:

```
├── main.py                    # Main orchestration file
├── linkedin_processor_agent.py # LinkedIn profile processing agent
├── matchmaking_agent.py       # Matchmaking workflow agent
├── data_manager.py           # Data management utilities
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

### Agents

1. **LinkedInProcessorAgent**: 
   - Processes raw LinkedIn data
   - Generates professional summaries and tags
   - Extracts "give" and "ask" from profiles

2. **MatchmakingAgent**:
   - LangGraph workflow for matchmaking
   - Semantic similarity scoring
   - Reflection-based validation
   - Multi-round refinement

3. **DataManager**:
   - Sample data management
   - Profile validation
   - Data utilities

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd networking-matchmaking-system
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## 🚀 Usage

### Basic Usage

Run the system with sample data:
```bash
python main.py
```

### Command Line Options

```bash
# Run with sample data
python main.py sample

# Run with custom data example
python main.py custom

# Show help
python main.py help
```

### Programmatic Usage

```python
from main import NetworkingMatchmakingSystem

# Initialize the system
system = NetworkingMatchmakingSystem()

# Your LinkedIn data from scraping agent
linkedin_profiles = [
    {
        "name": "John Doe",
        "linkedin_url": "https://linkedin.com/in/johndoe",
        "title": "Senior Software Engineer",
        "bio": "Full-stack developer with 5+ years experience...",
        "experience": ["Senior Engineer at Company A", "Engineer at Company B"],
        "education": ["BS Computer Science, University X"]
    }
    # ... more profiles
]

# Process and find matches
results = system.run_with_custom_data(linkedin_profiles)
```

## 📊 Input Data Format

The system expects LinkedIn profile data in this format:

```python
{
    "name": "Full Name",
    "linkedin_url": "https://linkedin.com/in/username",
    "title": "Job Title at Company",  # Optional
    "bio": "Professional bio text",   # Optional
    "experience": [                   # Optional
        "Senior Engineer at Company A (2020-Present)",
        "Engineer at Company B (2018-2020)"
    ],
    "education": [                    # Optional
        "BS Computer Science, University X",
        "MS Data Science, University Y"
    ]
}
```

## 📈 Output Format

The system generates rich match recommendations:

```
Hi John Doe, here are your top networking matches:

**1. Jane Smith**
**Title:** AI Product Manager at TechCorp
**Summary:** Experienced product manager specializing in AI/ML products with 4+ years at Google. Offers mentorship and product strategy expertise.
**Tags:** AI/ML, Product Management, Google, Mentoring, Product Strategy
**LinkedIn:** https://linkedin.com/in/janesmith
**Recommendation Score:** 0.87
**Why:** Strong match due to complementary skills - you offer technical expertise while she seeks technical cofounders.

**Reflection:** These matches are well-justified based on complementary skills and mutual interests in technology.
```

## 🔧 Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_MODEL`: Model to use (default: "gpt-4o")

### Customization

You can customize various aspects:

1. **Matching Weights**: Adjust the blend of LLM and similarity scores in `matchmaking_agent.py`
2. **Top Matches**: Change the number of top matches returned
3. **Reflection Logic**: Modify the validation criteria
4. **Output Format**: Customize the display format

## 🤝 Integration with LinkedIn Scraper

To integrate with your LinkedIn scraping agent:

1. **Replace sample data**: Update `data_manager.py` with your scraped data
2. **Use the processing function**: Call `process_linkedin_data()` with your raw data
3. **Custom validation**: Add any specific validation rules for your data

Example integration:
```python
# From your LinkedIn scraper
scraped_profiles = your_scraper.get_profiles()

# Process with our system
system = NetworkingMatchmakingSystem()
processed_users = system.process_linkedin_data(scraped_profiles)
matches = system.find_matches_for_all_users(processed_users)
```

## 🔍 How It Works

1. **Profile Processing**: LinkedIn data is analyzed to extract key insights
2. **Summary Generation**: AI creates professional summaries and tags
3. **Give/Ask Extraction**: System determines what each person can offer and seek
4. **Semantic Matching**: Embeddings compute similarity between profiles
5. **LLM Scoring**: Advanced reasoning scores each potential match
6. **Reflection Validation**: Quality check ensures match relevance
7. **Output Generation**: Rich, detailed recommendations are produced

## 🧪 Testing

The system includes sample data for testing. Run:
```bash
python main.py sample
```

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For questions or issues, please open an issue on GitHub. 