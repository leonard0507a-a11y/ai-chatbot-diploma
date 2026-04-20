import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

import openai

# ====== ENV ======
TOKEN = os.getenv("TELEGRAM_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

# ====== DB ======
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String, unique=True)

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    text = Column(Text)
    role = Column(String)

Base.metadata.create_all(engine)

# ====== DB FUNCTIONS ======
def save_message(user_id, text, role):
    session = Session()
    msg = Message(user_id=user_id, text=text, role=role)
    session.add(msg)
    session.commit()
    session.close()

def get_history(user_id):
    session = Session()
    msgs = session.query(Message).filter_by(user_id=user_id).all()
    session.close()
    return [{"role": m.role, "content": m.text} for m in msgs]

# ====== AI ======
def ask_ai(user_id, text):
    history = get_history(user_id)

    history.append({"role": "user", "content": text})

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ты менеджер по продаже онлайн курсов."},
            *history
        ]
    )

    answer = response["choices"][0]["message"]["content"]

    save_message(user_id, text, "user")
    save_message(user_id, answer, "assistant")

    return answer

# ====== TELEGRAM ======
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    text = update.message.text

    answer = ask_ai(user_id, text)

    await update.message.reply_text(answer)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle))

print("Bot started...")
app.run_polling()