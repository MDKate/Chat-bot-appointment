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

table_SH_name = 'Бот: встреча'
sheet_name = 'DB'
table_name_db = 'CBAppointment'
table_link = "Links"


async def on_startup(_):
    await db_start()



#
# @bot.message_handler(commands=['start'])  # Начинаем работу
# async def start(message: types.message):
#     # global count
#     # global page
#     request_contact_button = KeyboardButton(text="Отправить контакт", request_contact=True)
#     reply_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
#     reply_markup.add(request_contact_button)
#     await message.reply("Добрый день! Для начала работы с ботом необходимо зарегистрироваться по номеру телефона. \nДля этого нажмите на кнопку 'Отправить контакт' внизу экрана.",
#                         reply_markup=reply_markup)  # Выводим сопутствующее сообщение
#
# @bot.message_handler(content_types=types.ContentType.DOCUMENT)
# async def process_document(message: types.Message):
#     document = message.document
#     if ".xlsx" in document.file_name:
#         docName = document.file_name.partition('.')[0]
#         await document.download(destination_file=f'{document.file_name}')
#         table_replace = pd.read_excel(os.path.abspath(document.file_name))
#         table_replace.to_sql(docName, sq.connect('appointment.db'), if_exists='replace', index=False)
#         await botMes.send_message(text=f'Таблица {docName} обновлена!', chat_id=message.chat.id)
#     else:
#         await botMes.send_message(text=f'Вы загрузили некорректный файл!', chat_id=message.chat.id)
#
#

@bot.message_handler(content_types='text')
async def handle_message(message: types.Message):
    await botMes.send_message(text='В связи с окончанием мероприятия чат-бот больше не отвечает на вопросы. Приносим свои извинения!', chat_id=message.chat.id)
    # link_table_read = pd.DataFrame(await list_table_from_db(table_link))
    # def link_hide(link_table_read):
    #     txt=""
    #     for i in range(0, len(link_table_read)):
    #         txt += f'<a href="{link_table_read[1][i]}">{link_table_read[0][i]} </a> \n'
    #     return txt
    #
    #
    # if message.text == 'Информация о прибытии':
    #     if await parametr_search_from_db("phone_meeting", table_name_db, message.chat.id) is None or len(str(await parametr_search_from_db("phone_meeting", table_name_db, message.chat.id)))<3:
    #         await botMes.send_message(text=f'Данные по вашему прибытию еще не обновлены! Пожалуйста, напишите о проблеме <a href="@Moiseeva_Ekaterina">@Moiseeva_Ekaterina</a>.', chat_id=message.chat.id, parse_mode=types.ParseMode.HTML)
    #     else:
    #         phoneMeeting = "+" + str(int(await parametr_search_from_db("phone_meeting", table_name_db, message.chat.id)))
    #         await botMes.send_message(text=f'{await parametr_search_from_db("user_name", table_name_db, message.chat.id)}, Вы прибываете в город Новосибирск, {await parametr_search_from_db("place_arrival", table_name_db, message.chat.id)} {await parametr_search_from_db("date_arrival", table_name_db, message.chat.id)} {await parametr_search_from_db("time_arrival", table_name_db, message.chat.id)}. \n'+
    #                          f'Вас будет встречать {await parametr_search_from_db("name_meeting", table_name_db, message.chat.id)} <a href="{phoneMeeting}">{phoneMeeting}</a> \n'+
    #                          f'Ваш номер рейса {await parametr_search_from_db("arrival_flight_number", table_name_db, message.chat.id)}', chat_id=message.chat.id, parse_mode=types.ParseMode.HTML)
    #
    # elif message.text == 'Информация о гостинице':
    #     await botMes.send_message(text=f'{await parametr_search_from_db("user_name", table_name_db, message.chat.id)}, Вы проживаете в гостинице {await parametr_search_from_db("hotel_name", table_name_db, message.chat.id)}, {await parametr_search_from_db("hotel_address", table_name_db, message.chat.id)}, {await parametr_search_from_db("hotel_website", table_name_db, message.chat.id)}', chat_id=message.chat.id)
    #
    # elif message.text == 'Информация об отъезде':
    #     if await parametr_search_from_db("driver_phone", table_name_db, message.chat.id) is None or len(str(await parametr_search_from_db("driver_phone", table_name_db, message.chat.id)))<3:
    #
    #         await botMes.send_message(text=f'Данные по вашему отбытию еще не обновлены! Пожалуйста, напишите о проблеме <a href="@Moiseeva_Ekaterina">@Moiseeva_Ekaterina</a>.', chat_id=message.chat.id, parse_mode=types.ParseMode.HTML)
    #     else:
    #         driverPhone = "+" + str(int(await parametr_search_from_db("driver_phone", table_name_db, message.chat.id)))
    #         # Вас будет ожидать {await parametr_search_from_db("car_brand", table_name_db, message.chat.id)} {await parametr_search_from_db("number_seats", table_name_db, message.chat.id)} {await parametr_search_from_db("car_registration_number", table_name_db, message.chat.id)}.
    #         await botMes.send_message(text=f'{await parametr_search_from_db("user_name", table_name_db, message.chat.id)}, Ваш отъезд из гостиницы состоится {await parametr_search_from_db("date_departure", table_name_db, message.chat.id)} {await parametr_search_from_db("time_departure", table_name_db, message.chat.id)}.  \n '+
    #                                    f'Вас будет сопровождать {await parametr_search_from_db("driver_name", table_name_db, message.chat.id)} <a href="{driverPhone}">{driverPhone}</a>. Ваш рейс № {await parametr_search_from_db("departure_flight_number", table_name_db, message.chat.id)}.', chat_id=message.chat.id, parse_mode=types.ParseMode.HTML)
    #                                    # f'Вас будет сопровождать {await parametr_search_from_db("driver_name", table_name_db, message.chat.id)} <a href="{driverPhone}">{driverPhone}</a>. Ваш рейс № {await parametr_search_from_db("departure_flight_number", table_name_db, message.chat.id)} отправляется {await parametr_search_from_db("date_departure", table_name_db, message.chat.id)} {await parametr_search_from_db("time_departure", table_name_db, message.chat.id)}', chat_id=message.chat.id, parse_mode=types.ParseMode.HTML)
    #
    # elif message.text == 'Досуг':
    #     await botMes.send_message(text=f'{await parametr_search_from_db("user_name", table_name_db, message.chat.id)}, для того, чтобы Ваше пребывание в Новосибирске было более интересным, мы подготовили для Вас несколько ссылок. \n'+
    #                     f'{link_hide(link_table_read)}', chat_id=message.chat.id, parse_mode=types.ParseMode.HTML)
    #
    # elif message.text == 'Помощь':
    #     await help_from_db(table_name_db=table_name_db, help_request='1', user_id=message.chat.id)
    #     await botMes.send_message(text='Что вас интересует? \n'+
    #                               'Напишите ваш вопрос, и бот перешлет его организаторам.', chat_id=message.chat.id)
    #
    # elif message.text == 'Брошюра':
    #     await botMes.send_message(text='Этот раздел еще в разработке.',
    #                               chat_id=message.chat.id)
    #
    # elif message.text == 'Информационный канал':
    #     await botMes.send_message(text='Для перехода к каналу нажмите на ссылку: <a href="https://t.me/+l15DTn95GDc4ZWRi">ссылка</a> ', chat_id=message.chat.id, parse_mode=types.ParseMode.HTML)
    #
    #
    # elif await parametr_search_from_db('help_request', table_name_db, message.chat.id) == '1':
    #     await help_from_db(table_name_db, '0', message.chat.id)
    #     hID = await table_help_insert_from_db(message.chat.id, message.text)
    #     if await parametr_search_from_db("user_phone", table_name_db, message.chat.id) is None or len(str(await parametr_search_from_db("user_phone", table_name_db, message.chat.id)))<3:
    #         await botMes.send_message(text=f'Данные еще не обновлены! Пожалуйста, напишите о проблеме <a href="@Moiseeva_Ekaterina">@Moiseeva_Ekaterina</a>.', chat_id=message.chat.id, parse_mode=types.ParseMode.HTML)
    #     else:
    #         phoneMeeting = "+" + str(int(await parametr_search_from_db("user_phone", table_name_db, message.chat.id)))
    #         buttons = [['Информация о прибытии', 'Информация о гостинице'], ['Информация об отъезде', 'Досуг'],
    #                ['Помощь', 'Информационный канал']]
    #         markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=False)
    #         await botMes.send_message(text='Спасибо за обращение! Команда поддержки свяжется с вами в ближайшее время', chat_id=message.chat.id, reply_markup=markup)
    #         await botMes.send_message(text='Добрый день! Вам пришел запрос на помощь: \n'+
    #                               f'№ запроса: {hID} \n'+
    #                               f'От: {await parametr_search_from_db("user_name", table_name_db, message.chat.id)} \n'+
    #                               f'Телефон: <a href="{phoneMeeting}">{phoneMeeting}</a> \n'+
    #                               f'Текст вопроса: {message.text} \n', chat_id='-1001937614226', parse_mode=types.ParseMode.HTML)
    #
    # elif message.text == 'Обновить основную таблицу':
    #     db_table = await all_table_from_db(table_name_db)
    #     # print(db_table.columns)
    #     sh_table = await read_table_google_sheets(table_SH_name, sheet_name)
    #     # print(sh_table)
    #     out_table = sh_table.copy()
    #     out_table['user_ID'] = ""
    #     out_table['help_request'] = ""
    #     db_table = db_table.astype({'ID': object})
    #     # out_table['user_ID'] = out_table['user_ID'].fillna("0")
    #     # print(db_table.dtypes)
    #     # print(sh_table.dtypes)
    #
    #
    #     for i in range(0, len(sh_table)):
    #         try:
    #             # print(sh_table['ID'][i], db_table['ID'][i])
    #             # print(sh_table['ID'][i] == db_table['ID'][i])
    #             # print((sh_table['ID'][i]) == str(db_table['ID'][i]))
    #             # print((db_table[sh_table['ID'] == str(db_table['ID'][i])]['user_ID'].values)[0])
    #             out_table['user_ID'][i] = (db_table[sh_table['ID'] == str(db_table['ID'][i])]['user_ID'].values)[0]
    #         except:
    #             out_table['user_ID'][i] = np.nan
    #
    #     for i in range(0, len(sh_table)):
    #         try:
    #             out_table['help_request'][i] = (db_table[sh_table['ID'] == str(db_table['ID'][i])]['help_request'].values)[0]
    #         except:
    #             out_table['help_request'][i] = np.nan
    #
    #
    #     out_table.to_sql('CBAppointment', sq.connect('appointment.db'), if_exists='replace', index=False)
    #     sh_table_link = await read_table_google_sheets(table_SH_name, table_link)
    #     sh_table_link.to_sql('Links', sq.connect('appointment.db'), if_exists='replace', index=False)
    #     # await update_table_google_sheets(table_SH_name, sheet_name, out_table)
    #     await botMes.send_message(text='База данных успешно обновлена!', chat_id=message.chat.id)
    #
    # elif message.text == 'Обновить таблицу ПД':
    #     await botMes.send_message(text='Для обновления таблицы загрузите в чат файл xlsx с соответствующим именем. Например, ID.xlsx', chat_id=message.chat.id)
    #
    #
    #
    # elif message.text == 'Получить доступ к таблице':
    #     await botMes.send_message(text='Для получения доступа к Google таблице с базой данных напишите в чат адрес Google почты, которой будет предоставлен доступ для редактирования. Например: test@gmail.com \n'+
    #                               'Доступ будет предоставлен только для Google почты! \n' +
    #                               'После получения подтверждения о получении доступа, Вы можете зайти в Google диск выбранной почты и увидеть таблицу в разделе "Доступные"' , chat_id=message.chat.id)
    #
    # elif '@gmail.com' in message.text and await parametr_search_from_db("user_role", table_name_db, message.chat.id) == 'Админ':
    #     try:
    #         await create_writer_google_sheets(table_SH_name, message.text)
    #         await botMes.send_message(text='Вам предоставлены права на редактирование таблицы!', chat_id=message.chat.id)
    #     except:
    #         await botMes.send_message(text='Вы ввели неверный адрес электронной почты!',
    #                                   chat_id=message.chat.id)


#
#
# @bot.message_handler(content_types=types.ContentType.CONTACT)
# async def contacts(message: types.Message, table_name_db=table_name_db):
#     calB = await user_id_search_from_db(table_name_db, message.contact.phone_number)
#     if calB is None:
#         await message.reply(f"Вас нет в базе данных участников мероприятия! Ваш контакт направлен организаторам для включения в список участников. Организаторы скоро с вами свяжутся.")
#         await botMes.send_message(text='Добрый день! Вам пришел запрос на регистрацию на мероприятие: \n' +
#                                        f'От: {message.contact.full_name} \n' +
#                                        f'Телефон: <a href="+{message.contact.phone_number}">+{message.contact.phone_number}</a>'
#                                        , chat_id='-1001937614226',
#                                   parse_mode=types.ParseMode.HTML)
#
#
#     else:
#         await user_id_from_db(table_name_db = table_name_db, user_id = message.chat.id, user_phone = message.contact.phone_number)
#         if await parametr_search_from_db("user_role", table_name_db, message.chat.id) == "Гость":
#             await message.reply(f'Добро пожаловать в телеграм-бот совещания "Деятельность территориальных учреждений Банка России по развитию финансового рынка в регионах Российской федерации", которое состоится 26.06.2023-30.06.2023 на базе Сибирского ГУ Банка России. Здесь Вы можете узнать актуальную информацию о вашем пребывании в Новосибирске. При возникновении любых вопросов Вы можете воспользоваться кнопкой "Помощь", и наша команда поддержки ответит Вам в кратчайшие сроки')
#             buttons = [['Информация о прибытии', 'Информация о гостинице'], ['Информация об отъезде', 'Досуг'],
#                        ['Помощь', 'Информационный канал']]
#         else:
#             await message.reply(f"Здравствуйте, {await parametr_search_from_db('user_name', table_name_db, message.chat.id)}! \n"
#                                 "Вы зарегистрированы в роли Организатора.")
#             buttons = [['Информация о прибытии', 'Информация о гостинице'], ['Информация об отъезде', 'Досуг'], ['Обновить основную таблицу', 'Обновить таблицу ПД'], ['Получить доступ к таблице']]
#         markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=False)
#         await botMes.send_message(chat_id=message.chat.id, text='Что вы хотите узнать?', reply_markup=markup)

if __name__ == '__main__':
    # Бесконечно запускаем бот и игнорим ошибки
    while True:
        try:
            executor.start_polling(bot, on_startup=on_startup)
        except:
            pass