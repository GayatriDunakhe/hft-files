from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from datetime import datetime, timedelta

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

@app.route('/')
def activity():
    # Calculate the start and end timestamps for the current day
    today = datetime.now()
    start_of_day = today.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = today.replace(hour=23, minute=59, second=59, microsecond=999999)

    # Fetch activities for the current day
    cursor.execute("SELECT activity, calories_burned, distance_covered FROM activities1 WHERE timestamp BETWEEN %s AND %s", (start_of_day, end_of_day))
    activities = cursor.fetchall()
    print(f"Activities: {activities}")
    return render_template('activity.html', activities=activities)

@app.route('/form', methods=['GET','POST'])
def add_activity():
    if request.method == 'POST':
        selected_activity = request.form['selected_activity']
        duration = int(request.form['duration'])
        intensity = int(request.form['intensity'])
        weight = float(request.form['weight'])

        # Define the MET (Metabolic Equivalent of Task) values for activities
        met_values = {
            'Running': 9.8,
            'Swimming': 7.0,
            'Jogging': 7.0,
            'Walking': 3.9,
            'Cycling': 8.0,
            'Yoga': 2.5,
            'Weightlifting': 3.0
            # add more activities and met values
        }

        if selected_activity in met_values:
            met = met_values[selected_activity]
            duration_in_hours = duration / 60.0
            calories_burned = met * weight * duration_in_hours * intensity

            # Calculate distance for running, jogging, and walking
            if selected_activity in ['Running', 'Jogging', 'Walking','Cycling']:
                distance_covered = calories_burned / (weight * 1.036)
            else:
                distance_covered = 0  # For other activities

            # Store the data in the database with the current timestamp
            insert_query = "INSERT INTO activities1 (activity, duration, intensity, weight, calories_burned, distance_covered, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            timestamp = datetime.now()
            data = (selected_activity, duration, intensity, weight, calories_burned, distance_covered, timestamp)

            cursor.execute(insert_query, data)
            db.commit()

            return redirect(url_for('activity'))
        else:
            return "Invalid activity selected"
    else:
        # Render the form for a GET request
        return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)