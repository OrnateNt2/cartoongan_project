import os
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from handlers.start_handler import start
from handlers.photo_handler import handle_photo
from dotenv import load_dotenv

load_dotenv()  # Загрузка переменных окружения из .env

def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    application.run_polling()

if __name__ == '__main__':
    main()
