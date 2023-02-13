import os

from dotenv import load_dotenv
from firebase import Firebase
from flask import Flask, render_template, request, session, redirect, flash

app = Flask(__name__)
app.secret_key = os.getenv('secret_key')

CONFIG = {
    "apiKey": os.getenv('api'),
    "authDomain": "agriversity-dc858.firebaseapp.com",
    "projectId": "agriversity-dc858",
    "storageBucket": "agriversity-dc858.appspot.com",
    "messagingSenderId": "1059714227664",
    "appId": "1:1059714227664:web:52897932e204aac19e6dd5",
    "measurementId": "G-HN1CDE60QT",
    "databaseURL": "https://agriversity-dc858-default-rtdb.firebaseio.com/"
}

firebase = Firebase(CONFIG)
db = firebase.database()


def config():
    load_dotenv()


@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/about.html")
def about():
    return render_template("about.html")


@app.route("/index.html")
def index():
    return render_template("index.html")


@app.route("/team.html")
def team():
    return render_template("team.html")


@app.route("/coming-soon.html", methods=['GET', 'POST'])
def coming_soon():
    if request.method == 'POST':
        email = request.form.get('email')
        data = {
            'email': email
        }
        db.child('emailsubmissions').push(data)
        flash("Success")
        return redirect('coming-soon.html')
    return render_template('coming-soon.html')


@app.route("/feature.html")
def feature():
    return render_template("feature.html")


@app.route("/contact.html", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')
        company = request.form.get('company')
        message = request.form.get('message')

        data = {
            "username": username,
            "email": email,
            "phone": phone,
            "company": company,
            "message": message
        }
        db.child("All Submissions").push(data)

        # returning Flash message onto the screen
        flash("Success")
        return render_template("contact.html")
    return render_template("contact.html")


@app.route('/admin')
def admin():
    if 'user' in session:
        flash('Success')
        all_entries = db.child('All Submissions').get()
        return render_template('admin.html', all_entries=all_entries)
    return redirect('/login')


@app.route('/responses/<string:pushkey>')
def responses(pushkey):
    data = dict(db.child('All Submissions').child(pushkey).get().val())
    return render_template('responses.html', data=data, pushkey=pushkey)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        session.pop('user', None)
        print(request.form.get('email'), request.form.get('password'))
        if request.form.get('email') == os.getenv('username') and request.form.get('password') == os.getenv('password'):
            session['user'] = request.form.get('email')
            return redirect('/admin')
        else:
            flash('failure')
    if 'user' in session:
        redirect('/admin')
    return render_template('/login.html')


@app.route('/logout')
def logout():
    flash('logout')
    session.pop('user', None)
    return redirect('/login')


@app.route('/email')
def get_emails():
    if 'user' in session:
        all_entries = db.child('emailsubmissions').get()
        return render_template('adminemails.html', all_entries=all_entries)
    return redirect('/login')


if __name__ == '__main__':
    config()
    app.run()
