from typing import Final
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes 
from summary_video import summarize_video
from summary_article import summarize_article
from dotenv import load_dotenv
import os 

load_dotenv()

token = os.getenv("TOKEN")
bot_username = os.getenv("BOT_USERNAME")

TOKEN: Final = token
BOT_USERNAME: Final = bot_username

# Command handlers

# Handler for the /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот для создания краткого содержания.")
    await update.message.reply_text("Для суммаризации видео используй команду /summarize_video. Для суммаризации статьи используй команду /summarize_article")

# Handler for the /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
        Список команд:
        /start - Запуск бота
        /help - Получить список команд
        /summarize_video - Создать краткое содержание видео
        /summarize_article - Создать краткое содержание статьи
    """)

# Handler for the /summarize_video command
async def summarize_video_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    # Check if the message contains a YouTube link
    if 'youtube.com' not in text and 'youtu.be' not in text:
        context.user_data['waiting_for_video_link'] = True
        await update.message.reply_text("Пожалуйста, отправьте ссылку на Youtube-видео.")

# Handler for the /summarize_article command
async def summarize_article_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    # Check if the command was used correctly
    if text.strip() == '/summarize_article':
        context.user_data['waiting_for_article_text'] = True
        await update.message.reply_text("Пожалуйста, отправьте ссылку на текст статьи для суммаризации.")
    else:
        await update.message.reply_text("Неверная команда. Используйте /summarize_article для суммаризации статьи.")

# Handler for incoming messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'waiting_for_video_link' in context.user_data:
        text_url = update.message.text
        # Check if the message contains a YouTube link
        if 'youtube.com' in text_url or 'youtu.be' in text_url:
            await update.message.reply_text("Ссылка принята, обработка...")
            result = summarize_video(text_url)
            await update.message.reply_text(result)

            # Clear the waiting state for video link
            del context.user_data['waiting_for_video_link']
        else:
            await update.message.reply_text("Пожалуйста, отправьте ссылку на Youtube-видео.")
    elif 'waiting_for_article_text' in context.user_data:
        text_url = update.message.text
        await update.message.reply_text("Ссылка принята, обработка...")
        result = summarize_article(text_url)
        await update.message.reply_text(result)

        # Clear the waiting state for article text
        del context.user_data['waiting_for_article_text']
    else:
        await update.message.reply_text("Для суммаризации видео, используй команду /summarize_video. Для суммаризации статьи, используй команду /summarize_article.")

# Handler for errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('summarize_video', summarize_video_command))
    app.add_handler(CommandHandler('summarize_article', summarize_article_command))  # Adding summarize_article command

    # Add message handler
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Add error handler
    app.add_error_handler(error)

    # Start polling for updates
    print("Polling...")
    app.run_polling(poll_interval=3)