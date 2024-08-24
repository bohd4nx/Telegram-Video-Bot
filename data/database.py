import sqlite3
from datetime import datetime
from cfg import DATABASE


def initialize_db():
    """Initialize the database and create tables if they don't exist."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            usage_count INTEGER DEFAULT 0,
            registration_date TEXT
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS error_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            error_message TEXT,
            timestamp TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            message_type TEXT,
            content TEXT,
            timestamp TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        ''')
    conn.commit()


def save_feedback(user_id, username, message_text):
    """Save the feedback to the database."""
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO feedback (user_id, username, message_type, content, timestamp)
        VALUES (?, ?, ?, ?, ?)
        ''', (user_id, username, 'text', message_text, timestamp))
        conn.commit()


def add_user(user_id, username, first_name, last_name):
    """Add a new user to the database."""
    registration_date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT OR IGNORE INTO users (user_id, username, first_name, last_name, registration_date)
        VALUES (?, ?, ?, ?, ?)
        ''', (user_id, username, first_name, last_name, registration_date))
        conn.commit()


def usage(user_id):
    """Increment the usage count for a user."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE users SET usage_count = usage_count + 1
        WHERE user_id = ?
        ''', (user_id,))
        conn.commit()


def error(user_id, username, error_message):
    """Log an error message in the database."""
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO error_logs (user_id, username, error_message, timestamp)
        VALUES (?, ?, ?, ?)
        ''', (user_id, username, error_message, timestamp))
        conn.commit()


def errors_count() -> int:
    """Get the count of error logs from the database."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM error_logs')
        count = cursor.fetchone()[0]
    return count


def statistics():
    """Get statistics about the bot usage and number of users."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users')
        total_users = cursor.fetchone()[0]
        cursor.execute('SELECT SUM(usage_count) FROM users')
        total_usage = cursor.fetchone()[0]
        return total_users, total_usage
