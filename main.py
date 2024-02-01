from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def Index():
    return render_template("home.html.jinja")

@app.route("/register", methods =["POST", "GET"])
def register():
    return render_template("register.html.jinja")

