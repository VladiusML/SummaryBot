# Summarization Bot

This project contains a bot that provides concise summaries of YouTube videos and web articles. It uses a llama3(8b) for generating summaries and translates them to Russian.

## Project Structure

- `summary_video.py`: Contains the function to summarize YouTube videos.
- `summary_article.py`: Contains the function to summarize web articles.
- `bot.py`: Contains the bot logic, including command handlers and message processing.
- `requirements.txt`: Lists the Python dependencies.

## Setup Instructions
### Prerequisites

- Python 3.8+
- Virtual environment tool (optional but recommended)
- A `.env` file with the following variables:
  - `TOKEN`: Your bot's API token.
  - `BOT_USERNAME`: Your bot's username.

### Steps

1. **Clone the repository**
   ```sh
   git clone https://github.com/yourusername/summarization-bot.git
   cd summarization-bot
   ```
2. **Set up a virtual environment**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate.bat`
   ```
3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Create a .env file in the project root**
   ```sh
   TOKEN=your_bot_token_here
   BOT_USERNAME=your_bot_username_here
   ```
5. **Set up the llama3**
   
   - Install [Ollama](https://ollama.com/).
   
   - Once Ollama is installed, you can run the following command to set up the 'llama3' model:
     ```sh
     ollama run llama3
     ```
7. **Run the bot**
   ```sh
   python bot.py
   ```
