from flask import Flask, render_template, request, redirect , g
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
    cursor = get_db().cursor()


    cursor.execute("SELECT* FROM `users` WHERE `id` =" + str(user_id))
    result = cursor.fetchone()
    cursor.close()
    get_db().commit()
    if result is None:
        return None
    
    return User(result["id"], result ["username"]) #add the rest from users database

       



def connect_db():
    return pymysql.connect(
        host="10.100.33.60",
        user="dbrown",
        password="228370052",
        database="De'Andre",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

def get_db():
    '''Opens a new database connection per request.'''        
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db    

@app.teardown_appcontext
def close_db(error):
    '''Closes the database connection at the end of request.'''    
    if hasattr (g, 'db'):
        g.db.close() 

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


        cursor = get_db().cursor()
        cursor.execute(f"INSERT INTO `users` (__PUT_COLUMNS_HERE__) VALUES ('{username}', '{display_name}', '{password}', '{banned}', '{email}', '{bio}', '{photo}',)")
        cursor.close()
        get_db().commit()
        return redirect ('/')

    return render_template("register.html.jinja")

@app.route('/feed')
@flask_login.login_required
def feed():
   return flask_login.current_user


@app.route("/signin",methods = ["POST", "GET"])
def sign():
    if request.method == 'POST':
        username = request.form["username"]
        password= request.form["password"]

        cursor = get_db().cursor()
        
        cursor.execute(f"SELECT * FROM `users` WHERE `username` = '{username}'")
        cursor.close()
        get_db().commit()

        result = cursor.fetchone()

        if password == result["password "]:
            user = load_user (result['id'])
            flask_login.login_user(user)
            return redirect('/')
    
    return render_template("sign.html.jinja")

    
@app.route('/post', methods= ['POST'])
@flask_login.login_required
def create_post():
    description = request.form['description']
    user_id = flask_login.current_user.id

    cursor = get_db().cursor()

    cursor.execute("INSERT INTO `posts` (`description`, `user_id`)")





      

