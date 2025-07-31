import sqlite3

def initialize_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        age INTEGER NOT NULL,
                        gender TEXT NOT NULL,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL
                      )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS registration_status (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        status TEXT NOT NULL
                      )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS addresses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        address TEXT NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                      )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS words (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        word TEXT NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                      )''')

    conn.commit()
    conn.close()

# Function to check if the username is already taken
def is_username_taken(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result is not None  # Returns True if username exists, otherwise False

def register_user(username, password, first_name, last_name, age, gender):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Check if the username is already taken
    if is_username_taken(username):
        conn.close()
        return False  # Username is taken

    try:
        cursor.execute('INSERT INTO users (first_name, last_name, age, gender, username, password) VALUES (?, ?, ?, ?, ?, ?)',
                       (first_name, last_name, age, gender, username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def set_registration_complete():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO registration_status (status) VALUES ("completed")')
    conn.commit()
    conn.close()

def is_registration_complete():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM registration_status WHERE status="completed"')
    result = cursor.fetchone()
    conn.close()
    return result[0] > 0

def validate_login(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        user_details = {
            'id': user[0],
            'first_name': user[1],
            'last_name': user[2],
            'age': user[3],
            'gender': user[4],
            'username': user[5],
        }
        return user_details
    return None

def add_address(user_id, address):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO addresses (user_id, address) VALUES (?, ?)', (user_id, address))
    conn.commit()
    conn.close()

def get_addresses(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT address FROM addresses WHERE user_id=?', (user_id,))
    addresses = cursor.fetchall()
    conn.close()
    return [address[0] for address in addresses]

def update_address(user_id, old_address, new_address):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE addresses SET address=? WHERE user_id=? AND address=?', (new_address, user_id, old_address))
    conn.commit()
    conn.close()

def remove_address(user_id, address):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM addresses WHERE user_id=? AND address=?', (user_id, address))
    conn.commit()
    conn.close()

# New functions for managing words

def add_word(user_id, word):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO words (user_id, word) VALUES (?, ?)', (user_id, word))
    conn.commit()
    conn.close()

def get_words(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT word FROM words WHERE user_id=?', (user_id,))
    words = cursor.fetchall()
    conn.close()
    return [word[0] for word in words]

def update_word(user_id, old_word, new_word):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE words SET word=? WHERE user_id=? AND word=?', (new_word, user_id, old_word))
    conn.commit()
    conn.close()

def remove_word(user_id, word):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM words WHERE user_id=? AND word=?', (user_id, word))
    conn.commit()
    conn.close()
