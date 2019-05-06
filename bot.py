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
db=client.foodeater
users=db.users

allanimals=[
    'cat':{'name':'Кот',
          'data':'cat',
           'size':3},
    'squirrel':{'name':'Белка',
          'data':'squirrel',
           'size':2},
    'wolf':{'name':'Волк',
          'data':'wolf',
           'size':6},
    'frog':{'name':'Лягушка',
          'data':'frog',
           'size':1},
    'elephant':{'name':'Слон',
          'data':'elephant',
           'size':7},
    'shakal':{'name':'Шакал',
          'data':'shakal',
           'size':5},
    'dog':{'name':'Собака',
          'data':'dog',
           'size':4}
]

loctypes=[
    'fastfood':{'name':'Жирная еда',
            'data':'fastfood'},
    'vegan':{'name':'Зелень',
            'data':'vegan'},
    'meat':{'name':'Мясо',
            'data':'meat'},
    'sweet':{'name':'Сладости',
            'data':'sweet'}
]


starttext='/me - информация обо мне\n/eat - съесть случайный продукт из своих запасов\n/animal - выбрать себе вид\n/animalinfo - инфо о видах'


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
            if len(user['food'])>0:
                food=random.choice(user['food'])
                users.update_one({'id':user['id']},{'$pull':{'food':food['code']}})
                users.update_one({'id':user['id']},{'$inc':{'hunger':food['value']}})
                bot.send_message(m.chat.id, 'Вы съели *'+food['name']+'*!', parse_mode='markdown')
            else:
                bot.send_message(m.chat.id, 'У вас вообще нет еды.')
        
        if m.text[:7]=='/animal':
            kb=types.InlineKeyboardMarkup()
            for ids in allanimals:
                kb.add(types.InlineKeyboardButton(text=ids['name'], callback_data='animal'+ids['data']))
            bot.send_message(m.chat.id, 'Выберите себе вид.', reply_markup=kb)
            
        if m.text[:11]=='/animalinfo':
            text=''
            text+='Чем больше размер, тем меньше вероятность, что другие украдут у вас еду, но вы добываете её медленнее. Чем меньше размер, тем такая вероятность больше, но добыча идет быстрее.\n\n'
            for ids in allanimals:
                text+='*'+ids['name']+'*:\nРазмер: '+str(ids['size'])+'\n\n'
            bot.send_message(m.chat.id, text)
            
        if m.text[:5]=='/find':
            kb=types.InlineKeyboardMarkup()
            for ids in loctypes:
                kb.add(types.InlineKeyboardButton(text=ids['name'], callback_data='find'+ids['data']))
            bot.send_message(m.chat.id, 'Выберите тип добываемой еды.', reply_markup=kb)
            
            
            
@bot.callback_query_handler(func=lambda call:True)
def calls(call):
    user=users.find_one({'id':call.from_user.id})
    if user!=None:
        
        if call.data[:4]=='find':
            loc=call.data[4:]
            if user['status']!='finding':
                users.update_one({'id':user['id']},{'$set':{'searchtype':loc}})
                users.update_one({'id':user['id']},{'$set':{'status':'finding'}})
                
    
            
        
        
    
def createuser(user):
    return {
        'id':user.id,
        'name':user.first_name,
        'food':[],
        'hungermax':100,
        'hunger':100,
        'animal':None,
        'searchtype':'all',
        'status':'free'
    }
    

print('7777')
bot.polling(none_stop=True,timeout=600)

