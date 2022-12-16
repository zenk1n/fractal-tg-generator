import time
from mandelbrot import Mandelbrot
from auth_data import token
import telebot
import os
import os.path
from julia import Julia
import sys
from telebot import types

def create_julia():
    ju = Julia([500, 500])
    ju.setC(-0.835 - 0.232j)
    ju.doJulia(200)
    ju.wait()

def create_mandelbrot():
    man = Mandelbrot([500, 500])
    man.setRange(5, 5)
    man.doMandelbrot(200)
    man.wait()

def telegram_bot(token):
    bot = telebot.TeleBot(token)
    stic = open('stic/welcome.webp', 'rb')  # чтение файла в двоичном формате

    @bot.message_handler(commands=['start'])
    def start(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("💫 по Мандельброту")
        btn2 = types.KeyboardButton("💥 по Жулю")
        markup.add(btn1, btn2)
        bot.send_sticker(message.chat.id, stic)
        time.sleep(1.5)
        bot.send_message(message.chat.id, text="Привет, {0.first_name}!".format(message.from_user), reply_markup=markup)
        time.sleep(0.5)
        bot.send_message(message.chat.id, 'Тебя приветствует бот "math is better than design".')
        time.sleep(0.3)
        bot.send_message(message.chat.id, 'Я являюсь проектом по учебной практике студентов РГРТУ им. В.Ф.Уткина гр. 140.')
        time.sleep(0.3)
        bot.send_message(message.chat.id,'Зенкин М.Д. @zeenkin')
        time.sleep(0.3)
        bot.send_message(message.chat.id,'Королёв К.В. @@Kirkange')
        time.sleep(0.3)
        bot.send_message(message.chat.id, 'Данный бот генерирует узоры из фракталов Мандельброта и Жуля.')
        bot.send_message(message.chat.id, 'Просто нажми нужную кнопочку и всё! :) Приятного использования!')

    @bot.message_handler(content_types=["text"])
    def send_text(message):
        if message.text == "💫 по Мандельброту":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn3 = types.KeyboardButton("Подождите... Идёт генерация...")
            btn4 = types.KeyboardButton("Получить")
            markup.add(btn3)
            bot.send_message(message.chat.id, 'Пожалуйста, подождите.', reply_markup=markup)
            create_mandelbrot()
            markup1.add(btn4)
            bot.send_message(message.chat.id, 'Изображения успешно сгенерированы!', reply_markup=markup1)

        elif message.text == "💥 по Жулю":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn3 = types.KeyboardButton("Подождите... Идёт генерация...")
            btn4 = types.KeyboardButton("Получить")
            markup.add(btn3)
            bot.send_message(message.chat.id, 'Пожалуйста, подождите.', reply_markup=markup)
            create_julia()
            markup1.add(btn4)
            bot.send_message(message.chat.id, 'Изображения успешно сгенерированы!', reply_markup=markup1)

        elif message.text == "Получить":
            if os.path.exists("5.png"):
                try:
                    for i in range(1, 6, 1):
                        bot.send_photo(message.chat.id, photo=open(f'{i}.png', 'rb'))
                        os.remove(f'{i}.png')
                    markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    btn = types.KeyboardButton("Завершить")
                    markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    markup2.add(btn)
                    bot.send_message(message.chat.id, '5 изображений успешно отправлены.', reply_markup=markup2)
                except Exception as ex:
                    print(ex)
                    bot.send_message(message.chat.id, "Упс! Произошла ошибка. :(")

        elif message.text == "Завершить":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("💫 по Мандельброту")
            btn2 = types.KeyboardButton("💥 по Жулю")
            markup.add(btn1, btn2)
            bot.send_message(message.chat.id, 'Выберите режим генерации фракталов', reply_markup=markup)

        else:
            bot.send_message(message.chat.id, text="К сожалению, такой команды нет :(")
    bot.polling()

if __name__ == '__main__':
    flag = True
    while flag:
        telegram_bot(token)
