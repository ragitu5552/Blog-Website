# save this as app.py
from flask import Flask, render_template, url_for

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)