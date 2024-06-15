# save this as app.py
from flask import Flask, render_template, url_for
from forms import RegistrationForm, loginForm

app = Flask(__name__)
app.config['SECRET_KEY']='6fcb6719bc5ecf0a13deea4042a593'

dummy = [
    {
        'author': 'TukTuk',
        'title': 'TukTuk Blog',
        'content': 'First ever blog of TukTuk',
        'posted_date': '15 june, 2024'
    },
    {
        'author': 'Ravikesh Kumar',
        'title': 'Food Blog post',
        'content': 'First ever food blog by Ravikesh',
        'posted_date': '15 june, 2024'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', dummy=dummy)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template('register.html', form=form)

@app.route("/login")
def login():
    form = loginForm()
    return render_template('login.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)