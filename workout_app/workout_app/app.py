from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
#app.secret_key = 'your_secret_key'  # Change this to a strong, random secret key

# Temporary data storage (in-memory dictionaries)
workouts = {}
user_workouts = {}

# @app.route('/')
# def home():
#     if 'username' in session:
#         return redirect(url_for('workouts'))
#     return render_template('login.html')

# @app.route('/login', methods=['POST'])
# def login():
#     username = request.form.get('username')
#     password = request.form.get('password')
    
#     # In a real application, you'd perform authentication here. For simplicity, we'll assume the login is successful.
#     session['username'] = username
#     return redirect(url_for('workouts'))

# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     return redirect(url_for('home'))

@app.route('/workouts', methods=['GET', 'POST'])
def workouts():
    if 'username' not in session:
        return redirect(url_for('home'))

    username = session['username']

    if request.method == 'POST':
        exercise = request.form.get('exercise')
        sets = int(request.form.get('sets'))
        reps = int(request.form.get('reps'))
        duration = int(request.form.get('duration'))

        if username not in user_workouts:
            user_workouts[username] = []

        user_workouts[username].append({
            'exercise': exercise,
            'sets': sets,
            'reps': reps,
            'duration': duration
        })

        flash('Workout logged successfully', 'success')

    user_workout_history = user_workouts.get(username, [])

    return render_template('workouts.html', username=username, workouts=user_workout_history)

@app.route('/history')
def history():
    if 'username' not in session:
        return redirect(url_for('home'))

    username = session['username']

    user_workout_history = user_workouts.get(username, [])
    
    return render_template('history.html', username=username, workouts=user_workout_history)

if __name__ == '__main__':
    app.run(debug=True)
