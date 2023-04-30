import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from config import BOT_TOKEN
from base_requests import get_response
from keyboards import register_markup, main_markup
from utils import create_url

from handlers import register_handler, add_task_handler, complete_task_handler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    telegram_id = user.id
    url = create_url("user_telegram", telegram_id)
    response = await get_response(url)
    user_id = response["user_id"]
    if user_id == "not fount":
        await update.message.reply_html(f"Похоже вы, {user.mention_html()}, новый пользователь")
        await update.message.reply_text("Для начала работы пройдите небольшую регистрацию",
                                        reply_markup=register_markup)
    else:
        await update.message.reply_text(
            "Давайте, начнём работу",
            reply_markup=main_markup
        )


async def help_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("Я ваш помошник в управлении задачами")


async def get_statistics(update, context):
    telegram_id = update.effective_user.id
    url = create_url("user_telegram", telegram_id)
    response = await get_response(url)
    user_id = response["user_id"]
    url_tasks = create_url("tasks_user", user_id)
    tasks = await get_response(url_tasks)
    all_tasks = tasks["tasks"]
    completed_tasks = tasks["completed_tasks"]
    not_completed_tasks = tasks["not_completed_tasks"]
    count_all_tasks = len(all_tasks)
    count_completed_tasks = len(completed_tasks)
    count_not_completed_tasks = len(not_completed_tasks)
    if count_all_tasks == 0:
        string = "Вы ещё не добавляли задачи, давайте это исправим"
    else:
        percent = count_completed_tasks / count_all_tasks
        string = f"Процент выполненных задач: {percent * 100}"
    await update.message.reply_text(
        f"Всего Вы добавили {count_all_tasks} задач\n"
        f"Из них Вы выполнили {count_completed_tasks} задач\n"
        f"Осталось выполнить {count_not_completed_tasks} задач\n"
        + string,
        reply_markup=main_markup
    )


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler('get_statistics', get_statistics))

    application.add_handler(register_handler)
    application.add_handler(add_task_handler)
    application.add_handler(complete_task_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
