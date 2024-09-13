import psycopg

def log_data(sensor_type, value):
    try:
        # Establish connection
        with psycopg.connect(
            dbname="sensor",
            user="postgres",
            password="Aryan1027@@",
            host="localhost"
        ) as conn:
            # Use context manager for cursor
            with conn.cursor() as cur:
                # Execute SQL insert command
                cur.execute(
                    """
                    INSERT INTO sensor_data (sensor_type, value, timestamp)
                    VALUES (%s, %s, NOW())
                    """,
                    (sensor_type, value)
                )
                # Commit changes
                conn.commit()
                print("Data logged successfully")
    except psycopg.Error as e:
        # Log the exception or handle it as necessary
        print(f"An error occurred: {e}")

# Example usage
log_data("temperature", 22.5)
