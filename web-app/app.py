from flask import Flask, render_template, request, redirect, url_for, flash
from auth import register_user, authenticate_user, get_db_connection
from flask_wtf import FlaskForm
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo
import random
from data_collector import log_data

app = Flask(__name__)
app.secret_key = 'your_secret_key'

from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class SignupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match')
    ])

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, name, email FROM users WHERE id = %s', (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    
    if user:
        return User(user_id=user[0], name=user[1], email=user[2])
    return None

# User class
class User(UserMixin):
    def __init__(self, user_id, name, email):
        self.id = user_id
        self.name = name
        self.email = email

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        print("Form validated!")
        name = form.name.data
        email = form.email.data
        password = form.password.data
        
        if register_user(email, password):
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Email already exists. Please try again.', 'error')
    else:
        print("Form errors:", form.errors)
    
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        if authenticate_user(email, password):
            user = User(email=email, name='', user_id=1)  # Adjust as needed
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))  # Redirect to a protected page
        else:
            flash('Invalid email or password. Please try again.', 'error')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/')
@login_required
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

if __name__ == "__main__":
    app.run(debug=True)
