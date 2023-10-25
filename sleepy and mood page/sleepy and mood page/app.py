from flask import Flask, render_template, request, jsonify
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate_duration', methods=['POST'])
def calculate_duration():
    data = request.get_json()
    mood = data['mood']
    sleepiness = data['sleepiness']

    duration = {
        'moodDuration': calculate_duration(mood),
        'sleepinessDuration': calculate_duration(sleepiness)
    }

    return jsonify(duration)

def calculate_duration(selected_value):
    # This function should calculate the duration based on timestamps.
    # For simplicity, this example returns a constant value (10 seconds).
    return 10

if __name__ == '__main__':
    app.run(debug=True)
