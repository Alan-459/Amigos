from flask import *
import pyrebase
import speech_recognition
import cv2
recognizer=speech_recognition.Recognizer()

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

camera=cv2.VideoCapture(0)
def generate_frames():
    while True:
            
        ## read the camera frame
        success,frame=camera.read()
        if not success:
            break
        else:
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')


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

ar=['']
@app.route('/re',methods=['GET','POST'])
def re():
    while True:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.1)
            audio=recognizer.listen(mic)
            try:
                text=recognizer.recognize_google(audio)
                #text=text.lower()
                ar.append(text)
                print(text)
                print(ar)

            except:
                print("Internet issue")   


@app.route('/sn',methods=['GET','POST'])
def sn():
    str=''
    for i in ar:
        str=str+' '+i
    return render_template('new3.html',t=str)


if __name__ == '__main__':
    app.run(debug=True)
