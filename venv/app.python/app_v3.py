from flask import Flask, g, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL #imports the mysql package for use
from tabulate import tabulate
import MySQLdb.cursors 
import re 



app = Flask(__name__)
#secret key assigns session cookies for protection against cookie data tampering
app.secret_key = 'super secret key'

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

#calls Nike page
@app.route('/nike')
def nike():
    return render_template("nike.html")

#calls Zara page
@app.route('/zara')
def zara():
    return render_template("zara.html")    
    
#saves a user review to the database
#top code inspired by user registration code by @venniladeenan at https://www.geeksforgeeks.org/login-and-registration-project-using-flask-and-mysql/
@app.route('/review' , methods =['GET', 'POST']) 
def review():
    msg= '' 
    if request.method == 'POST' and 'store' in request.form and 'size' in request.form and 'rating' in request.form and 'review' in request.form:  
        store = request.form['store']
        size = request.form['size']
        rating = request.form['rating']  
        review = request.form['review']
       

        #activites mysql cursor    
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        #code extract taken from https://realpython.com/python-mysql/ by Chaitanya Baweja 
        insert_reviews_query = """
        INSERT INTO reviews (id, store, size, rating, review)
        VALUES
        ('% s','% s','% s','% s','% s')
         """ % (
        session['id'],
        store,
        size,
        rating,
        review,
        )
        
        cursor.execute(insert_reviews_query)
        mysql.connection.commit() 
        msg = 'Your SizeWise review has been logged!'
    
    return render_template('index.html', msg = msg)
 
#calls the profile page
#code from @venniladeenan at https://www.geeksforgeeks.org/profile-application-using-python-flask-and-mysql/
@app.route('/profile')
def profile():
    if 'loggedin' in session: 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM accounts WHERE id = % s', (session['id'], )) 
        account = cursor.fetchone()     
        return render_template("profile.html", account = account) 
    return redirect(url_for('login'))

@app.route('/userreviews')

#display user review on their profile
#code extract inspired by user @broxamson at https://www.reddit.com/r/flask/comments/evr3jk/display_mysql_table_with_html/ combined with the profile code used in iteration 2
def userreviews(): 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM accounts WHERE id = % s', (session['id'], )) 
        account = cursor.fetchone() 
        cursor.execute('SELECT * FROM reviews WHERE id = % s', (session['id'], )) 
        review = cursor.fetchall() #reviews from database 
        print(tabulate(review, headers="keys", tablefmt="github"))
    #return redirect(url_for("profile", review=['review'])) 
        return render_template("profile.html", account=account, review=review)


          
   

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
            cursor.execute
        
        #altered for v3, code taken from user review db code referenced above by Chaitanya Baweja 
            insert_user_query = """
        INSERT INTO accounts (username, password, email)
        VALUES
        ('% s','% s','% s')
         """ % (
        username,
        password,
        email
        )
        
        cursor.execute(insert_user_query)
        #commits new changes to the mySQL database
        mysql.connection.commit() 
        msg = 'You have successfully registered!'
    elif request.method == 'POST': 
        msg = 'Please fill out the form !'
    return render_template('login.html', msg = msg)   

#edit an account profile
#code from @venniladeenan at https://www.geeksforgeeks.org/profile-application-using-python-flask-and-mysql/

@app.route('/edit', methods =['GET', 'POST']) 
def edit():
    msg= ''
    if 'loggedin' in session: 
        if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'first_name' in request.form and 'last_name' in request.form and 'age' in request.form and 'height' in request.form and 'weight' in request.form and 'avgsize' in request.form: 
            username = request.form['username'] 
            email = request.form['email'] 
            first_name = request.form['first_name']   
            last_name = request.form['last_name'] 
            age = request.form['age'] 
            height = request.form['height'] 
            weight = request.form['weight']     
            avgsize = request.form['avgsize']  
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
            cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, )) 
            account = cursor.fetchone() 
            #Form controls 
            if account: 
                msg = 'Account already exists !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email): 
                msg = 'Invalid email address !'
            elif not re.match(r'[A-Za-z0-9]+', username): 
                msg = 'name must contain only characters and numbers !'
            else: 
                cursor.execute('UPDATE accounts SET  username =% s, email =% s, first_name =% s, last_name =% s, age =% s, height =% s, weight =% s, avgsize =% s WHERE id =% s', (username, email, first_name, last_name, age, height, weight, avgsize, (session['id'], ), )) 
                #coommits database changes to MySQL
                mysql.connection.commit() 
                msg = 'You have successfully updated your account details!'
        elif request.method == 'POST': 
            msg = 'Please fill out the form !'
        return render_template("edit.html", msg = msg) 
    return redirect(url_for('login'))  
    

#Code to verify a login
#code from code from @venniladeenan at https://www.geeksforgeeks.org/login-and-registration-project-using-flask-and-mysql/

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


#calls b2b login page
@app.route('/b2blogin')
def b2blogin():
    return render_template("b2blogin.html")


#Code to verify a store login, taken from user login code referenced above by @venniladeenan
@app.route('/') 
@app.route('/storelogin', methods =['GET', 'POST']) 
def storelogin(): 
    msg = '' 
    if request.method == 'POST' and 'store' in request.form and 'password' in request.form: 
        store = request.form['store'] 
        password = request.form['password'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        #SQL query to fetch the user from the db
        cursor.execute('SELECT * FROM store WHERE store = % s AND password = % s', (store, password, )) 
        store = cursor.fetchone() 
        if store: 
            session['loggedin'] = True
            session['id'] = store['storeID'] 
            session['username'] = store['store'] 
            msg = 'Logged in successfully !'
            return render_template('b2bhome.html', msg = msg) 
        else: 
            msg = 'Unrecognised store, please try again'
    return render_template('b2blogin.html', msg = msg) 

#calls b2b login page
@app.route('/b2bhome')
def b2bhome():
    return render_template("b2bhome.html")

#Shows a stores review database
#code extract inspired by user @broxamson at https://www.reddit.com/r/flask/comments/evr3jk/display_mysql_table_with_html/ combined with the profile code used in iteration 2
@app.route('/reviewb2b')
def reviewb2b(): 
    if 'loggedin' in session: 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM reviews WHERE store = % s', (session['username'], )) 
        review = cursor.fetchall() #reviews from database 
        print(review)
        return render_template("b2bhome.html", review=review)   
    return redirect(url_for('b2blogin'))

#Logs out a user if they choose to
#code from @venniladeenan at https://www.geeksforgeeks.org/login-and-registration-project-using-flask-and-mysql/
@app.route('/logout') 
def logout(): 
    session.pop('loggedin', None) 
    session.pop('id', None) 
    session.pop('username', None) 
    return redirect(url_for('login')) 



#Python app starter code from https://www.codementor.io/@adityamalviya/python-flask-mysql-connection-rxblpje73 by Aditya Malviya
if __name__ == '__main__':
  
    app.config['SESSION_TYPE'] = 'filesystem'

    #app.debug = True 
    #prevents the registration of users

    app.run()