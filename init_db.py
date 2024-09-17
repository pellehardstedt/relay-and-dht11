import sqlite3

def init_db():
    conn = sqlite3.connect('sensor_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            date TEXT,
            temperature REAL,
            humidity REAL,
            weather_temperature REAL,
            weather_feels_like REAL,
            weather_humidity REAL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()