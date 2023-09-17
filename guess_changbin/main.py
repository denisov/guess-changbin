import logging
import os
import random
from dataclasses import dataclass
from typing import cast

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from guess_changbin.questions_with_answers import questions_with_answers


@dataclass
class UserAnswer:
    question: str
    answer: str


async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    question = random.choice(list(questions_with_answers.keys()))

    answer_buttons = []

    uniq_answers = list(set(questions_with_answers.values()))
    answers = list(random.sample(uniq_answers, len(uniq_answers)))
    for answer in answers:
        answer_buttons.append(
            InlineKeyboardButton(
                text=answer, callback_data=UserAnswer(question=question, answer=answer)
            )
        )

    if update.callback_query:
        await update.callback_query.answer()

    message = update.message or update.callback_query.message
    await update.get_bot().send_photo(
        chat_id=message.chat_id,
        photo=question,
        reply_markup=InlineKeyboardMarkup([answer_buttons]),
    )


async def submit_variant(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_answer = cast(UserAnswer, query.data)

    await update.callback_query.answer()
    if user_answer.answer == questions_with_answers[user_answer.question]:
        await update.callback_query.message.reply_text(
            "Правильно.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Новый вопрос", callback_data="ask_question")]]
            ),
        )
    else:
        await update.callback_query.message.reply_text("Неправильно, попробуй еще")


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def run():
    application = (
        ApplicationBuilder()
        .token(os.getenv("TELEGRAM_BOT_TOKEN"))
        .arbitrary_callback_data(True)
        .build()
    )

    application.add_handler(CommandHandler("start", ask_question))
    application.add_handler(CallbackQueryHandler(ask_question, pattern="ask_question"))
    application.add_handler(CallbackQueryHandler(submit_variant, pattern=UserAnswer))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, ask_question)
    )

    application.run_polling()


if __name__ == "__main__":
    run()
