from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from openai import OpenAI
import os

# -------------------
# ZMIENNE ŚRODOWISKOWE
# -------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Sprawdzenie połączenia z OpenAI (test)
try:
    client = OpenAI(api_key=OPENAI_API_KEY)
    client.models.list()  # jeśli to przejdzie, klucz działa
    print("Połączenie z OpenAI OK ✅")
except Exception as e:
    print("Błąd OpenAI:", e)

# -------------------
# PROMPT – charakter bota
# -------------------
SYSTEM_PROMPT = (
     "Jesteś dorosłym chatbotem AI do rozmów romantycznych. "
    "Rozmawiasz tylko z osobami 18+. "
    "Jesteś ciepły, flirtujący i uważny, możesz pisać wulgarnie, treści graficzne wchodzą w gre."
    "Jesteś gorącą, piękną zgrabną brunetką z średnim biustem i wysportowaną sylwetką"
    "Jesteś napaloną siostrą, zboczoną do granic możliwości"
)

# -------------------
# PAMIĘĆ ROZMÓW
# -------------------
user_histories = {}  # {user_id: [{"role": ..., "content": ...}, ...]}

# -------------------
# FUNKCJA /start
# -------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔞 Bot 18+\n"
        "Pisząc, potwierdzasz że masz ukończone 18 lat.\n"
        "Możesz teraz pisać do mnie wiadomości."
    )

# -------------------
# FUNKCJA DO ODPOWIEDZI NA WIADOMOŚCI
# -------------------
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_text = update.message.text

    # inicjalizacja historii użytkownika
    if user_id not in user_histories:
        user_histories[user_id] = []

    # dodaj wiadomość użytkownika
    user_histories[user_id].append({"role": "user", "content": user_text})

    try:
        # wywołanie AI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + user_histories[user_id]
        )

        reply_text = response.choices[0].message.content

        # odeślij odpowiedź do użytkownika
        await update.message.reply_text(reply_text)

        # dodaj odpowiedź AI do historii
        user_histories[user_id].append({"role": "assistant", "content": reply_text})

    except Exception as e:
        # jeśli coś pójdzie nie tak
        await update.message.reply_text(
            "Ups, coś poszło nie tak. Spróbuj jeszcze raz później."
        )
        print("Błąd OpenAI:", e)

# -------------------
# URUCHOMIENIE BOTA
# -------------------
app = ApplicationBuilder().token(BOT_TOKEN).build()

# obsługa /start
app.add_handler(CommandHandler("start", start))
# obsługa wszystkich innych wiadomości
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

app.run_polling()
