import psycopg

def init_db():
    try:
        conn = psycopg.connect(
            dbname="sensor",
            user="postgres",
            password="1Ab2",
            host="localhost"
        )
        cur = conn.cursor()
    cur.execute('''DROP TABLE IF EXISTS sensor_data''')
    cur.execute('''CREATE TABLE IF NOT EXISTS sensor_data (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                    sensor_type VARCHAR(50),
                    value REAL)''')

    cur.execute('''DROP TABLE IF EXISTS users''')
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100),
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL)''')
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"An error occurred: {e}")
    
print("finished")

init_db()
