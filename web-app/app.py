from flask import Flask, render_template
import random
from data_collector import log_data

app = Flask(__name__)

@app.route('/')
def home():
    temperature = round(random.uniform(15.0, 35.0), 2)
    humidity = round(random.uniform(30.0, 70.0), 2)
    soil_moisture = round(random.uniform(0.0, 100.0), 2)
    light_intensity = round(random.uniform(100.0, 2000.0), 2)

    log_data('temperature', temperature)
    log_data('humidity', humidity)
    log_data('soil_moisture', soil_moisture)
    log_data('light_intensity', light_intensity)
    
    return render_template('dashboard.html', temp=temperature, hum=humidity, soil = soil_moisture, light = light_intensity)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

if __name__ == "__main__":
    app.run(debug=True)
