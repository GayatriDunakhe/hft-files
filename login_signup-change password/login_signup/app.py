from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Email, Length, Regexp
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


# Validation for signup page
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message="Invalid email address")])
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


# Route for signup page
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


# Class for login page
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


# Route for login page
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
    return redirect(url_for('change_password'))


class ChangePasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message="Invalid email address")])
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=8),
        Regexp(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])',
               message='Password must contain at least 8 characters, one uppercase, one lowercase, one special character, and one number.')
    ])
    confirm_new_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match')
    ])
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        old_password = form.old_password.data
        new_password = form.new_password.data
        email = form.email.data  # Get the user's email

        # Check if the old password matches the user's current password
        cursor.execute("SELECT id FROM user3 WHERE email = %s AND password = %s", (email, old_password))
        user_id = cursor.fetchone()
     
        if user_id:
             # Fetch results to clear the cursor
            cursor.fetchall()

            # Create a new cursor for the update query
            update_cursor = db.cursor()
            update_cursor.execute("UPDATE user3 SET password = %s WHERE id = %s", (new_password, user_id[0]))
            db.commit()
            update_cursor.close()  # Close the update cursor

           
            flash('Password changed successfully.', 'password_changed')
            return redirect(url_for('dashboard'))
        else:
            flash('Password change failed. Please check your old password.', 'password_change_failed')

    return render_template('change_password.html', form=form)



if __name__ == '__main__':
    app.run(debug=True)
