# Two Provider Cost Tracker

## Project Overview
This Python project compares responses from two AI providers: Google Gemini and Groq. It sends the same prompt to both providers and displays their responses, token usage, response time, and estimated API cost.

## Features
- Sends the same prompt to Gemini and Groq.
- Displays AI-generated replies.
- Tracks input and output tokens.
- Measures response time in seconds.
- Calculates estimated API costs in USD.
- Saves results in a JSON file.

## Requirements
- Python
- UV package manager
- Gemini API key
- Groq API key

## Installation

1. Clone or download this repository.
2. Open the project folder in the terminal.
3. Install dependencies:

```bash
uv sync
```

4. Create a `.env` file in the project root.
5. Add your API keys and model names:

```env
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
GEMINI_MODEL=your_gemini_model
GROQ_MODEL=your_groq_model
```

## How to Run

Run the following command:

```bash
uv run tracker.py "Explain what an electrical relay does in simple words."
```

Replace the prompt with any question you want to test.

## Output
The program displays:
- Gemini response
- Groq response
- Input and output token counts
- Response time
- Estimated cost in USD

The results are saved in `results.json`.

## What I Learned

1. I learned how to connect Python applications with AI APIs using Gemini and Groq.
2. I learned how to measure token usage, response time, and calculate API costs.
3. I learned how to store API results in JSON and protect secret API keys using environment variables.

## Security
API keys are stored in `.env`. This file should never be uploaded to GitHub. The `.env.example` file contains placeholder values only.