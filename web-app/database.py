import psycopg

def init_db():
    conn = psycopg.connect(
        dbname="sensor",
        user="postgres",
        password="1Ab2",
        host="localhost"
    )
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS sensor_data (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                    sensor_type VARCHAR(50),
                    value REAL)''')
    conn.commit()
    cur.close()
    conn.close()

init_db()
