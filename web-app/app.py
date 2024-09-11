from flask import Flask, render_template
import psycopg

app = Flask(__name__)

def get_latest_data():
    conn = psycopg.connect(
        dbname="sensor",
        user="postgres",
        password="1Ab2",
        host="localhost"
    )
    cur = conn.cursor()
    cur.execute("SELECT sensor_type, value FROM sensor_data ORDER BY timestamp DESC LIMIT 2")
    data = cur.fetchall()
    conn.close()
    return {row[0]: row[1] for row in data}

@app.route('/')
def home():
    data = get_latest_data()
    return render_template('dashboard.html', temp=data.get('Temperature'), hum=data.get('Humidity'))

if __name__ == "__main__":
    app.run(debug=True)
