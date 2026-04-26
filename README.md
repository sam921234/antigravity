# Vitality AI - Fitness Dashboard

🏋️‍♂️ **Vitality AI** is an intelligent fitness coaching application powered by Google's Gemini API. It provides personalized workout guidance, activity tracking, and AI-driven fitness insights through an intuitive Streamlit web interface.

## Features

- **Personalized Fitness Coaching**: AI-powered coaching based on your age, fitness goals, and workout history
- **Activity Logging**: Track your workouts, duration, and how you felt during each session
- **Interactive Dashboard**: View your fitness metrics and progress with beautiful visualizations
- **User Profiles**: Create and manage multiple user profiles with different fitness goals
- **Chat-Based Coaching**: Have personalized conversations with your AI fitness coach
- **Progress Analytics**: Visualize your recent workouts and activity patterns
- **Persistent Data Storage**: Your fitness data is automatically saved and loaded
- **Automatic Model Failover**: Intelligent fallback system for LLM model selection

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Google Gemini API key

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sam921234/antigravity.git
   cd antigravity
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure API Key**:
   - Create a `.env` file in the root directory:
     ```
     GEMINI_API_KEY=your_api_key_here
     LLM_MODEL=gemini-2.5-flash
     ```
   - Alternatively, if deploying on Streamlit Cloud, add these to your Streamlit secrets

6. **Get your Gemini API Key**:
   - Visit [Google AI Studio](https://aistudio.google.com/apikey)
   - Create a new API key and paste it in your `.env` file

## Usage

### Running Locally

Start the Streamlit application:

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

### Using the Dashboard

1. **Sign In/Register**:
   - Enter your username to create a new profile or access an existing one
   - No password required for local testing

2. **Set Your Profile**:
   - Enter your age and select your fitness goal
   - This information will be used to personalize coaching

3. **Log Activities**:
   - Enter the type of activity (e.g., "Running", "Weight Training", "Yoga")
   - Specify duration in minutes
   - Record how you felt during the activity

4. **Get Coaching**:
   - Chat with your AI fitness coach
   - Ask for workout recommendations, tips, or feedback
   - The coach will reference your recent activities

5. **View Analytics**:
   - See visualizations of your recent workouts
   - Track trends in your fitness activities

## Project Structure

```
antigravity/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── README.md              # This file
├── backend/
│   ├── __init__.py
│   └── llm_service.py     # Google Gemini API integration & coaching logic
└── data/
    └── [username].json    # User profiles and activity logs (auto-generated)
```

## Requirements

See `requirements.txt` for full list:
- **streamlit** - Web framework for the dashboard UI
- **google-genai** - Google Generative AI SDK for Gemini API
- **python-dotenv** - Environment variable management
- **pandas** - Data processing and analysis
- **plotly** - Interactive charts and visualizations

## API Models

The application supports multiple Google Gemini models with automatic failover:
- `gemini-2.5-flash` (recommended)
- `gemini-3.1-flash-lite-preview`
- `gemini-2.0-flash`
- `gemini-flash-lite-latest`

## Deployment

### Deploy on Streamlit Cloud

1. Push your code to GitHub (already done!)
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Create an account and connect your GitHub repository
4. Add secrets:
   - Click "Advanced settings"
   - Add `GEMINI_API_KEY` and `LLM_MODEL` to secrets
5. Deploy!

## Safety Features

- **Medical Disclaimer**: The AI coach explicitly avoids giving medical advice
- **Safety Checks**: Refuses extreme or dangerous diet/exercise requests
- **Professional Recommendations**: Directs users to doctors for pain or injuries
- **Data Privacy**: All user data is stored locally (when running locally)

## Troubleshooting

### API Key Issues
- Verify your `GEMINI_API_KEY` is set correctly in `.env`
- Make sure the API key has Generative AI access enabled
- Check that you haven't exceeded your API quota

### Model Not Found Errors
- The app will automatically try fallback models
- If all models fail, check your internet connection and API key validity

### Data Not Saving
- Ensure the `data/` directory exists and is writable
- Check file permissions on your system

## License

This project is open source and available for personal use.

## Contributing

Feel free to fork, modify, and improve this project!

---

Built with ❤️ using Streamlit and Google Gemini AI
