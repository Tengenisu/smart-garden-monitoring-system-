import psycopg
import random
import time

def log_data(sensor_type, value):
    conn = psycopg.connect(
        dbname="sensor",
        user="postgres",
        password="Aryan1027@@",
        host="localhost"
    )
    cur = conn.cursor()
    cur.execute("INSERT INTO sensor_data (sensor_type, value) VALUES (%s, %s)", (sensor_type, value))
    conn.commit()
    cur.close()
    conn.close()

def check_alerts(sensor_type, value):
    if sensor_type == 'Temperature' and value > 30:
        print(f"ALERT: {sensor_type} is too high! Value: {value}")
    if sensor_type == 'Humidity' and value < 35:
        print(f"ALERT: {sensor_type} is too low! Value: {value}")


# Simulating sensor data logging
while True:
    temp = round(random.uniform(15.0, 35.0), 2)
    humidity = round(random.uniform(30.0, 70.0), 2)
    log_data('Temperature', temp)
    log_data('Humidity', humidity)
    time.sleep(5)
