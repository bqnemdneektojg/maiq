import telebot
import smtplib
from telebot import *
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import hashlib
import re
import requests
markupprofile = types.InlineKeyboardMarkup()
markupprofile.add(types.InlineKeyboardButton(text='Купить подписку', url='https://t.me/OLEG_DZHIHADOV'))
markupprofile.add(types.InlineKeyboardButton(text='Информация', url='https://telegra.ph/DZHIHAD-MAILER-07-28'))
WHITELIST = ['b0a9309ed39669014f51b940e3ddedf48419469aec5e0a62d61b3212f8a93656', 'c70a0d582ae76d310b21ee0b55e8c339d36f5add1d3f879f491d39826b1efc73', '7dcb7fd256bd2da8bb87afea6ccaed6d1284bba19b210d83a60912dc7d714377', '75a8a4bb0cfa29c896db7ce39d5d7ebe2e045561da2f8463dcce5a4e1186de51', 'c5744460e2256b58df17a214047c1727607a7479c7250d29357977d6d5403c6d', '7b47cfadd0476ae0f89eb18bed64479498f6081ba1df4165bf4338fceb2c530e', '83875b264c684999b5dd26b96f55ded364cc50532d9a7b09e98f4565d382128c', 'c3c5a72814cd35794d1b398592261a08034fe759bf13df76f1fad1c8792f2fe6', '288f054d6ceba778045f1d6e450dcd86ceee4d22e207cdf23d8f5a867e320d83', 'afc6f16803892f4338dea529bbf46b682a0e8bf4db8cf768e1900241efb26b78', '9be26c29828019e585091e1dfca381c090cadc2ba3e2b66c44cd0f485634c208', 'd9052612f0234d1081d7d74f3da8a44d794837cceddc28c23b6acb99cbc25051']
admin = "b0a9309ed39669014f51b940e3ddedf48419469aec5e0a62d61b3212f8a93656"
API_TOKEN = '6548237032:AAH1V1RUsVgc8zpXIuJT_nm13H-n_X20jDQ'
CONFIG_FILE = 'config.txt'
markup = types.InlineKeyboardMarkup(row_width=2)
btn1 = types.InlineKeyboardButton('Отправить письмо', callback_data='send')
btn2 = types.InlineKeyboardButton('Проверить почту', callback_data='mailcheck')
btn3 = types.InlineKeyboardButton('Статистика', callback_data='stats')
btn4 = types.InlineKeyboardButton('Профиль', callback_data='profile')
markup.add(btn1)
markup.add(btn2)
markup.add(btn3)
markup.add(btn4)


bot = telebot.TeleBot(API_TOKEN)

def validate_email(email):
    pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
    if re.match(pattern, email):
        return True
    else:
        return False


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    encrypted_id = hashlib.sha256(str(user_id).encode()).hexdigest()
    with open('users.txt', 'r') as file:
        if encrypted_id in file.read():
                print(".")
        else:
            with open('users.txt', 'a') as file:
                file.write(encrypted_id + '\n')
                print(".")
    bot.reply_to(message, "Привет! Я официальный бот сервиса DzhihadMailer!\nВоспользуйся кнопками ниже для использования бота.\n\n@DzhihadMailer", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def start_email_dialog(call):
    user_id = call.from_user.id
    encrypted_id = hashlib.sha256(str(user_id).encode()).hexdigest()
    if encrypted_id in WHITELIST:
        if call.data == "send":
            msg = call.id
            bot.send_message(call.from_user.id, "Введите адрес отправителя:")
            bot.register_next_step_handler(msg, get_sender_email)
    else:
        bot.reply_to(message, "Заблокировано.\nУ вас нет подписки! Приобрести можно тут:\n@Oleg_Dzhihadov")

    if call.data == "profile":
        user_id = call.from_user.id
        encrypted_id = hashlib.sha256(str(user_id).encode()).hexdigest()

        value = encrypted_id
        if value in WHITELIST:
                status = 'Присутствует'
        else:
                status = 'Отсутствует'
        bot.send_message(user_id, f'Ваш ID: {encrypted_id}\nСтатус подписки: {status}', reply_markup=markupprofile)

    elif call.data == "stats":
        valuepodpis = len(WHITELIST)
        with open('users.txt', 'r') as file:
                users_count = sum(1 for line in file)
                bot.send_message(call.message.chat.id, f'Количество пользователей: {users_count}\nКоличество пользователей с подпиской: {valuepodpis}')
    elif call.data == "mailcheck":
        msg = call.message
        bot.send_message(call.from_user.id, "Введите email'ы для проверки (можно ввести несколько адресов через запятую):")
        bot.register_next_step_handler(msg, validate_emails)


def validate_emails(message):
    emails = message.text.split(",")
    valid_emails = []
    invalid_emails = []

    for email in emails:
        if validate_email(email.strip()):
            valid_emails.append(email.strip())
        else:
            invalid_emails.append(email.strip())

    valid_count = len(valid_emails)
    invalid_count = len(invalid_emails)

    valid_emails_str = ", ".join(valid_emails)
    invalid_emails_str = ", ".join(invalid_emails)
    bot.send_message(message.chat.id, f"✅ Валидные email'ы ({valid_count}): {valid_emails_str}\n⛔ Невалидные email'ы ({invalid_count}): {invalid_emails_str}")

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "send":
        msg = bot.send_message(call.from_user.id, "Введите адрес отправителя:")
        bot.register_next_step_handler(msg, get_sender_email)


def get_sender_email(call):
    sender_email = call.message
    msg = bot.send_message(message.chat.id, "Введите адрес получателя (можно ввести несколько адресов через запятую):")
    bot.register_next_step_handler(msg, get_recipient_email, sender_email)

def get_recipient_email(call, sender_email):
    recipient_emails = call.message.text.split(",")
    msg = bot.reply_to(message, "Введите тему письма:")
    bot.register_next_step_handler(msg, get_email_subject, sender_email, recipient_emails)

def get_email_subject(call, sender_email, recipient_emails):
    email_subject = call.message
    msg = bot.reply_to(message, "Введите текст письма:")
    bot.register_next_step_handler(msg, send_email, sender_email, recipient_emails, email_subject)

def send_email(call, sender_email, recipient_emails, email_subject):
    email_text = message.text
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(recipient_emails)
    msg['Subject'] = email_subject
    msg.attach(MIMEText(email_text, 'plain'))

    try:
        with open(CONFIG_FILE, 'r') as file:
            config = file.read().splitlines()
            smtp_server = config[0]
            smtp_port = int(config[1])
            sender_email = config[2]
            sender_password = config[3]
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)

            sent_count = 0
            not_sent_count = 0
            error_message = ""

            start_time = datetime.datetime.now()

            for recipient_email in recipient_emails:
                try:
                    server.sendmail(sender_email, recipient_email, msg.as_string())
                    sent_count += 1
                except Exception as e:
                    not_sent_count += 1
                    error_message += f"⛔ Ошибка при отправке письма на адрес {recipient_email}: {str(e)}\n"

            end_time = datetime.datetime.now()
            total_time = end_time - start_time

            server.quit()

            if sent_count > 0:
                success_message = f"✅ Успешно отправлено писем: {sent_count}\n"
            else:
                success_message = ""

            if not_sent_count > 0:
                failure_message = f"⛔ Не удалось отправить писем: {not_sent_count}\n"
            else:
                failure_message = ""

            time_message = f"🕘 Время выполнения: {total_time}\n@DzhihadMailer"

            bot.reply_to(message, success_message + failure_message + error_message + time_message)
    except Exception as e:
        bot.reply_to(message, "Произошло что-то страшное...\n1. Исчерпан суточный лимит в 200 сообщений\n2. Почта не валидная")
bot.polling()
