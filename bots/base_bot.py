from telegram.ext import CommandHandler, ContextTypes, Application, JobQueue


class BaseBot:
    def __init__(self, token: str, channel_ids: list):
        self.token = token
        self.channel_ids = channel_ids
        # Enable JobQueue by setting it explicitly in the application
        self.application = Application.builder().token(token).build()

    async def start(self, update, context: ContextTypes.DEFAULT_TYPE):
        """Respond to the /start command."""
        await update.message.reply_text("Hello! This bot provides updates on TRX and BTC prices.")

    def setup(self):
        """Set up common handlers."""
        self.application.add_handler(CommandHandler("start", self.start))
        print("BaseBot handlers registered.")

    def run_polling(self):
        """Start the polling loop."""
        print("Polling started.")
        self.application.run_polling()
