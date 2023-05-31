import pandas as pd
import numpy as np
import datetime
import os
import pathlib
import sqlite3 as sq

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from SQL import db_start, user_id_from_db, user_id_search_from_db, DB_replace_from_db, parametr_search_from_db, all_table_from_db, list_table_from_db, help_from_db, table_help_insert_from_db
from quickstart import create_writer_google_sheets, read_table_google_sheets, update_table_google_sheets, create_table_google_sheets

botMes = Bot(open(os.path.abspath('token.txt')).read())
bot = Dispatcher(botMes)

table_SH_name = 'testT'
sheet_name = 'DB'
table_name_db = 'CBAppointment'
table_link = "Links"


async def on_startup(_):
    await db_start()
#
# @bot.callback_query_handler()
# async def callback_query(callback: types.CallbackQuery, table_SH_name, sheet_name) :
# #     Перехватываем ID нажатой кнопки
#     call = callback
#     req = call.data.split('_')
#     if req[0] == 'start':
#
#
#         await DB_replace_from_db(table_SH_name, sheet_name)
#         await botMes.edit_message_text("ok", chat_id=call.message.chat.id,
#                            message_id=call.message.message_id)
#
#
#     if req[0] == 'start':  # Если метка start
#         ChoosingTopicsResult = ChoosingTopics(tree)  # Вызываем функцию
#         markup = InlineKeyboardMarkup()  # Определяем кнопку
#         for i in range(0, len(ChoosingTopicsResult), 2):  # Бежим по списку, вовзвращенному функцией
#             markup.add(InlineKeyboardButton(text=ChoosingTopicsResult[i],
#                                 callback_data=str(int(i / 2))))  # Создаем соответствующие кнопки
#         await botMes.edit_message_text(emoji.emojize(f"Выберите раздел: :magnifying_glass_tilted_left: "),
#                            reply_markup=markup,
#                            chat_id=call.message.chat.id,
#                            message_id=call.message.message_id)  # Выводим сопутствующее сообщение
#         page = 0
#         count = 0
#         # Сохраняем переменные в БД
#         ChoosingTopicsResult = ','.join(ChoosingTopicsResult)  # Функция преобразования массива в строку
#         await edit_profile('ChoosingTopicsResult', ChoosingTopicsResult, call.message.chat.id)
#         await edit_profile('page', page, call.message.chat.id)
#         await edit_profile('count', count, call.message.chat.id)




@bot.message_handler(commands=['start'])  # Начинаем работу
async def start(message: types.message):
    # global count
    # global page
    request_contact_button = KeyboardButton(text="Отправить контакты", request_contact=True)
    reply_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    reply_markup.add(request_contact_button)
    await message.reply("Добрый день! Для начала работы с ботом необходимо зарегистрироваться по номеру телефона.",
                        reply_markup=reply_markup)  # Выводим сопутствующее сообщение

@bot.message_handler(content_types='text')
async def handle_message(message: types.Message):
    link_table_read = pd.DataFrame(await list_table_from_db(table_link))
    def link_hide(link_table_read):
        txt=""
        for i in range(0, len(link_table_read)):
            txt += f'<a href="{link_table_read[1][i]}">{link_table_read[0][i]} </a> \n'
        return txt


    if message.text == 'Информация о прибытии':
        await botMes.send_message(text=f'{await parametr_search_from_db("user_name", table_name_db, message.chat.id)}, Вы прибываете в город Новосибирск, {await parametr_search_from_db("place_arrival", table_name_db, message.chat.id)} {await parametr_search_from_db("date_arrival", table_name_db, message.chat.id)} {await parametr_search_from_db("time_arrival", table_name_db, message.chat.id)}. \n'+
                             f'Вас будет встречать {await parametr_search_from_db("name_meeting", table_name_db, message.chat.id)}: {await parametr_search_from_db("phone_meeting", table_name_db, message.chat.id)} \n'+
                             f'Ваш номер рейса {await parametr_search_from_db("arrival_flight_number", table_name_db, message.chat.id)}', chat_id=message.chat.id)

    elif message.text == 'Информация о гостинице':
        await botMes.send_message(text=f'{await parametr_search_from_db("user_name", table_name_db, message.chat.id)}, Вы проживаете в гостинице {await parametr_search_from_db("hotel_name", table_name_db, message.chat.id)}, {await parametr_search_from_db("hotel_address", table_name_db, message.chat.id)}, {await parametr_search_from_db("hotel_website", table_name_db, message.chat.id)}', chat_id=message.chat.id)

    elif message.text == 'Информация об отъезде':
        await botMes.send_message(text=f'{await parametr_search_from_db("user_name", table_name_db, message.chat.id)}, Ваш отъезд из гостиницы состоится {await parametr_search_from_db("date_departure", table_name_db, message.chat.id)} {await parametr_search_from_db("time_departure", table_name_db, message.chat.id)}. Вас будет ожидать {await parametr_search_from_db("car_brand", table_name_db, message.chat.id)} {await parametr_search_from_db("number_seats", table_name_db, message.chat.id)} {await parametr_search_from_db("car_registration_number", table_name_db, message.chat.id)} \n '+
                                       f'{await parametr_search_from_db("driver_name", table_name_db, message.chat.id)} {await parametr_search_from_db("driver_phone", table_name_db, message.chat.id)}. Ваш рейс {await parametr_search_from_db("departure_flight_number", table_name_db, message.chat.id)} состоится {await parametr_search_from_db("date_departure", table_name_db, message.chat.id)} {await parametr_search_from_db("time_departure", table_name_db, message.chat.id)}', chat_id=message.chat.id)

    elif message.text == 'Досуг':
        await botMes.send_message(text=f'{await parametr_search_from_db("user_name", table_name_db, message.chat.id)}, для того, чтобы Ваше пребывание в Новосибирске было более интересным, мы подготовили для Вас несколько ссылок. \n'+
                        f'{link_hide(link_table_read)}', chat_id=message.chat.id, parse_mode=types.ParseMode.HTML)

    elif message.text == 'Помощь':
        await help_from_db(table_name_db=table_name_db, help_request='1', user_id=message.chat.id)
        await botMes.send_message(text='Что вас интересует? \n'+
                                  'Напишите ваш вопрос, и бот перешлет его администратору.', chat_id=message.chat.id)

    elif await parametr_search_from_db('help_request', table_name_db, message.chat.id) == '1':
        await help_from_db(table_name_db, '0', message.chat.id)
        hID = await table_help_insert_from_db(message.chat.id, message.text)
        await botMes.send_message(text='Ваше сообщение отправлено! Администратор скоро с вами свяжется!', chat_id=message.chat.id)
        await botMes.send_message(text='Добрый день! Вам пришел запрос на помощь: \n'+
                                  f'№ запроса: {hID} \n'+
                                  f'От: {await parametr_search_from_db("user_name", table_name_db, message.chat.id)} \n'+
                                  f'Телефон: {await parametr_search_from_db("user_phone", table_name_db, message.chat.id)} \n'+
                                  f'Текст вопроса: {message.text} \n', chat_id='920154651')

    elif message.text == 'Обновить базу':
        db_table = await all_table_from_db(table_name_db)
        # print(db_table)
        sh_table = await read_table_google_sheets(table_SH_name, sheet_name)
        # print(sh_table)
        out_table = sh_table.copy()
        out_table['user_ID'] = ""
        # out_table['user_ID'] = out_table['user_ID'].fillna("0")

        for i in range(0, len(sh_table)):
            try:
                # print((db_table[sh_table['user_phone'] == db_table['user_phone'][i]]['user_ID']))
                out_table['user_ID'][i] = (db_table[sh_table['user_phone'] == db_table['user_phone'][i]]['user_ID'].values)[0]
            except:
                out_table['user_ID'][i] = np.nan
        # print(out_table['user_ID'][:])


        out_table.to_sql('CBAppointment', sq.connect('appointment.db'), if_exists='replace', index=False)
        sh_table_link = await read_table_google_sheets(table_SH_name, table_link)
        sh_table_link.to_sql('Links', sq.connect('appointment.db'), if_exists='replace', index=False)
        # await update_table_google_sheets(table_SH_name, sheet_name, out_table)
        await botMes.send_message(text='База данных успешно обновлена!', chat_id=message.chat.id)

    elif message.text == 'Получить доступ к таблице':
        await botMes.send_message(text='Для получения доступа к Google таблице с базой данных напишите в чат адрес Google почты, которой будет предоставлен доступ для редактирования. Например: test@gmail.com \n'+
                                  'Доступ будет предоставлен только для Google почты! \n' +
                                  'После получения подтверждения о получении доступа, Вы можете зайти в Google диск выбранной почты и увидеть таблицу в разделе "Доступные"' , chat_id=message.chat.id)

    elif '@gmail.com' in message.text and await parametr_search_from_db("user_role", table_name_db, message.chat.id) == 'Админ':
        try:
            await create_writer_google_sheets(table_SH_name, message.text)
            await botMes.send_message(text='Вам предоставлены права на редактирование таблицы!', chat_id=message.chat.id)
        except:
            await botMes.send_message(text='Вы ввели неверный адрес электронной почты!',
                                      chat_id=message.chat.id)




@bot.message_handler(content_types=types.ContentType.CONTACT)
async def contacts(message: types.Message, table_name_db=table_name_db):
    calB = await user_id_search_from_db(table_name_db, message.contact.phone_number)
    if calB is None:
        await message.reply(f"Вас нет в базе участников мероприятия! Пожалуйста, обратитесь за консультацией  к администраторам.")
    else:
        await user_id_from_db(table_name_db = table_name_db, user_id = message.chat.id, user_phone = message.contact.phone_number)
        # markup = InlineKeyboardMarkup()  # Определяем кнопку
        # markup.add(InlineKeyboardButton(text=f'Начнем', callback_data=f'start'))  # Создаем кнопку старта
        await message.reply("Ваш номер успешно получен!")
        if await parametr_search_from_db("user_role", table_name_db, message.chat.id) == "Гость":
            await message.reply(f'Здравствуйте, {await parametr_search_from_db("user_name", table_name_db, message.chat.id)}! \n'
                                'Добро пожаловать в телеграм-бот Совещания!\n' 
                                'Здесь Вы можете узнать актуальную информацию о Вашем пребывании в Новосибирске. \n'
                                'При возникновении любых вопросов Вы можете воспользоваться кнопкой "Помощь", и наша команда поддержки ответит Вам в кратчайшие')
            buttons = [['Информация о прибытии', 'Информация о гостинице'], ['Информация об отъезде', 'Досуг'],
                       ['Помощь']]
        else:
            await message.reply(f"Здравствуйте, {await parametr_search_from_db('user_name', table_name_db, message.chat.id)}! \n"
                                "Вы зарегистрированы в роли админа.")
            buttons = [['Информация о прибытии', 'Информация о гостинице'], ['Информация об отъезде', 'Досуг'], ['Обновить базу', 'Получить доступ к таблице'],['Помощь']]
        markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=False)
        await botMes.send_message(chat_id=message.chat.id, text='Что вы хотите узнать?', reply_markup=markup)

# @bot.message_handler()  # Обрабатываем текстовые сообщения
# async def start(message: types.message):
#     await message.reply(emoji.emojize(
#         "Увы! :weary_face: Я умею общаться только кнопками(	:woman_facepalming: Поэтому, пожалуйста, напишите мне /start, чтобы снова начать общение! :beating_heart:"))  # Выводим сопутствующее сообщение

if __name__ == '__main__':
    # Бесконечно запускаем бот и игнорим ошибки
    while True:
        try:
            executor.start_polling(bot, on_startup=on_startup)
        except:
            pass