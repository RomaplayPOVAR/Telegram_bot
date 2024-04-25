import os
import requests
from time import sleep
from pyautogui import screenshot, click, moveTo
from sympy import solve, parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

BOT_TOKEN = '6649778454:AAFsLP_IXCjqEnSl9guLoErjdAkn3cjyL8g'

reply_keyboard = [['Посчитать выражение', 'Решить уравнение'],
                  ['Установить таймер', 'Сбросить таймер']]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

one_key = InlineKeyboardMarkup([[InlineKeyboardButton('TECT', callback_data='call_me')]])


async def callback(call, context):
    print(call.callback_query.message)
    if call.callback_query.data == 'exit':
        await call.callback_query.message.reply_text('Завершение...')
        exit()
    elif call.callback_query.data == 'not_exit':
        await call.callback_query.message.reply_text('Отмена.')


async def ex(update, context):
    if update.message.chat.username in [i.name for i in
                                        os.scandir('C:/Users/User/PycharmProjects/Telegram/Telega_1/users_data')]:
        file = open(f'C:/Users/User/PycharmProjects/Telegram/Telega_1/users_data/'
                    f'{update.message.chat.username}/data.txt').read().split('\n')
        if file[0] == 'Admin':
            await update.message.reply_text('Вы уверены?',
                                            reply_markup=InlineKeyboardMarkup(
                                                [[InlineKeyboardButton('Да', callback_data='exit'),
                                                  InlineKeyboardButton('Нет', callback_data='not_exit')]]))
        else:
            await update.message.reply_text('Отказано в доступе...')


def passage(file_name, folder):
    for element in os.scandir(folder):
        if element.is_file():
            try:
                if element.name == file_name:
                    yield folder
            except:
                ...
        else:
            yield from passage(file_name, element.path)


async def get_click(update, context):
    if update.message.chat.username == 'TYPUCT_C_MAPCA':
        pos = [int(i) for i in update.message.text[update.message.text.index('.') + 1:].split('.')]
        x, y = pos[0], pos[1]
        moveTo(x, y)
        click(button='left' if pos[2] else 'right')
        sleep(0.5)
        await scr_shot(update, context)


async def scr_shot(update, context):
    if update.message.chat.username == 'TYPUCT_C_MAPCA':
        screenshot('scr.png')
        await context.bot.send_photo(chat_id=update.message.chat.id, photo=open('scr.png', 'rb'))


async def echo(update, context):
    msg = update.message.text
    if msg == 'Посчитать выражение':
        await calculate(update, context)
    elif msg == 'Решить уравнение':
        await equation(update, context)
    await update.message.reply_text('404 - not found')


async def ans_file(update, context):
    print(update.message.chat.username)
    if update.message.chat.username in \
            [i.name for i in os.scandir('C:/Users/User/PycharmProjects/Telegram/Telega_1/users_data')]:
        file = open(f'C:/Users/User/PycharmProjects/Telegram/Telega_1/users_data/'
                    f'{update.message.chat.username}/data.txt').read().split('\n')
        if file[0] == 'Admin':
            await update.message.reply_text('Введите пароль:')
            return 'user_pass'
        else:
            await update.message.reply_text('Отказано в доступе')
            return ConversationHandler.END
    else:
        await update.message.reply_text('Такого пользователя нет')
        return ConversationHandler.END


async def check_password(update, context):
    file = open(f'C:/Users/User/PycharmProjects/Telegram/Telega_1/users_data/'
                f'{update.message.chat.username}/data.txt').read().split('\n')
    if file[2] == update.message.text:
        await update.message.reply_text('Какой вас интересует файл?')
        return 'send_file'
    else:
        await update.message.reply_text('Неверный пероль!')
        return ConversationHandler.END


async def send_file(update, context):
    try:
        file = open(update.message.text, 'rb')
        await context.bot.send_document(chat_id=update.message.chat.id, document=file)
    except:
        await update.message.reply_text('Не удалось открыть файл(')


async def start(update, context):
    print(update)
    await update.message.reply_text(f'BEHAPA_BOT приветствует вас, {update.message.chat.first_name}!',
                                    reply_markup=one_key)
    await context.bot.send_photo(chat_id=update.message.chat.id, photo=open('pictures/ava.jpeg', 'rb'))


async def help(update, context):
    await update.message.reply_text('Я не помошник)')


def remove_job(name, context):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.shedule_removal()
    return True


# -----------------------------------------------------------

async def ans_calc(update, context):
    await update.message.reply_text('Что надобно псочитать?')
    return 1


async def calculate(update, context):
    try:
        res = eval(update.message.text)
    except:
        res = 'Ошибка в примере)'
    await update.message.reply_text(f'{res}')
    return ConversationHandler.END


# -----------------------------------------------------------


async def ans_timer(update, context):
    await update.message.reply_text('На сколько?')
    return 1


async def modern_set(update, context):
    time = int(eval(update.message.text))
    chat_id = update.effective_message.chat_id
    job_removed = remove_job(str(chat_id), context)
    context.job_queue.run_once(task, time, chat_id=chat_id, name=str(chat_id), data=time)

    text = f'Установлен таймер на {time} секунд'
    if job_removed:
        text += 'Старая задача удалена!'
    await update.effective_message.reply_text(text)
    return ConversationHandler.END


async def task(context):
    await context.bot.send_message(context.job.chat_id, text=f'Время вышло!')


async def unset(update, context):
    chat_id = update.message.chat_id
    job_removed = remove_job(str(chat_id), context)
    text = 'Таймер отменен!' if job_removed else 'У вас нет активных таймеров'
    await update.message.reply_text(text)


async def ans_eq(update, context):
    await update.message.reply_text(f'Введите уравнение:')
    return 1


async def equation(update, context):
    try:
        transformations = (standard_transformations + (implicit_multiplication_application,))
        formula = update.message.text
        res = solve(parse_expr(formula.replace("^", "**").replace("=", "-"), transformations=transformations))
        res = '\n'.join([(str(i) if 'C' not in str(i) else 'Сложный комплексный корень...') for i in res])
        await update.message.reply_text(res)
    except:
        await update.message.reply_text('Что-то пошло не так...')
    return ConversationHandler.END


# -----------------------------------------------------------

async def update_keyboard(update, context):
    await update.message.reply_text('Обновление клавы...', reply_markup=markup)
    return


async def stop(update, context):
    await update.message.reply_text('Прерывание...')
    return ConversationHandler.END


async def money_info(update, context):
    YOUR_API_KEY = "cecd51a2ca8344ed8451ed6bff04a379"
    data = requests.get(
        'https://openexchangerates.org/api/latest.json?app_id="cecd51a2ca8344ed8451ed6bff04a379"&base=USD&symbols=RUB').json
    await update.message.reply_text(f"BEHAPA_BOT Даёт курс валют: USD {data['rates']['RUB']}")


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    conv_hadler = ConversationHandler(
        entry_points=[CommandHandler('calc', ans_calc)],
        states={1: [MessageHandler(filters.TEXT & ~filters.COMMAND, calculate)]},
        fallbacks=[]
    )

    timer = ConversationHandler(
        entry_points=[CommandHandler('set', ans_timer)],
        states={1: [MessageHandler(filters.TEXT & ~filters.COMMAND, modern_set)]},
        fallbacks=[]
    )

    eq = ConversationHandler(
        entry_points=[CommandHandler('eq', ans_eq)],
        states={1: [MessageHandler(filters.TEXT & ~filters.COMMAND, equation)]},
        fallbacks=[]
    )

    file = ConversationHandler(
        entry_points=[CommandHandler('send_file', ans_file)],
        states={'user_pass': [MessageHandler(filters.TEXT & ~filters.COMMAND, check_password)],
                'send_file': [MessageHandler(filters.TEXT & ~filters.COMMAND, send_file)]},
        fallbacks=[]
    )

    app.add_handler(conv_hadler)
    app.add_handler(timer)
    app.add_handler(eq)
    app.add_handler(file)

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help))
    app.add_handler(CommandHandler('unset', unset))
    app.add_handler(CommandHandler('money_info', money_info))
    app.add_handler(CommandHandler('key', update_keyboard))
    app.add_handler(CommandHandler('stop', stop))
    app.add_handler(CommandHandler('scr', scr_shot))
    app.add_handler(CommandHandler('1', get_click))
    app.add_handler((CallbackQueryHandler(test)))
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    app.add_handler(text_handler)
    print('Run')
    app.run_polling()


if __name__ == '__main__':
    main()
