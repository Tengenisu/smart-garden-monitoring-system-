import psycopg

def log_data(sensor_type, value):
    try:
        with psycopg.connect(
            dbname="sensor",
            user="postgres",
            password="1Ab2",
            host="localhost"
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(
                """
                INSERT INTO sensor_data (sensor_type, value, timestamp)
                VALUES (%s, %s, NOW())
                """,
                (sensor_type, value)
            )
            conn.commit()
    except psycopg.Error as e:
        # Log the exception or handle it as necessary
        print(f"An error occurred: {e}")
