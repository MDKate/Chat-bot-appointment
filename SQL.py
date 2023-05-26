import sqlite3 as sq
import pandas as pd
from quickstart import create_table_google_sheets, read_table_google_sheets

async def db_start():
    global db, cur
    db = sq.connect('appointment.db')
    cur = db.cursor()
    table_name = 'CBAppointment'
    sheet_name = "DB"
    cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    result = cur.fetchone()
    if result is None:
        data = read_table_google_sheets("Чат-бот встреча", sheet_name)
        data['user_ID'] = ""
        data.to_sql(table_name, sq.connect('appointment.db'), index=False)
    table_name = 'Links'
    sheet_name = "Links"
    cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    result = cur.fetchone()
    if result is None:
        data = read_table_google_sheets("Чат-бот встреча", sheet_name)
        data.to_sql(table_name, sq.connect('appointment.db'), index=False)
    db.commit()

async def user_id_from_db(table_name_db, user_id, user_phone):
    sql_update_query = f"""Update {table_name_db} set user_ID = {user_id} where user_phone = {user_phone}"""
    cur.execute(sql_update_query)
    db.commit()

async def help_from_db(table_name_db, help_request, user_id):
    sql_update_query = f"""Update {table_name_db} set help_request = {help_request} where user_ID = {user_id}"""
    cur.execute(sql_update_query)
    db.commit()

async def user_id_search_from_db(table_name_db, user_phone):
    # cursor = db.cursor()
    cur.execute(f"SELECT user_name FROM {table_name_db} WHERE user_phone = {user_phone}")
    result = cur.fetchone()
    # await result[0]
    return result[0] if result else None

async def list_table_from_db(table_name_db):
    df = pd.read_sql(f"SELECT * FROM {table_name_db}", sq.connect('appointment.db')).values
    # txt = ""
    # for i in range(0, len(df)):
    #     txt+= df[i][0] + " " + df[i][1] + "\n"
    # return txt
    return df

async def all_table_from_db(table_name_db):
    df = pd.read_sql(f"SELECT * FROM {table_name_db}", sq.connect('appointment.db'))
    return df

async def parametr_search_from_db(parametr, table_name_db, user_ID):
    # cursor = db.cursor()
    cur.execute(f"SELECT {parametr} FROM {table_name_db} WHERE user_ID = {user_ID}")
    result = cur.fetchone()
    # await result[0]
    return result[0] if result else None

async def DB_replace_from_db(table_name, sheet_name):
    data = read_table_google_sheets(table_name, sheet_name)
    data.to_sql('CBAppointment', sq.connect('appointment.db'), if_exists='replace', index=False)


# async def city_value_from_db(user_id):
#     # cursor = db.cursor()
#     cur.execute("SELECT city FROM base WHERE user_id=?", (user_id,))
#     result = cur.fetchone()
#     return result[0] if result else None
#
# async def page_value_from_db(user_id):
#     # cursor = db.cursor()
#     cur.execute("SELECT page FROM base WHERE user_id=?", (user_id,))
#     result = cur.fetchone()
#     return result[0] if result else None
#
# async def ChoosingTopicsResult_value_from_db(user_id):
#     # cursor = db.cursor()
#     cur.execute("SELECT ChoosingTopicsResult FROM base WHERE user_id=?", (user_id,))
#     result = cur.fetchone()
#     return result[0] if result else None
#