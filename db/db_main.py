import sqlite3 as sq
from db import quer

db = sq.connect("db/db.sqlite3")
cur = db.cursor()


async def sql_creat():
    if db:
        print("База данных подключена")
    cur.execute(quer.CREATE_TABLE_LEGO)
    cur.execute(quer.CREATE_TABLE_LEGO_GET)
    db.commit()


async def sql_insert_lego(name, size, category, price, id_product, photo):
    cur.execute(quer.INSERT_LEGO, (name, size, category, price, id_product, photo))
    db.commit()


async def sql_insert_lego_get(id_product, size, count, number):
    cur.execute(quer.INSERT_LEGO_GET, (id_product, size, count, number))
    db.commit()