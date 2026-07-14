import sqlite3

conn = sqlite3.connect("monitor.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS devices (
    hostname TEXT PRIMARY KEY,
    username TEXT,
    operating_system TEXT,
    ip_address TEXT,
    cpu_usage REAL,
    ram_usage REAL,
    disk_usage REAL,
    last_seen REAL
)
""")

conn.commit()