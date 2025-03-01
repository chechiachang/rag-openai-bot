import os

from dotenv import find_dotenv
from dotenv import load_dotenv
from loguru import logger
from telegram import Update
from telegram.ext import Application
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes
from telegram.ext import filters

from .conversational_retrieval_agent import ConversationalRetrievalAgent
from .utils import get_message_text


def get_chat_filter() -> filters.BaseFilter:
    whitelist = os.getenv("BOT_WHITELIST")
    if not whitelist:
        logger.warning("No whitelist specified, allowing all chats")
        return filters.ALL
    else:
        chat_ids = [int(chat_id) for chat_id in whitelist.replace(" ", "").split(",")]
        return filters.Chat(chat_ids)

def get_bot_token() -> str:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN is not set")
    return token

def run_bot() -> None:
    load_dotenv(find_dotenv(raise_error_if_not_found=True, usecwd=True))
    chat_filter = get_chat_filter()

    app = Application.builder().token(get_bot_token()).build()
    app.add_handlers(
        [
            CommandHandler("k8s", k8s_qa, filters=chat_filter),
        ]
    )

    app.run_polling(allowed_updates=Update.ALL_TYPES)

async def k8s_qa(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bot = ConversationalRetrievalAgent('demo_collection')
    bot.setup_bot()

    text = get_message_text(update)
    if not text:
        return
    logger.info(f"Received message: {text}")

    question = text.replace("/k8s", "").strip()
    answer = bot.ask_question(question)

    await update.message.reply_text(answer)
