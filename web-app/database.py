import psycopg

def init_db():
    try:
        conn = psycopg.connect(
            dbname="sensor",
            user="postgres",
            password="Aryan1027@@",
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
    except Exception as e:
        print(f"An error occurred: {e}")
    
print("finished")

init_db()
