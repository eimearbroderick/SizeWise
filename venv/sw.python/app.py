from flask import Flask, g, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL #imports the mysql package for use
import MySQLdb.cursors 
import re 



app = Flask(__name__)
app.secret_key = 'super secret key'

#Flask DB Configuration
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
        

        #attempts to log
        #sql = 'INSERT INTO reviews VALUES (% s, % s, % s  WHERE id =% s )'
        #values = (store, rating, review, (session['id'] )
        #cursor.execute('INSERT INTO reviews VALUES (% s, % s, % s  WHERE id =% s', (store, rating, review, (session['id'], ) )) 
        
        
        #cursor.execute('INSERT INTO reviews VALUES ( ,% s,% s,% s,% s)', (store, size, rating, review,)) 

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
        #cursor.commit()
        
        #add_review = ("INSERT INTO reviews "
         #      "(store, size, rating, review) "
          #     "VALUES (% s, % s, % s, % s)")
        #cursor.execute(add_review)
        #reviewID = cursor.lastrowid
        
        #cursor.execute(sql, values)
        #commits new changes to the mySQL database
        
        #tried using proper query paramaterisation 
        #cursor.execute(""")
        #UPDATE login.reviews
        #SET store = %s
         #   rating=%s
          #  review=%s
        #WHERE id = (session['id'])"""


        mysql.connection.commit() 
        msg = 'Your SizeWise review has been logged!'
    return render_template('index.html', msg = msg)

  

 #display user review on their profile
@app.route('/display_user_review')
def display_user_review():
   cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
   cursor.execute('SELECT * FROM reviews where id = % s', (session['id'], ))
   showreviews = cursor.fetchall()
   return render_template('profile.html', showreviews = showreviews)
    


#calls the profile page
@app.route('/profile')
def profile():
    if 'loggedin' in session: 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM accounts WHERE id = % s', (session['id'], )) 
        account = cursor.fetchone()     
        return render_template("profile.html", account = account) 
    return redirect(url_for('login'))
   

 #Registers a new user 
@app.route('/register', methods =['GET', 'POST']) 
def register(): 
    #ensures that all required fields are filled
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'first_name' in request.form and 'last_name' in request.form and 'age' in request.form and 'height' in request.form and 'weight' in request.form and 'avgsize' in request.form:  
        username = request.form['username'] 
        password = request.form['password'] 
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
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s, NULL, NULL, NULL, NULL, NULL, NULL)', (username, password, email, first_name, last_name, age, height, weight, avgsize )) 
            #commits new changes to the mySQL database
            mysql.connection.commit() 
            msg = 'You have successfully registered!'
    elif request.method == 'POST': 
        msg = 'Please fill out the form !'
    return render_template('login.html', msg = msg)   

#edit an account profile
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


if __name__ == '__main__':
    #moved to top app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    #app.debug = True 
    #prevents the registration of users

    app.run()