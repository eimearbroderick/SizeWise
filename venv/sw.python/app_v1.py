from flask import Flask, g, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL #imports the mysql package for use
import MySQLdb.cursors 
import re 

#creating an instance of the Flask class
app = Flask(__name__)


#Flask DB Configuration
#DB Connection code taken from https://www.codementor.io/@adityamalviya/python-flask-mysql-connection-rxblpje73 by Aditya Malviya

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mypass'
app.config['MYSQL_DB'] = 'login'

#Creates an instance of the application to provide us with DB Access
mysql = MySQL(app)

#calls the homepage
@app.route('/home')
def home():
    return render_template("home.html")

#calls Weekday page
@app.route('/weekday')
def weekday():
    return render_template("index.html")

#Registers a new user 
#code from @venniladeenan at https://www.geeksforgeeks.org/login-and-registration-project-using-flask-and-mysql/

@app.route('/register', methods =['GET', 'POST']) 
def register(): 
    #ensures that all required fields are filled
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:  
        username = request.form['username'] 
        password = request.form['password'] 
        email = request.form['email'] 

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, )) 
        account = cursor.fetchone() 
        if account: 
            msg = 'Account already exists !'
            #email validation
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email): 
            msg = 'Invalid email address !'
            #username validation
        elif not re.match(r'[A-Za-z0-9]+', username): 
            msg = 'Invalid username!'
            #empty required fields
        elif not username or not password or not email: 
            msg = 'Please fill out the required fields'
        else: 
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email)) 
            #commits new changes to the mySQL database
            mysql.connection.commit() 
            msg = 'You have successfully registered!'
    elif request.method == 'POST': 
        msg = 'Please fill out the form !'
    return render_template('login.html', msg = msg)   


#Code to verify a login
#Also taken from @venniladeenan at https://www.geeksforgeeks.org/login-and-registration-project-using-flask-and-mysql/
@app.route('/') 
@app.route('/login', methods =['GET', 'POST']) 
def login(): 
    msg = '' 
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form: 
        username = request.form['username'] 
        password = request.form['password'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        #SQL query to fetch the user from the db
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, )) 
        account = cursor.fetchone() 
        if account: 
            session['loggedin'] = True
            session['id'] = account['id'] 
            session['username'] = account['username'] 
            msg = 'Logged in successfully !'
            return render_template('home.html', msg = msg) 
        else: 
            msg = 'Incorrect username / password !'
            return render_template('login.html', msg = msg) 

#Logs out a user if they choose to
#Also taken from @venniladeenan at https://www.geeksforgeeks.org/login-and-registration-project-using-flask-and-mysql/
@app.route('/logout') 
def logout(): 
    session.pop('loggedin', None) 
    session.pop('id', None) 
    session.pop('username', None) 
    return redirect(url_for('login')) 




#environment test
#@app.route('/', methods=['GET', 'POST'])
#def index():
#    if request.method == "POST":
#        details = request.form
#        firstName = details['fname'] #fetches firstname from the html form
 #       lastName = details['lname'] #fetches lastname from the html form
  #      #establishment of connection   
   #     cur = mysql.connection.cursor()
    #    #execution of db query
     #   cur.execute("INSERT INTO MyUsers(firstName, lastName) VALUES (%s, %s)", (firstName, lastName))
      #  mysql.connection.commit() #commits any changes to the database
       # cur.close()
        #return 'You have successfully been added to the database!'
    #return render_template('index.html')


#Python app starter code from https://www.codementor.io/@adityamalviya/python-flask-mysql-connection-rxblpje73 by Aditya Malviya

if __name__ == '__main__':
  #secret key assigns session cookies for protection against cookie data tampering
   app.secret_key = 'super secret key' 
app.config['SESSION_TYPE'] = 'filesystem'

    #app.debug = True 
    #stopped because prevents the registration of users

app.run()