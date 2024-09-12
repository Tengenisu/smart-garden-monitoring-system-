import psycopg
from werkzeug.security import generate_password_hash, check_password_hash

def get_db_connection():
    conn = psycopg.connect(
        dbname="sensor",
        user="postgres",
        password="1Ab2",
        host="localhost"
    )
    return conn

def register_user(email, password):
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Check if email already exists
    cur.execute('SELECT id FROM users WHERE email = %s', (email,))
    if cur.fetchone():
        cur.close()
        conn.close()
        return False  # Email already exists
    
    # Insert new user
    hashed_password = generate_password_hash(password)
    cur.execute('INSERT INTO users (email, password_hash) VALUES (%s, %s)',
                (email, hashed_password))
    conn.commit()
    cur.close()
    conn.close()
    return True  # Registration successful

def authenticate_user(email, password):
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Fetch user by email
    cur.execute('SELECT password_hash FROM users WHERE email = %s', (email,))
    user = cur.fetchone()
    
    if user and check_password_hash(user[0], password):
        cur.close()
        conn.close()
        return True  # Authentication successful
    
    cur.close()
    conn.close()
    return False  # Authentication failed
