from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import csv
from flask import make_response

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT NOT NULL,
            rating INTEGER NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


@app.route('/')
def index():
    return render_template('index.html', title="Feedback Form")

@app.route('/submit', methods=['POST'])
def submit_feedback():
    name = request.form.get('name')
    email = request.form.get('email')
    rating = request.form.get('rating')
    message = request.form.get('message')

    if not email or not rating or not message:
        return "Please fill out all required fields.", 400

    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute("INSERT INTO feedback (name, email, rating, message) VALUES (?, ?, ?, ?)",
              (name, email, int(rating), message))
    conn.commit()
    conn.close()

    return redirect(url_for('thank_you'))

@app.route('/thankyou')
def thank_you():
    return "<h2>Thank you for your feedback!</h2><p><a href='/'>Go back</a></p>"

@app.route('/export')
def export_csv():
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute("SELECT * FROM feedback")
    feedbacks = c.fetchall()
    conn.close()

    # Prepare CSV response
    si = []
    headers = ['ID', 'Name', 'Email', 'Rating', 'Message']
    si.append(headers)
    si.extend(feedbacks)

    response = make_response()
    writer = csv.writer(response.stream)
    for row in si:
        writer.writerow(row)

    response.headers['Content-Disposition'] = 'attachment; filename=feedback.csv'
    response.headers['Content-Type'] = 'text/csv'
    return response

@app.route('/admin')
def admin_dashboard():
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute("SELECT * FROM feedback")
    feedbacks = c.fetchall()
    conn.close()

    total = len(feedbacks)
    avg_rating = round(sum(row[3] for row in feedbacks) / total, 2) if total > 0 else 0

    return render_template('admin.html', feedbacks=feedbacks, total=total, avg_rating=avg_rating)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
