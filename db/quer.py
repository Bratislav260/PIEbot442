CREATE_TABLE_LEGO = """CREATE TABLE IF NOT EXISTS Lego_Store 
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255),
    size VARCHAR(255),
    category VARCHAR(255),
    price VARCHAR(255),
    id_product VARCHAR(255),
    photo TEXT
)"""

INSERT_LEGO = """
    INSERT INTO Lego_Store(name, size, category, price, id_product, photo)
    VALUES (?, ?, ?, ?, ?, ?)
"""


CREATE_TABLE_LEGO_GET = """CREATE TABLE IF NOT EXISTS Lego_Get 
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_product VARCHAR(255),
    size VARCHAR(255),
    count VARCHAR(255),
    number VARCHAR(255)
)"""

INSERT_LEGO_GET = """
    INSERT INTO Lego_Get(id_product, size, count, number)
    VALUES (?, ?, ?, ?)
"""