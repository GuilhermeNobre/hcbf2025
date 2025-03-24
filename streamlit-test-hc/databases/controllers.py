import sqlite3



def put_plague_register(data, path):
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        cursor.executemany('INSERT INTO registers (plague, timestamp, location) VALUES (?, ?, ?)', data)

        conn.commit()

    cursor.close()

def get_plague_register(path):
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM registers')
        data = cursor.fetchall()
    
    cursor.close()
    return data