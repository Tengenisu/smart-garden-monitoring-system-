from flask import Flask, render_template
import random

app = Flask(__name__)

@app.route('/')
def home():
    # Simulate sensor data
    temperature = round(random.uniform(15.0, 35.0), 2)
    humidity = round(random.uniform(30.0, 70.0), 2)
    return render_template('dashboard.html', temp=temperature, hum=humidity)

if __name__ == "__main__":
    app.run(debug=True)
