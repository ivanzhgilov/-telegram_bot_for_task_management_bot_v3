from telegram import ReplyKeyboardMarkup

register_keyboard = [['/register']]
register_markup = ReplyKeyboardMarkup(register_keyboard)
stop_register_keyboard = [['/stop_register']]
stop_register_markup = ReplyKeyboardMarkup(stop_register_keyboard, one_time_keyboard=False)
end_registration_keyboard = [['/register', "/end_registration"]]
end_registration_markup = ReplyKeyboardMarkup(end_registration_keyboard)
stop_add_task_keyboard = [['/stop_add_task']]
stop_add_task_markup = ReplyKeyboardMarkup(stop_add_task_keyboard)
main_keyboard = [['/get_statistics'], ['/add_task'], ['/compete_task']]
main_markup = ReplyKeyboardMarkup(main_keyboard, one_time_keyboard=True)
yes_or_no_keyboard = [['Да', "Нет"]]
yes_or_no_markup = ReplyKeyboardMarkup(yes_or_no_keyboard, one_time_keyboard=True)
start_timer_keyboard = [["СТАРТ"]]
start_timer_markup = ReplyKeyboardMarkup(start_timer_keyboard, one_time_keyboard=True)
stop_timer_keyboard = [["СТОП"]]
stop_timer_markup = ReplyKeyboardMarkup(stop_timer_keyboard, one_time_keyboard=True)
