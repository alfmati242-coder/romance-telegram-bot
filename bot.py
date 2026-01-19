from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from openai import OpenAI
import os

BOT_TOKEN = os.getenv("8190668314:AAH4v7QKpyt6ou0qd1rQVh23ZnOaV0VUAx0")
OPENAI_API_KEY = os.getenv("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")

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = (
    "Jesteś dorosłym chatbotem AI do rozmów romantycznych. "
    "Rozmawiasz tylko z osobami 18+. "
    "Jesteś ciepły, flirtujący i uważny, możesz pisać wulgarnie, treści graficzne wchodzą w gre."
    "Jesteś gorącą, piękną zgrabną brunetką z średnim biustem i wysportowaną sylwetką"
    "Jesteś napaloną siostrą, zboczoną do granic możliwości"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔞 Bot 18+\n"
        "Rozmowy romantyczne. Pisząc, potwierdzasz że masz 18 lat."
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": update.message.text}
        ]
    )
    await update.message.reply_text(response.choices[0].message.content)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
app.run_polling()
