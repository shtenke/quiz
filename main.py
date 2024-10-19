
import telebot
from config import token
# Задание 7 - испортируй команду defaultdict
from logic import quiz_questions
from collections import defaultdict

user_responses = {} 
# Задание 8 - создай словарь points для сохранения количества очков пользователя

bot = telebot.TeleBot(token)
points = defaultdict(int)
def send_question(chat_id):
    bot.send_message(chat_id, quiz_questions[user_responses[chat_id]].text, reply_markup=quiz_questions[user_responses[chat_id]].gen_markup())

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):

    if call.data == "correct":
        points[call.message.chat.id] += 1
        bot.answer_callback_query(call.id, f"Answer is correct, your points: {points[call.message.chat.id]}")
        # Задание 9 - добавь очки пользователю за правильный ответ
    elif call.data == "wrong":
        bot.answer_callback_query(call.id,  "Answer is wrong")
      
    # Задание 5 - реализуй счетчик вопросов
    if user_responses[call.message.chat.id] < len(quiz_questions)-1: #оно странно работает
        user_responses[call.message.chat.id] += 1 
    else:
        user_responses[call.message.chat.id] = 0
    # Задание 6 - отправь пользователю сообщение с количеством его набранных очков, если он ответил на все вопросы, а иначе отправь следующий вопрос
    send_question(call.message.chat.id)

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id not in user_responses.keys():
        user_responses[message.chat.id] = 0
        send_question(message.chat.id)


bot.infinity_polling()
