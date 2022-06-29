
from flask import Flask,render_template,url_for
 
app = Flask(__name__)

@app.route('/')
@app.route('/home')
def Home():
    return render_template("mainhome.html")
@app.route('/signup')
def register():
    return render_template("signup.html")

@app.route('/signin')
def signin():
    return render_template("login.html")

@app.route('/main')
def main():
    return render_template("index.html")
if __name__ =="__main__":
    app.run(debug = True)
