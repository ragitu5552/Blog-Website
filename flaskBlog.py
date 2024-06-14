# save this as app.py
from flask import Flask

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return "Home Page"

@app.route("/about")
def about():
    return "About Page"

@app.route("/contact")
def contact():
    return "<h1> Contact Information </h1>"

if __name__ == "__main__":
    app.run(debug=True)