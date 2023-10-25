from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import  PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired,EqualTo,Email,Length, Regexp
import mysql.connector


app = Flask(__name__)
# Configure your MySQL database connection
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root1234',
    database='sys'
)

cursor = db.cursor()


app.config['SECRET_KEY'] = 'mysecretkey' 


# validation for signup page
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message="Invalid email address")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8),
        Regexp(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])',
               message='Password must contain at least 8 characters, one uppercase, one lowercase, one special character, and one number.')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')

    def validate_email(self, field):
        email = field.data
        # Check if the email already exists in the database
        cursor.execute("SELECT id FROM user3 WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            raise ValidationError('Email already exists')  
        # Close the result set after fetching results
        cursor.close()  


# route for signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Insert user data into the database
        cursor.execute("INSERT INTO user3 (email, password) VALUES (%s, %s)", (email, password))
        db.commit()
        flash('Registration successful. You can now log in.', 'registration_success')
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)

# class for login page 
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


# route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Check user credentials in the database
        cursor.execute("SELECT * FROM user3 WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()

        if user:
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Please check your credentials.', 'login_failed')

    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    return 'Welcome to the Dashboard'


if __name__ == '__main__':
    app.run(debug=True)