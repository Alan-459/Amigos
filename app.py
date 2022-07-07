from flask import *
import pyrebase
config = {
    "apiKey": "AIzaSyAEHIF53_-kWZ-z6gPw2l1CWoWDdrhsvc0",
    "authDomain": "diary-aab7f.firebaseapp.com",
    "databaseURL": "https://diary-aab7f-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "diary-aab7f",
    "storageBucket": "diary-aab7f.appspot.com",
    "messagingSenderId": "527831026284",
    "appId": "1:527831026284:web:008e0e1bbb0c2b6fe1a649"
}
firebase = pyrebase.initialize_app(config)

db = firebase.database()
storage = firebase.storage()
auth = firebase.auth()

app = Flask(__name__)


@app.route('/')
def mainpage():
    return render_template('mainhome.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        emai = request.form["email"]
        pas = request.form["pass"]
        con = request.form["conpass"]
        if con == pas:
            auth.create_user_with_email_and_password(emai, pas)
            return redirect(url_for('mainpage'))
        return render_template('signup.html')
    return render_template('signup.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        emai = request.form["email"]
        pas = request.form["pass"]
        auth.sign_in_with_email_and_password(emai, pas)
        # flash('You were successfully logged in')
        return redirect(url_for('basic'))
    return render_template('login.html')


@app.route('/tile', methods=['GET', 'POST'])
def basic():
    todo = db.get()
    to = todo.val()
    if request.method == 'POST':
        var = request.form['show']
        if var:
            return render_template('show.html', t=to[var])

    if to:
        return render_template('index.html', t=to.values())
    return render_template('index.html')


date = {'date': '', 'text': '', 'rate': '', 'link': ''}


@app.route('/date', methods=['GET', 'POST'])
def datef():

    if request.method == 'POST':
        date1 = request.form['date']
        date['date'] = date1
        db.child(date['date']).update(date)
        return render_template('new2.html')
    return render_template('new1.html')


@app.route('/rate', methods=['GET', 'POST'])
def ratef():
    if request.method == 'POST':
        rate = int(request.form['rate'])
        date['rate'] = rate
        db.child(date['date']).update(date)
        return render_template('new3.html')
    return render_template('new2.html')


@app.route('/text', methods=['GET', 'POST'])
def textf():
    if request.method == 'POST':
        text = request.form['text']
        date['text'] = text
        db.child(date['date']).update(date)
        img = request.form['file']
        if img:
            storage.child(date['date']).put(img)
            date['link'] = storage.child(date['date']).get_url(date['date'])
            db.child(date['date']).update(date)
        return redirect(url_for('basic'))
    return render_template('new3.html')


if __name__ == '__main__':
    app.run(debug=True)
