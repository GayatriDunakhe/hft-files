from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/notifications')
def notifications():
    return render_template('notifications.html')

app.run(debug=True)