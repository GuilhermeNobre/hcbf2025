import sqlite3

def put_plague_register(data, path):
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()

        if data[0][4] == '' or data[0][4] == None or data[0][4] == ' ':
            data[0][4] = 'Nenhuma observação'

        cursor.executemany('INSERT INTO registers (plague, timestamp, id_image ,location, observations) VALUES (?, ?, ?, ?, ?)', data)

        conn.commit()

    cursor.close()

def get_plague_register(path, limite=False, start_date=None, end_date=None):
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        
        query = 'SELECT * FROM registers'
        params = []
        
        if start_date or end_date:
            conditions = []
            if start_date:
                conditions.append('timestamp >= ?')
                params.append(start_date.timestamp())
            if end_date:
                conditions.append('timestamp <= ?')
                params.append(end_date.timestamp())
            
            if conditions:
                query += ' WHERE ' + ' AND '.join(conditions)
        
        if limite:
            query += f' LIMIT {limite}'
            
        cursor.execute(query, params)
        data = cursor.fetchall()
    
    cursor.close()
    return data

def get_plague_register_by_plague(path, plague):
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM registers WHERE plague = "{plague}"')

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

def get_plague_names(path):
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM plague')

        data = cursor.fetchall()
    
    cursor.close()
    return data