# -*- coding: utf-8 -*-
import os
import telebot
import time
import random
import threading
from emoji import emojize
from telebot import types
from pymongo import MongoClient
import traceback

token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)


client=MongoClient(os.environ['database'])
db=client.
users=db.users

starttext='/eat - съесть случайный продукт из своих запасов\n/animal - выбрать себе вид\n/animalinfo - инфо о видах'


@bot.message_handler(commands=['start'])
def start(m):
    user=users.find_one({'id':m.from_user.id})
    if user==None:
        users.insert_one(createuser(m.from_user))
        user=users.find_one({'id':m.from_user.id})
        bot.send_message(user['id'], 'Ну тут ты короче будешь добывать еду и есть её. И да, выбери, кто ты, командой /animal.')
    else:
        bot.send_message(user['id'], starttext)
        
@bot.message_handler()
def alltext(m):
    user=users.find_one({'id':m.from_user.id})
    if user!=None:
        if m.text[:4]=='/eat':
        
        
                         

print('7777')
bot.polling(none_stop=True,timeout=600)

