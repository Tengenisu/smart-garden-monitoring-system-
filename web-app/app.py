from flask import Flask, render_template
import random
from data_collector import log_data

app = Flask(__name__)

@app.route('/')
def home():
    temperature = round(random.uniform(15.0, 35.0), 2)
    humidity = round(random.uniform(30.0, 70.0), 2)

    log_data('temperature', temperature)
    log_data('humidity', humidity)
    
    return render_template('dashboard.html', temp=temperature, hum=humidity)

if __name__ == "__main__":
    app.run(debug=True)
