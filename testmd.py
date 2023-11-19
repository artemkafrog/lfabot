import telebot
import os
import sqlite3
from telebot import types

# Инициализация бота с помощью токена
bot = telebot.TeleBot('6555884873:AAGVjCoQPLZtRNpTo9-rZKS9cIq8B8so2iI')

# Функция для обработки команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "Привет! Я бот для мероприятий. Используй /help, чтобы увидеть больше информации.")

@bot.message_handler(commands=['help'])
def send_help(message):
    response = """
Список доступных команд:
/create_db - Создать мероприятие
/delete_db - Удалить мероприятие
/add_student - Добавить ученика в мероприятие
/show_db - Просмотреть участников мероприятия
/show_all_db - Активные мероприятия
/info - Информация о проекте
    
Для корректной работы бота вводите название мероприятий так, как изначально задумывал организатор мероприятия.
    """
    bot.reply_to(message, response)

@bot.message_handler(commands=['info'])
def bot_information(message):
    bot.reply_to(message, "Здесь находится вся информация о данном проекте")

@bot.message_handler(commands=['create_db'])
def handle_create_db(message):
    bot.reply_to(message, "Введите название новой базы данных:")
    bot.register_next_step_handler(message, create_db)

def create_db(message):
    db_name = message.text + '.db'
    if not os.path.exists(db_name):
        conn = sqlite3.connect(db_name)
        bot.reply_to(message, f"База данных {db_name} успешно создана.")
    else:
        bot.reply_to(message, f"База данных {db_name} уже существует.")

# Функция для добавления ученика в базу данных
@bot.message_handler(commands=['add_student'])
def handle_add_student(message):
    bot.reply_to(message, "Введите название базы данных, в которую нужно добавить ученика:")
    bot.register_next_step_handler(message, add_student)

def add_student(message):
    db_name = message.text + '.db'
    if os.path.exists(db_name):
        bot.reply_to(message, "Введите имя ученика:")
        bot.register_next_step_handler(message, lambda msg: save_student(db_name, msg))
    else:
        bot.reply_to(message, f"Базы данных {db_name} не существует.")

def save_student(db_name, message):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS students (name TEXT)")
    cursor.execute("INSERT INTO students (name) VALUES (?)", (message.text,))
    conn.commit()
    bot.reply_to(message, "Ученик успешно добавлен.")


# Функция для отображения содержимого базы данных
@bot.message_handler(commands=['show_db'])
def handle_show_db(message):
    bot.reply_to(message, "Введите название базы данных, чтобы отобразить учеников:")
    bot.register_next_step_handler(message, show_db)

def show_db(message):
    db_name = message.text + '.db'
    if os.path.exists(db_name):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM students")
        students = cursor.fetchall()
        students_list = [f'{i + 1}. {student[0]}' for i, student in enumerate(students)]
        students_string = '\n'.join(students_list)
        bot.reply_to(message, f"Ученики в базе данных {db_name}:\n{students_string}")
    else:
        bot.reply_to(message, f"Базы данных {db_name} не существует.")

@bot.message_handler(commands=['delete_db'])
def handle_delete_db(message):
    bot.reply_to(message, "Введите название базы данных, чтобы удалить:")
    bot.register_next_step_handler(message, delete_db)

def delete_db(message):
    db_name = message.text + '.db'
    if os.path.exists(db_name):
        os.remove(db_name)
        bot.reply_to(message, f"База данных {db_name} успешно удалена.")
    else:
        bot.reply_to(message, f"Базы данных {db_name} не существует.")

@bot.message_handler(commands=['show_all_db'])
def handle_show_all_db(message):
    db_files = [f for f in os.listdir('.') if f.endswith('.db')]
    if len(db_files) > 0:
        db_list = '\n'.join(db_files)
        bot.reply_to(message, f"Список всех активных мероприятий:\n{db_list}")
    else:
        bot.reply_to(message, "Список баз данных пуст.")

# Запуск бота
bot.polling(none_stop=True)
