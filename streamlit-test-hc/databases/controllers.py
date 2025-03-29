import sqlite3

def put_plague_register(data, path):
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        cursor.executemany('INSERT INTO registers (plague, timestamp, id_image ,location) VALUES (?, ?, ?, ?)', data)

        conn.commit()

    cursor.close()

def get_plague_register(path, limite=False):
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        if not limite:
            cursor.execute('SELECT * FROM registers')
        else:
            cursor.execute(f'SELECT * FROM registers LIMIT {limite}')

        data = cursor.fetchall()
    
    cursor.close()
    return data

def get_plague_database(path):
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM plague')

        data = cursor.fetchall()
    
    cursor.close()
    return data 

def get_single_plague_database(path, plague):
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM plague WHERE name = "{plague}"')

        data = cursor.fetchall()
    
    cursor.close()
    return data 