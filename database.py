import sqlite3

def init_db():
    conn = sqlite3.connect("movement.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        latitude REAL,
        longitude REAL,
        timestamp TEXT,
        landmark TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_data(lat, lon, timestamp, landmark):
    conn = sqlite3.connect("movement.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO movements (latitude, longitude, timestamp, landmark)
    VALUES (?, ?, ?, ?)
    """, (lat, lon, timestamp, landmark))

    conn.commit()
    conn.close()