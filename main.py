from flask import Flask, render_template, request, redirect 
import flask_login
import pymysql

app = Flask(__name__)

app.secret_key ="something_secret" #change this
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User:
    is_authenticated = True
    is_anonymous = False
    is_active = True
   
    def __init__(self,id,username): #add the rest from the users database
      self.username = username
      self.id = id
      pass
    def get_id(self):
      return str(self.id)
@login_manager.user_loader
def load_user(user_id):
    cursor = con.cursor()

    cursor.execute("SELECT* FROM `users` WHERE `id` =" + str(user_id))
    result = cursor.fetchone()
    cursor.close()
    cursor.commit()
    if result is None:
        return None
    
    return User(result["id"], result ["username"]) #add the rest from users database

       



con= pymysql.connect(
    database = "dbrown_socialmedia",
    user="dbrown",
    password="228370052",
    host="10.100.33.60",
    cursorclass= pymysql.cursors.DictCursor
) 

@app.route('/')
def Index():
    if flask_login.current_user.is_authenticated:
       return redirect('/feed')
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

@app.route('/feed',methods = [])
@flask_login.login_required
def feed():
   return flask_login.current_user


@app.route("/signin",methods = ["POST", "GET"])
def sign():
    if request.method == 'POST':
        username = request.form["username"]
        password= request.form["password"]

        cursor = con.cursor()
        
        cursor.execute(f"SELECT * FROM `users` WHERE `username` = '{username}'")
        cursor.close()
        con.commit()

        result = cursor.fetchone()

        if password == result["password "]:
            user = load_user (result['id'])
            flask_login.login_user(user)
            return redirect('/')
    
    return render_template("sign.html.jinja")

    
    





      

