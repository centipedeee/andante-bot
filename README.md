# Andante-Bot

A Python-based automation solution designed to scrape highlights from allstar.gg and deliver them to subscribed Telegram users.

---

## Features

- **Automated Video Parsing**:
  - Uses Selenium to scrape video links from specified websites.
  - Filters and identifies new video highlights.

- **Video Management**:
  - Downloads highlights using URLs and saves them locally.
  - Removes videos after they've been delivered to subscribers.

- **Telegram Bot Integration**:
  - Subscribes users to a notification system.
  - Sends downloaded video highlights directly to Telegram users via `aiogram`.

- **Concurrent Execution**:
  - Implements multiprocessing for simultaneous parsing and Telegram bot operations.

---

## How It Works

1. **Video Scraping**:
   - Selenium browser automation navigates to a specified webpage, extracts video URLs, and ensures only new clips are processed.

2. **Video Handling**:
   - Videos are downloaded with unique names and stored in a predefined directory.
   - Supports dynamic updates and appends new links to a file-based database.

3. **Telegram Bot**:
   - Allows users to subscribe by simply messaging the bot.
   - Automatically pushes scraped and downloaded video highlights to all subscribers.

4. **Asynchronous Design**:
   - Fully utilizes asynchronous operations (`asyncio`) for efficient execution.
   - Ensures smooth integration of scraping, downloading, and sending videos.

---

## Requirements

- **Installed Python Packages**:
  - [Selenium](https://pypi.org/project/selenium): For web scraping.
  - [Aiogram](https://docs.aiogram.dev/en/latest/): To interact with Telegram Bot API.
  - [Python-Dotenv](https://pypi.org/project/python-dotenv/): For managing environment variables.
  
- **Software**:
  - Python 3.13.0 or higher (may work on any >3.0).
  - Google Chrome and ChromeDriver (Ensure compatibility versions).

- **Environment Variables**:
  - The bot relies on environment variables defined in a `.env` file:
    - `TOKEN`: Telegram Bot API token.
    - `LINKS`: Comma-separated URL to scrape.

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/centipedeee/andante-bot.git
   cd andante-bot
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add the required environment variables:

   ```plaintext
   TOKEN=your-telegram-bot-token
   LINKS=url
   ```

4. Run the project:

   ```bash
   python andante-bot.py
   ```

---

## File Structure

```plaintext
andante-bot/
├── data/
│   ├── links             # Stores previously scraped video links
│   ├── users             # Stores Telegram user IDs
│   ├── videos/           # Directory where downloaded videos are saved
├── src/
│   ├── parser.py         # Handles web scraping and video downloading
│   ├── tgbot.py          # Manages the Telegram bot
├── .env                  # Environment variables
├── andante-bot.py        # Main entry point, runs parser & bot concurrently
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## Usage

- **Start the Bot**:
  Simply run the `andante-bot.py` script. It will concurrently:
  - Start scraping video links from the specified URLs (with 30m cooldown by default).
  - Send videos to Telegram users who have subscribed.

- **Subscribe to Highlights**:
  New users can subscribe by typing `/start` in the Telegram bot chat.

---

## Notes

- Supports asynchronous messaging for fast delivery of videos.
- Automatically handles video cleanup after sending them to users.
- Incorporates robust error handling for web scraping and Telegram messaging.

---


## License

This project is open-source and available under the [MIT License](LICENSE).