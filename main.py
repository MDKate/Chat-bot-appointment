#Импорты библиотек
import pandas as pd
import numpy as np
import datetime
import os
import pathlib
import transliterate
import shutil
import sqlite3 as sq
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
#Импорты функций
from SQL import db_start, user_id_from_db, user_id_search_from_db, DB_replace_from_db, parametr_search_from_db, \
    all_table_from_db, list_table_from_db, help_from_db, table_help_insert_from_db, photo_insert_from_db
from quickstart import create_writer_google_sheets, read_table_google_sheets, update_table_google_sheets, create_table_google_sheets
from QR import generate_qrcode
#Подключение к боту
botMes = Bot(open(os.path.abspath('token.txt')).read())
bot = Dispatcher(botMes)
#Задаем названия элементов БД
table_SH_name = 'Бот: встреча'
sheet_name = 'DB'
table_name_db = 'CBAppointment'
table_link = "Links"
tab_mes = 'Message'

async def on_startup(_): #Проверка существования базы и подключение
    await db_start()




@bot.message_handler(commands=['start'])  # Начинаем работу
async def start(message: types.message):
    #Получаем текст сообщения
    table_message = await read_table_google_sheets(table_SH_name, tab_mes)
    text = table_message['message'][0]
    #Созщдаем кнопку
    request_contact_button = KeyboardButton(text="Отправить контакт", request_contact=True)
    reply_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    reply_markup.add(request_contact_button)
    #Отправляем сообщение с кнопкой
    await message.reply(text=text,
                        reply_markup=reply_markup)

@bot.message_handler(content_types=types.ContentType.DOCUMENT) #Перезагрузка таблиц ПД
async def process_document(message: types.Message):
    #Получить документ
    document = message.document
    #Проверяем, эксель ли это
    if ".xlsx" in document.file_name:
        #Получаем имя документа
        docName = document.file_name.partition('.')[0]
        #Скачиваем файл
        await document.download(destination_file=f'{document.file_name}')
        #Обновляем таблицу в бд в соотвествтии с файлом
        table_replace = pd.read_excel(os.path.abspath(document.file_name))
        table_replace.to_sql(docName, sq.connect('appointment.db'), if_exists='replace', index=False)
        #Считываем текст сообщения
        table_message = await read_table_google_sheets(table_SH_name, tab_mes)
        text = table_message['message'][1]
        #Отправляем сообщение
        await botMes.send_message(text=f"{text.format(docName)}", chat_id=message.chat.id)
    else: #если это иной файл
        #Считываем текст сообщения
        table_message = await read_table_google_sheets(table_SH_name, tab_mes)
        text = table_message['message'][2]
        #Отправляем сообщение
        await botMes.send_message(text=text, chat_id=message.chat.id)


@bot.message_handler(content_types='text') #Обработка всех текстовых сообщений
async def handle_message(message: types.Message):
    # await botMes.send_message(text='В связи с окончанием мероприятия чат-бот больше не отвечает на вопросы. Приносим свои извинения!', chat_id=message.chat.id)
    link_table_read = pd.DataFrame(await list_table_from_db(table_link))
    def link_hide(link_table_read): #Заготовка списка ссылок для досуга
        txt=""
        for i in range(0, len(link_table_read)):
            txt += f'<a href="{link_table_read[1][i]}">{link_table_read[0][i]} </a> \n'
        return txt


    if message.text == 'Информация о прибытии': #Реакция на кнопку Информация о прибытии
        #Если информации нет для человека
        if await parametr_search_from_db("phone_meeting", table_name_db, message.chat.id) is None or len(str(await parametr_search_from_db("phone_meeting", table_name_db, message.chat.id)))<3:
            #Считываем текст сообщения
            table_message = await read_table_google_sheets(table_SH_name, tab_mes)
            text = table_message['message'][3]
            #Отправляем сообщение
            await botMes.send_message(text=f'{text}', chat_id=message.chat.id, parse_mode=types.ParseMode.HTML)
        else: #Если информация есть для человека
            #Считываем текст сообщения
            table_message = await read_table_google_sheets(table_SH_name, tab_mes)
            text = table_message['message'][4]
            #Делаем номер телефона ссылкой
            phoneMeeting = "+" + str(int(await parametr_search_from_db("phone_meeting", table_name_db, message.chat.id)))
            #Формируем сообщение
            text = text.format(await parametr_search_from_db("user_name", table_name_db, message.chat.id),
                                 await parametr_search_from_db("place_arrival", table_name_db, message.chat.id),
                                 await parametr_search_from_db("date_arrival", table_name_db, message.chat.id),
                                 await parametr_search_from_db("time_arrival", table_name_db, message.chat.id),
                                 await parametr_search_from_db("name_meeting", table_name_db, message.chat.id),
                                 f'<a href="{phoneMeeting}">{phoneMeeting}</a>',
                                 await parametr_search_from_db("arrival_flight_number", table_name_db, message.chat.id))
            #Отправляем сообщение
            await botMes.send_message(text=f'{text}', chat_id=message.chat.id, parse_mode=types.ParseMode.HTML)

    elif message.text == 'Информация о гостинице': #Реакция на кнопку Информация о гостинице
        #Считываем текст сообщения
        table_message = await read_table_google_sheets(table_SH_name, tab_mes)
        text = table_message['message'][5]
        #Отправка сообщения
        await botMes.send_message(text=text.format(await parametr_search_from_db("user_name", table_name_db, message.chat.id),
                                                   await parametr_search_from_db("hotel_name", table_name_db, message.chat.id),
                                                   await parametr_search_from_db("hotel_address", table_name_db, message.chat.id),
                                                   await parametr_search_from_db("hotel_website", table_name_db, message.chat.id)), chat_id=message.chat.id)

    elif message.text == 'Информация об отъезде': #Реакция на кнопку Информация об отъезде
        if await parametr_search_from_db("driver_phone", table_name_db, message.chat.id) is None or len(str(await parametr_search_from_db("driver_phone", table_name_db, message.chat.id)))<3:
            #Если информации нет для человека
            #Считываем текст сообщения
            table_message = await read_table_google_sheets(table_SH_name, tab_mes)
            text = table_message['message'][6]
            #ОТправка сообщения
            await botMes.send_message(text=text.format(f'<a href="@Moiseeva_Ekaterina">@Moiseeva_Ekaterina</a>'), chat_id=message.chat.id, parse_mode=types.ParseMode.HTML)
        else: #Если информация есть для человека
            #Делаем телефон ссылкой
            driverPhone = "+" + str(int(await parametr_search_from_db("driver_phone", table_name_db, message.chat.id)))
            #Считываем текст сообщения
            table_message = await read_table_google_sheets(table_SH_name, tab_mes)
            text = table_message['message'][7]
            #Отправка сообщения
            await botMes.send_message(text=text.format(await parametr_search_from_db("user_name", table_name_db, message.chat.id),
                                                       await parametr_search_from_db("date_departure", table_name_db, message.chat.id),
                                                       await parametr_search_from_db("time_departure", table_name_db, message.chat.id),
                                                       await parametr_search_from_db("driver_name", table_name_db, message.chat.id),
                                                       f'<a href="{driverPhone}">{driverPhone}</a>',
                                                       await parametr_search_from_db("departure_flight_number", table_name_db, message.chat.id)), chat_id=message.chat.id, parse_mode=types.ParseMode.HTML)


    elif message.text == 'Досуг': #Реакция на кнопку Досуг
        #Считывае текст сообщения
        table_message = await read_table_google_sheets(table_SH_name, tab_mes)
        text = table_message['message'][8]
        #Отправляем сообщение
        await botMes.send_message(text=text.format(await parametr_search_from_db("user_name", table_name_db, message.chat.id),
                                                   link_hide(link_table_read)), chat_id=message.chat.id, parse_mode=types.ParseMode.HTML)

    elif message.text == 'Помощь': #Реакция на кнопку Помощь
        #Ставим пометку о необходимости помощи
        await help_from_db(table_name_db=table_name_db, help_request='1', user_id=message.chat.id)
        #Считываем текст сообщения
        table_message = await read_table_google_sheets(table_SH_name, tab_mes)
        text = table_message['message'][9]
        #Отправка сообщения
        await botMes.send_message(text=text, chat_id=message.chat.id)

    # elif message.text == 'Брошюра': #Реакция на кнопку Брошюра (временно исключена)
    #     table_message = await read_table_google_sheets(table_SH_name, tab_mes)
    #     text = table_message['message'][10]
    #     await botMes.send_message(text=text, chat_id=message.chat.id)

    elif message.text == 'Сгенерировать QR code': #Реакция на кнопку "Сгенерировать QR code"
        #генерим картинку
        img = await generate_qrcode(message.chat.id)
        #Считываем екст сообщения
        table_message = await read_table_google_sheets(table_SH_name, tab_mes)
        text = table_message['message'][25]
        #Отправляем сообщение и картинку
        await botMes.send_message(text=text, chat_id=message.chat.id)
        await message.answer_photo(img)

    elif message.text == 'Скачать таблицу для QR контроля':#Реакция на кнопку "Скачать таблицу для QR контроля"
        #Считываем таблицу и оставляем нужные столбцы
        df = await all_table_from_db(table_name_db)
        df = df.loc[:, ['FIO', 'user_ID']]
        # Сохранение в файл Excel
        df.to_excel(('data.xlsx'), index=False)
        # Отправка файла пользователю
        with open('data.xlsx', 'rb') as file:
            await botMes.send_document(message.chat.id, file)
        # Удаление файла
        import os
        os.remove('data.xlsx')


    elif message.text == 'Информационный канал': #Реакция на кнопку Информационный канал
        #Считываем текст сообщения
        table_message = await read_table_google_sheets(table_SH_name, tab_mes)
        text = table_message['message'][11]
        #Отправляем сообщение
        await botMes.send_message(text=text.format('<a href="https://t.me/+l15DTn95GDc4ZWRi">ссылка</a>'), chat_id=message.chat.id, parse_mode=types.ParseMode.HTML)


    elif await parametr_search_from_db('help_request', table_name_db, message.chat.id) == '1': #Пересылка запроса о помощи
        #Обновляем состояние запроса на помощь
        await help_from_db(table_name_db, '0', message.chat.id)
        hID = await table_help_insert_from_db(message.chat.id, message.text)
        if await parametr_search_from_db("user_phone", table_name_db, message.chat.id) is None or len(str(await parametr_search_from_db("user_phone", table_name_db, message.chat.id)))<3:
            #Если человека нет в базе
            #Считываем текст сообщения
            table_message = await read_table_google_sheets(table_SH_name, tab_mes)
            text = table_message['message'][12]
            #ОТправляем сообщение
            await botMes.send_message(text=text.format('<a href="@Moiseeva_Ekaterina">@Moiseeva_Ekaterina</a>') , chat_id=message.chat.id, parse_mode=types.ParseMode.HTML)
        else: #Если человек есть в базе
            #Делаем номер телефона ссылкой
            phoneMeeting = "+" + str(int(await parametr_search_from_db("user_phone", table_name_db, message.chat.id)))
            #Возвращаем кнопки
            buttons = [['Информация о прибытии', 'Информация о гостинице'], ['Информация об отъезде', 'Досуг'],
                       ['Помощь', 'Информационный канал'], ['Сгенерировать QR code']]
            markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=False)
            #Считываем текст сообщения
            table_message = await read_table_google_sheets(table_SH_name, tab_mes)
            text = table_message['message'][13]
            #Отправляем сообщение
            await botMes.send_message(text=text, chat_id=message.chat.id, reply_markup=markup)
            text = table_message['message'][14]
            #Отправляем сообщение
            await botMes.send_message(text=text.format(hID,
                                                       await parametr_search_from_db("FIO", table_name_db, message.chat.id),
                                                       f'<a href="{phoneMeeting}">{phoneMeeting}</a>', message.text), chat_id='-899649626', parse_mode=types.ParseMode.HTML)

    elif message.text == 'Обновить основную таблицу': #Реакция на кнопку Обновить основную таблицу (иногда матерится)
        #Получаем таблицу из базы и из гугла
        db_table = await all_table_from_db(table_name_db)
        sh_table = await read_table_google_sheets(table_SH_name, sheet_name)
        out_table = sh_table.copy()
        out_table['user_ID'] = ""
        out_table['help_request'] = ""
        db_table = db_table.astype({'ID': object})
        #Добавляем в копию таблицы гугла нехватающие параметры
        for i in range(0, len(sh_table)):
            try:
                out_table['user_ID'][i] = (db_table[sh_table['ID'] == str(db_table['ID'][i])]['user_ID'].values)[0]
            except:
                out_table['user_ID'][i] = np.nan

        for i in range(0, len(sh_table)):
            try:
                out_table['help_request'][i] = (db_table[sh_table['ID'] == str(db_table['ID'][i])]['help_request'].values)[0]
            except:
                out_table['help_request'][i] = np.nan

        #Перезаписываем таблицу в бд
        out_table.to_sql('CBAppointment', sq.connect('appointment.db'), if_exists='replace', index=False)
        sh_table_link = await read_table_google_sheets(table_SH_name, table_link)
        sh_table_link.to_sql('Links', sq.connect('appointment.db'), if_exists='replace', index=False)
        #Считываем текст ответа
        table_message = await read_table_google_sheets(table_SH_name, tab_mes)
        text = table_message['message'][15]
        #Отправляем сообщение
        await botMes.send_message(text=text, chat_id=message.chat.id)

    elif message.text == 'Обновить таблицу ПД': #Реакция на кнопку Обновить таблицу ПД
        #Считываем текст сообщения
        table_message = await read_table_google_sheets(table_SH_name, tab_mes)
        text = table_message['message'][16]
        #Отправляем сообщение
        await botMes.send_message(text=text, chat_id=message.chat.id)

    elif message.text == 'Получить доступ к таблице': #Реакция на кнопку Получить доступ к таблице
        #Считать текст сообщения
        table_message = await read_table_google_sheets(table_SH_name, tab_mes)
        text = table_message['message'][17]
        #Отправить сообщение
        await botMes.send_message(text=text, chat_id=message.chat.id)

    elif '@gmail.com' in message.text and await parametr_search_from_db("user_role", table_name_db, message.chat.id) == 'Админ': #Если это админ и верно введена почта, то продолжить
        try:
            #Добавить права на редактирование гугл таблицы
            await create_writer_google_sheets(table_SH_name, message.text)
            #Считать текст сообщения
            table_message = await read_table_google_sheets(table_SH_name, tab_mes)
            text = table_message['message'][18]
            #Отправить сообщение
            await botMes.send_message(text=text, chat_id=message.chat.id)
        except:
            #Считать текст сообщения
            table_message = await read_table_google_sheets(table_SH_name, tab_mes)
            text = table_message['message'][19]
            #Отправить сообщение
            await botMes.send_message(text=text,
                                      chat_id=message.chat.id)


@bot.message_handler(content_types=types.ContentType.PHOTO) #Обработка фотографий
async def save_photo(message: types.Message):
    if await parametr_search_from_db('photo', table_name_db, message.chat.id) != '1':
        # Получаем информацию о фотографии
        photo = message.photo[-1]

        # Сохраняем фотографию во временную папку
        photo_path = os.path.join(os.path.abspath('Base/'), f'photo_{photo.file_unique_id}.jpg')
        await photo.download(destination=photo_path)

        #Создаем транскрипцию ФИО по данным из базы
        name = await parametr_search_from_db('FIO', table_name_db, message.chat.id)
        transcription = transliterate.translit(name, 'ru', reversed=True)
        transcription = transcription.replace(" ", "_")

        # Перемещаем фотографию в нужную папку
        final_path = os.path.join(os.path.abspath('Base/'), f'{transcription}_1.jpg')
        shutil.move(photo_path, final_path)

        await photo_insert_from_db(message.chat.id, table_name_db, "1")

        # Отправляем пользователю сообщение о сохранении фотографии
        await message.reply("Фотография сохранена!")
    else:
        await message.reply("Вы уже внесли фото! Новое фото не будет сохранено.")

@bot.message_handler(content_types=types.ContentType.CONTACT) #Регистрация пользователя
async def contacts(message: types.Message, table_name_db=table_name_db):
    #Ищем человека в БД
    calB = await user_id_search_from_db(table_name_db, message.contact.phone_number)
    if calB is None: #Если пользователя нет в БД
        #Считываем текст сообщения
        table_message = await read_table_google_sheets(table_SH_name, tab_mes)
        text = table_message['message'][20]
        #Отправляем сообщение
        await message.reply(text=text)
        text = table_message['message'][21]
        #Отправляем сообщение
        await botMes.send_message(text=text.format(message.contact.full_name,
                                                   f'<a href="+{message.contact.phone_number}">+{message.contact.phone_number}</a>')
                                       , chat_id='-899649626',
                                  parse_mode=types.ParseMode.HTML)


    else: #Если пользователь есть в БД
        await user_id_from_db(table_name_db = table_name_db, user_id = message.chat.id, user_phone = message.contact.phone_number)
        #Если у пользователя роль Гость
        if await parametr_search_from_db("user_role", table_name_db, message.chat.id) == "Гость":
            #Считываем текст сообщения
            table_message = await read_table_google_sheets(table_SH_name, tab_mes)
            text = table_message['message'][22]
            #Отправляем сообщение
            await message.reply(text=text)
            #Создаем кнопки
            buttons = [['Информация о прибытии', 'Информация о гостинице'], ['Информация об отъезде', 'Досуг'],
                       ['Помощь', 'Информационный канал'], ['Сгенерировать QR code']]
        else: #Если у пользователя роль Админ
            #Считываем текст сообщения
            table_message = await read_table_google_sheets(table_SH_name, tab_mes)
            text = table_message['message'][23]
            #Отправляем сообщение
            await message.reply(text=text.format(await parametr_search_from_db('user_name', table_name_db, message.chat.id)))
            #Создаем кнопки
            buttons = [['Информация о прибытии', 'Информация о гостинице'], ['Информация об отъезде', 'Досуг'],
                       ['Обновить основную таблицу', 'Обновить таблицу ПД'],
                       ['Получить доступ к таблице', 'Сгенерировать QR code'],
                       ['Скачать таблицу для QR контроля']]
        #Считываем текст сообщения
        markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=False)
        table_message = await read_table_google_sheets(table_SH_name, tab_mes)
        text = table_message['message'][24]
        #Отправляем сообщение с кнопками
        await botMes.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)

if __name__ == '__main__':
    # Бесконечно запускаем бот и игнорим ошибки
    while True:
        try:
            executor.start_polling(bot, on_startup=on_startup)
        except:
            pass