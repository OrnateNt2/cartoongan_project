
# CartoonGAN Telegram Bot

![Telegram](https://img.shields.io/badge/Telegram-Bot-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## Overview

This project is a Telegram bot that converts user-uploaded photos into cartoon-style images using the CartoonGAN model. The bot is designed to handle multiple users simultaneously, providing a seamless and engaging experience.

## Features

- **Photo to Cartoon Conversion:** Converts user photos into cartoon-style images.
- **Asynchronous Processing:** Supports multiple users simultaneously with asynchronous image processing.
- **Simple and Secure:** Token management via `.env` file, ensuring security.

## Setup

### Prerequisites

- Python 3.8+
- Telegram Bot API Token
- Libraries listed in `requirements.txt`

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/OrnateNt2/cartoongan_project.git
   cd cartoon-telegram-bot
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add your Telegram bot token:

   ```
   TELEGRAM_BOT_TOKEN=your_token_here
   ```

4. Run the bot:

   ```bash
   python bot.py
   ```

## Project Structure

```plaintext
cartoon_bot/
│
├── bot.py                 # Main bot script
├── handlers/
│   ├── __init__.py        # Initialize package
│   ├── start_handler.py   # /start command handler
│   └── photo_handler.py   # Photo handling logic
├── utils/
│   ├── __init__.py        # Initialize package
│   ├── model.py           # Model loading and processing
│   └── image_processing.py# Image processing functions
└── requirements.txt       # Project dependencies
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Python Telegram Bot](https://python-telegram-bot.readthedocs.io/)
- [CartoonGAN](https://arxiv.org/abs/1808.08585)
