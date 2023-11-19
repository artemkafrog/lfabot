import telebot
import sqlite3
from telebot import types

bot = telebot.TeleBot('6555884873:AAGVjCoQPLZtRNpTo9-rZKS9cIq8B8so2iI')
name = None


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,"Привет! Я бот для управления базами данных учеников. Используй /help, чтобы увидеть список команд.")


@bot.message_handler(commands=['help'])
def send_help(message):
    response = """Список доступных команд:
    /create_db - Создать новую базу данных
    /delete_db - Удалить базу данных
    /add_student - Добавить ученика в базу данных
    /show_db - Просмотреть базу данных
    """
    bot.reply_to(message, response)


@bot.message_handler(commands=['create_db'])
#def create_db(message):
   # bot.reply_to(message, "Введите ")
    #bot.register_next_step_handler(message, process_db_name_step)

def process_db_name_step(message):
    db_name = message.text
    conn = sqlite3.connect('lfa.sql')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS db_name (id int auto_increment primary key, name varchar(50))')
    conn.commit()
    cur.close()
    conn.close()
    bot.reply_to(message, f"Мероприятие уже создано.")
    bot.send_message(message.chat.id, "Введите имя ученика")
    bot.register_next_step_handler(message, create_user_name)

def create_user_name(message):
    global name
    name = message.text.strip()
    conn = sqlite3.connect('lfa.sql')
    cur = conn.cursor()
    cur.execute('INSERT INTO db_name (name) VALUES ("%s")' % (name))
    conn.commit()
    cur.close()
    conn.close()

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Список пользователей', callback_data='users')
    #btn2 = types.InlineKeyboardButton('Добавить ученика', callback_data='add_student')
    markup.row(btn1)
    bot.send_message(message.chat.id, "Ученик добавлен", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_message(callback):
    if callback.data == 'users':
        conn = sqlite3.connect('lfa.sql')
        cur = conn.cursor()

        cur.execute('SELECT * FROM db_name')
        users = cur.fetchall()

        info = ''
        for el in users:
            info += f'Имя: {el[1]}\n'

        cur.close()
        conn.close()

        bot.send_message(callback.message.chat.id, info)


@bot.message_handler(commands=['add_student'])
def process_add_student_db(message):
    bot.register_next_step_handler(message, process_db_name_step)

@bot.message_handler(commands=['delete_db'])
def delete_db(message):
    bot.register_next_step_handler(message, process_db_delete)

def process_db_delete(message):
    db_name = message.text
    conn = sqlite3.connect('lfa.sql')
    cur = conn.cursor()
    cur.execute('DROP TABLE db_name')
    conn.commit()
    cur.close()
    conn.close()
    bot.reply_to(message, f"Мероприятие '{db_name}' успешно удалено.")


bot.polling(none_stop=True)