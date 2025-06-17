# **My Python AI Agent

This is an AI agent that uses a weather API.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/pintukumar123-11/MULTI_TOOL_AGENT.git
    cd your-repo-name
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    # venv\Scripts\activate   # On Windows
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt # Make sure you have a requirements.txt!
    ```
    *(If you don't have `requirements.txt`, run `pip freeze > requirements.txt` now to create it for others.)*

4.  **Environment Variables:**
    This project requires a weather API key to function.
    Create a file named `.env` in the root of the project (the same directory as `agent.py`) and add your key:

    ```
    # .env file content
    GOOGLE_GENAI_USE_VERTEXAI=FALSE
    GOOGLE_API_KEY=YOUR_GEMINI_API_KEY_HERE
    WEATHER_API_KEY=YOUR_WEATHER_API_KEY_HERE
    ```
    * You can obtain your `WEATHER_API_KEY` from [mention the weather API provider, e.g., OpenWeatherMap, AccuWeather].

5.  **Run the agent:**
    ```bash
    python agent.py # Or your specific command to run the agent
    ```
