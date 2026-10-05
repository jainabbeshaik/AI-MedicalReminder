import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("medical.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# Create Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS medicines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    medicine_name TEXT NOT NULL,
    dosage TEXT NOT NULL,
    medicine_time TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL
)
""")

# Create Medicines table
cursor.execute("""
CREATE TABLE IF NOT EXISTS medicines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    medicine_name TEXT NOT NULL,
    dosage TEXT NOT NULL,
    medicine_time TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

conn.commit()
conn.close()

print("Database created successfully!")