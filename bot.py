from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import asyncio
import logging

TOKEN = "7870279311:AAFSvNF8n4DX96GSqKy-OJPco0YQmAokz1M"

logging.basicConfig(level=logging.INFO)
scheduler = BackgroundScheduler()
scheduler.start()

# This function runs when a user types /start.
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Hello! I can remind you about events. Use /set YYYY-MM-DD HH:MM event_name to set a reminder.")

# Users will type /set followed by a date, time, and event name to set a reminder.
async def set_reminder(update: Update, context: CallbackContext) -> None:
    try:
        args = context.args
        if len(args) < 3:
            await update.message.reply_text("Usage: /set YYYY-MM-DD HH:MM event_name")
            return

        date_str = args[0]  # e.g., "2025-04-15"
        time_str = args[1]  # e.g., "14:30"
        event_name = " ".join(args[2:])  # e.g., "Doctor Appointment"

        # Convert to datetime object
        event_time = datetime.datetime.strptime(date_str + " " + time_str, "%Y-%m-%d %H:%M")

        # Schedule reminder
        scheduler.add_job(
            send_reminder, "date", run_date=event_time, args=[update.message.chat_id, event_name]
        )

        await update.message.reply_text(f"Reminder set for {event_name} at {event_time} ✅")

    except Exception as e:
        await update.message.reply_text("Error setting reminder. Make sure the format is correct.")
        logging.error(f"Error setting reminder: {e}")

# This function sends a reminder when the scheduled time arrives.
async def send_reminder(chat_id: int, event_name: str):
    """Sends the reminder message to the user."""
    app = Application.builder().token(TOKEN).build()
    await app.bot.send_message(chat_id=chat_id, text=f"⏰ Reminder: {event_name}")

# This sets up the bot and starts polling.
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("set", set_reminder))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
