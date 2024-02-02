from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

con= pymysql.connect(
    database = "dbrown_socialmedia",
    user="dbrown",
    password="228370052",
    host="10.100.33.60",
    cursorclass= pymysql.cursors.DictCursor
) 

@app.route('/')
def Index():
    return render_template("home.html.jinja")

@app.route("/register", methods =["POST", "GET"])
def register():
    if request.method == 'POST':
        # Do this for every input in your form
        username = request.form["username"]
        display_name = request.form["display_name"]
        password= request.form["password"]
        banned = request.form["banned"]
        email= request.form["email"]
        bio= request.form["bio"]
        photo= request.form["photo"]


        cursor = con.cursor()
        cursor.execute(f"INSERT INTO `users` (__PUT_COLUMNS_HERE__) VALUES ('{username}', '{display_name}', '{password}', '{banned}', '{email}', '{bio}', '{photo}',)")
        cursor.close()
        con.commit()







      
    return render_template("register.html.jinja")


      

