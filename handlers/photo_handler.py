from telegram import Update
from telegram.ext import ContextTypes
from utils.image_processing import async_process_image

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Ваше фото обрабатывается, это может занять некоторое время...")

    photo = await update.message.photo[-1].get_file()
    photo_data = await photo.download_as_bytearray()

    processed_image = await async_process_image(photo_data)

    await update.message.reply_photo(photo=processed_image)
