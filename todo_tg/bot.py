import logging
from telegram.ext import Updater, CommandHandler
from django.contrib.auth import authenticate, login
from todo_web.models import Task

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                       level=logging.INFO)

def start_command(update, context):
       context.bot.send_message(chat_id=update.effective_chat.id, text='Введите ваш логин и пароль в формате: /login ЛОГИН ПАРОЛЬ')

def login_command(update, context):
    args = context.args
    if len(args) == 2:
        username = args[0]
        password = args[1]
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
           login(update.message.from_user, user)
           tasks = Task.objects.filter(user=user)
           task_list = '\n'.join([task.title for task in tasks])
           context.bot.send_message(chat_id=update.effective_chat.id, text=f'Ваши задачи:\n{task_list}')
        else:
           context.bot.send_message(chat_id=update.effective_chat.id, text='Некорректный логин или пароль')
    else:
           context.bot.send_message(chat_id=update.effective_chat.id, text='Неверный формат команды /login')

updater = Updater(token='6077583494:AAGuu9WeJXeomPOsJFSaC6zu2mj_gLhypew', use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start_command))
dispatcher.add_handler(CommandHandler("login", login_command))
updater.start_polling()