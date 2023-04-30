import telegram_bot_calendar
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from keyboards import register_markup, stop_register_markup, end_registration_markup, stop_add_task_markup, \
    yes_or_no_markup, start_timer_markup, stop_timer_markup, main_markup
from base_requests import post_response, get_response, put_response
from utils import checking_for_success, create_url, get_id_from_string
import datetime


async def register(update, context):
    """Отправляет сообщение когда получена команда /register"""
    await update.message.reply_text("Давайте начнём регистрацию")
    await update.message.reply_text("Укажите ваше имя", reply_markup=stop_register_markup)
    return 1


async def name_response(update, context):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("А теперь укажите фамилию")
    return 2


async def surname_response(update, context):
    context.user_data["surname"] = update.message.text
    await update.message.reply_text(
        "Укажите адрес электронной почты"
    )
    return 3


async def email_response(update, context):
    context.user_data["email"] = update.message.text
    context.user_data['telegram_id'] = int(update.effective_user.id)
    url = create_url("users")
    resp = await post_response(url, context.user_data)
    answer = "Регистрация завершена"
    await update.message.reply_text(answer,
                                    reply_markup=main_markup)
    return ConversationHandler.END


async def stop_register(update, context):
    await update.message.reply_text('Регистрация остановлена')
    await update.message.reply_text('Если хотите начать снова то используйте конанду /start',
                                    reply_markup=register_markup)
    return ConversationHandler.END


register_handler = ConversationHandler(
    entry_points=[CommandHandler('register', register)],
    states={
        1: [MessageHandler(filters.TEXT & ~filters.COMMAND, name_response)],
        2: [MessageHandler(filters.TEXT & ~filters.COMMAND, surname_response)],
        3: [MessageHandler(filters.TEXT & ~filters.COMMAND, email_response)]
    },
    fallbacks=[CommandHandler('stop_register', stop_register)]
)


async def add_task(update, context):
    await update.message.reply_text("Давайте добавим задачу")
    await update.message.reply_text("Напишите название задачи", reply_markup=stop_add_task_markup)
    return 1


async def task_title_response(update, context):
    context.user_data['title'] = update.message.text
    await update.message.reply_text("Напишите содержание задачи")
    return 2


async def task_content_response(update, context):
    context.user_data['content'] = update.message.text
    user_id_url = create_url('user_telegram', update.effective_user.id)
    user_id = await get_response(user_id_url)
    context.user_data['user_id'] = user_id
    url = create_url("tasks")
    resp = await post_response(url, context.user_data)
    answer = "Задача добавлена"
    await update.message.reply_text(answer, reply_markup=main_markup)
    return ConversationHandler.END


async def stop_add_task(update, context):
    await update.message.reply_text('Добавление задачи остановлено',
                                    reply_markup=main_markup)
    return ConversationHandler.END


add_task_handler = ConversationHandler(
    entry_points=[CommandHandler("add_task", add_task)],
    states={
        1: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_title_response)],
        2: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_content_response)]
    },
    fallbacks=[CommandHandler("stop_add_task", stop_add_task)]
)


async def compete_task(update, context):
    telegram_id = update.effective_user.id
    url = create_url('user_telegram', telegram_id)
    user_id = await get_response(url)
    url_tasks = create_url('tasks_user', user_id['user_id'])
    tasks = await get_response(url_tasks)

    not_complete_tasks = tasks["not_completed_tasks"]
    titles_and_id_tasks = [[item["title"], item['id']] for item in not_complete_tasks]
    tasks_keyboards = [[f'{i[1]}: {i[0]}'] for i in titles_and_id_tasks]
    tasks_markup = ReplyKeyboardMarkup(tasks_keyboards, one_time_keyboard=True)
    await update.message.reply_text("Выберите задачу, которую хотите завершить",
                                    reply_markup=tasks_markup)
    return 1


async def task_response(update, context):
    string = update.message.text
    id = get_id_from_string(string)
    context.user_data['id'] = id
    await update.message.reply_text("Вы хотите засечь время выполнения задачи?",
                                    reply_markup=yes_or_no_markup)
    return 2


async def timer_response(update, context):
    answer = update.message.text
    if answer == 'Нет':
        await update.message.reply_text("Как скажите")
        data = {
            'is_completed': True,
            'execution_time': "не засечено"
        }
        url = create_url('task', context.user_data['id'])
        resp = await put_response(url, data)
        string = checking_for_success("Задача отмечена завершённой", resp)
        await update.message.reply_text(string, reply_markup=main_markup)
        return ConversationHandler.END
    else:
        await update.message.reply_text(
            "Хорошо. Нажмите на кнопку чтобы запустить секундомер\n"
            "Когда закончите нажмите на кнопку СТОП",
            reply_markup=start_timer_markup
        )
        return 3


async def start_timer(update, context):
    answer = update.message.text
    if answer == "СТАРТ":
        context.user_data["start_time"] = datetime.datetime.now()
        await update.message.reply_text(
            "Время пошло",
            reply_markup=stop_timer_markup
        )
    return 4


async def stop_timer(update, context):
    answer = update.message.text
    if answer == "СТОП":
        stop_time = datetime.datetime.now()
        time = stop_time - context.user_data["start_time"]
        await update.message.reply_text(
            f"На выполнение задачи потрачено {time}"
        )
        data = {
            'is_completed': True,
            'execution_time': str(time)
        }
        url = create_url('task', context.user_data['id'])
        resp = await put_response(url, data)
        string = "Задача отмечена завершённой"
        await update.message.reply_text(string, main_markup)
        return ConversationHandler.END


async def stop_complete_task(update, context):
    await update.message.reply_text('Выполнение задачи остановлено',
                                    reply_markup=ReplyKeyboardRemove)
    return ConversationHandler.END


complete_task_handler = ConversationHandler(
    entry_points=[CommandHandler("compete_task", compete_task)],
    states={
        1: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_response)],
        2: [MessageHandler(filters.TEXT & ~filters.COMMAND, timer_response)],
        3: [MessageHandler(filters.TEXT & ~filters.COMMAND, start_timer)],
        4: [MessageHandler(filters.TEXT & ~filters.COMMAND, stop_timer)]
    },
    fallbacks=[CommandHandler("stop_complete_task", stop_complete_task)]
)
