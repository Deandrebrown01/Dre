from flask import Flask, render_template

app = Flask(__name__)

@app.route('/main')
def Index():
    return render_template("home.html.jinja")