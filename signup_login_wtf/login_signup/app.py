from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import  PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired,EqualTo,Email,Length, Regexp



app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey' 

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



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Registration successful. You can now log in.', 'registration_success')
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('dashboard'))
    # else:
    #     flash('Login failed. Please check your credentials.')

    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    return 'Welcome to the Dashboard'


if __name__ == '__main__':
    app.run(debug=True)