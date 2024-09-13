from flask import Flask, render_template, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        dbname="sensor",
        user="postgres",
        password="Aryan1027@@",
        host="localhost",
        cursor_factory=RealDictCursor
    )

@app.route('/')
def index():
    return render_template('history.html')

@app.route('/history', methods=['GET'])
def get_history():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not start_date or not end_date:
        return render_template('history.html')

    conn = get_db_connection()
    cur = conn.cursor()
    query = '''
    SELECT timestamp, sensor_type, value
    FROM sensor_data
    WHERE timestamp BETWEEN %s AND %s
    ORDER BY timestamp
    '''
    cur.execute(query, (start_date, end_date))
    data = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('history.html', data=data)

@app.route('/plot_data', methods=['GET'])
def plot_data():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    conn = get_db_connection()
    cur = conn.cursor()
    query = '''
    SELECT timestamp, sensor_type, value
    FROM sensor_data
    WHERE timestamp BETWEEN %s AND %s
    ORDER BY timestamp
    '''
    cur.execute(query, (start_date, end_date))
    data = cur.fetchall()
    cur.close()
    conn.close()

    timestamps = []
    temperatures = []
    humidities = []
    soil_moistures = []
    light_intensities = []

    for row in data:
        timestamps.append(row['timestamp'].isoformat())
        if row['sensor_type'] == 'temperature':
            temperatures.append(row['value'])
        elif row['sensor_type'] == 'humidity':
            humidities.append(row['value'])
        elif row['sensor_type'] == 'soil_moisture':
            soil_moistures.append(row['value'])
        elif row['sensor_type'] == 'light_intensity':
            light_intensities.append(row['value'])

    return render_template('plot.html', 
                           timestamps=timestamps, 
                           temperatures=temperatures, 
                           humidities=humidities, 
                           soil_moistures=soil_moistures, 
                           light_intensities=light_intensities)

if __name__ == '__main__':
    app.run(debug=True)