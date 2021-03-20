from flask import Flask, g, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL #imports the mysql package for use
from tabulate import tabulate
import MySQLdb.cursors 
import re 
import pandas as pd


app = Flask(__name__)

#secret key assigns session cookies for protection against cookie data tampering
app.secret_key = 'super secret key'

#Flask DB Configuration
#DB Connection code taken from https://www.codementor.io/@adityamalviya/python-flask-mysql-connection-rxblpje73 by Aditya Malviya

#connecting to heroku
DB_CONN= "mysql+pymysql://wxyyl46fbev0qqau:c27lzs5zwbfzj29x@lmc8ixkebgaq22lo.chr7pe7iynqr.eu-west-1.rds.amazonaws.com:3306/p72ii57nh03mrmhe"

#local db
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

#calls Login page
@app.route('/loginpage')
def loginpage():
    return render_template("venv/sw.python/templates/login.html")

#calls Weekday page
@app.route('/weekday')
def weekday():
    return render_template("home.html")

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
    if request.method == 'POST' and 'store' in request.form and 'size' in request.form and 'rating' in request.form and 'fit' in request.form and 'product' in request.form and 'review' in request.form:  
        store = request.form['store']
        size = request.form['size']
        rating = request.form['rating']
        fit = request.form['fit']
        product = request.form['product']  
        review = request.form['review']
       

        #activites mysql cursor    
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        #code extract taken from https://realpython.com/python-mysql/ by Chaitanya Baweja 
        insert_reviews_query = """
        INSERT INTO reviews (id, store, size, rating, fit, product, review)
        VALUES
        ('% s','% s','% s','% s', '% s', '% s', '% s')
         """ % (
        session['id'],
        store,
        size,
        rating,
        fit,
        product,
        review
        )


        cursor.execute(insert_reviews_query)
        mysql.connection.commit() 
        msg = 'Your SizeWise review has been logged!'
    #code from Philip Martin at https://stackoverflow.com/questions/36872257/how-to-show-confirmation-modal-in-flask-app-after-form-submission
    submission_successful = True 
    return render_template('reviewWeekday.html', msg=msg, submission_successful=submission_successful )
 

#fit column generator
@app.route('/fitcol', methods =['GET', 'POST']) 
def fitcol():
     #activites mysql cursor    
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        #code extract taken from https://realpython.com/python-mysql/ by Chaitanya Baweja 
       # insert_fit_query = """
        #SET SQL_MODE = '';
        
        #INSERT INTO reviews(category)
        #VALUES
        #(SELECT
        #CASE 
        #WHEN fit >= 4 
         #    then 'Big'
        #WHEN fit <= 2 
         #    then 'Small' 
        #ELSE 'Regular'     
        #END as category)
        #"""
        insert_fit_query = """
            UPDATE reviews SET category =
             CASE
                    WHEN ( fit = 1 ) THEN 'Small'
                    WHEN ( fit = 2 ) THEN 'Small'
                    WHEN ( fit = 3 ) THEN 'Regular'
                    WHEN ( fit = 4 ) THEN 'Big'
                    WHEN ( fit = 5 ) THEN 'Big'
                    else 'NULL'
                    END 
                    WHERE fit in (1,2,3,4,5)
        """
        cursor.execute(insert_fit_query)
        mysql.connection.commit() 

        return render_template('reviewWeekday.html' )

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
        #changing SQL output from JSON to a dataframe
        review = pd.DataFrame.from_records(review)
    #return redirect(url_for("profile", review=['review'])) 
        return render_template("profile.html", account=account, review=review)

#calculates the sizewise average score
#code extract from @saksham_kapoor at https://www.geeksforgeeks.org/how-to-compute-the-average-of-a-column-of-a-mysql-table-using-python/

@app.route('/swscore' , methods =['GET', 'POST'])
def swscore():  
    #activites mysql cursor    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)      
    #executing the query 
    avgrating= "Select (AVG(rating),0) AS avgrating from reviews;"
    cursor.execute(avgrating) 
   # avgrating = cursor.fetchall()
    #avgrating = pd.DataFrame.from_records(avgrating) 
    rows = cursor.fetchall() 
    for i in rows: 
        avgrating = str(i[0])
        displayavg = pd.DataFrame.from_records(avgrating) 
        return render_template('home.html',displayavg=displayavg, rows=rows, avgrating=avgrating)  

#saves a discount code to the database
# code inspired by user registration code by @venniladeenan at https://www.geeksforgeeks.org/login-and-registration-project-using-flask-and-mysql/
@app.route('/add_dcode' , methods =['GET', 'POST']) 
def add_dcode():
    msg= '' 
    if request.method == 'POST' and 'dcode' in request.form and 'date' in request.form and 'amount' in request.form and 'active' in request.form:  
        dcode = request.form['dcode']
        date = request.form['date']
        amount = request.form['amount']  
        active = request.form['active']
       

        #activites mysql cursor    
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        #code extract taken from https://realpython.com/python-mysql/ by Chaitanya Baweja 
        insert_dcode_query = """
        INSERT INTO discounts (dcode, date, amount, storeID, active)
        VALUES
        ('% s','% s','% s','% s','% s')
         """ % (
        dcode,
        date,
        amount,
        session['id'],
        active
        )

        
        cursor.execute(insert_dcode_query)
        mysql.connection.commit() 
        msg = 'Your SizeWise discount code has been logged!'
        cursor.execute('SELECT * FROM discounts WHERE storeID = % s', (session['id'], )) 
        
        discounts = cursor.fetchall() #reviews from database
        discounts= pd.DataFrame.from_records(discounts) 
    
    return render_template('b2bhome.html', discounts=discounts, msg = msg)     

#displays a company's discount codes
@app.route('/showcodes')
def showcodes():
    if 'loggedin' in session: 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM discounts WHERE storeID = % s', (session['id'], )) 
        discounts = cursor.fetchall()     
        discounts= pd.DataFrame.from_records(discounts)
        return render_template("b2bhome.html", discounts = discounts) 
    return redirect(url_for('login'))

   

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
        session['load'] = 0
        #SQL query to fetch the user from the db
        cursor.execute('SELECT * FROM store WHERE store = % s AND password = % s', (store, password, )) 
        store = cursor.fetchone() 

        cursor.execute('SELECT * FROM discounts WHERE storeID = % s', (session.get('id'), )) 
        discounts = cursor.fetchall() #reviews from database 
        discounts= pd.DataFrame.from_records(discounts)
        
        if store: 
            session['loggedin'] = True
            session['id'] = store['storeID'] 
            session['username'] = store['store'] 
            msg = 'Logged in successfully !'
            return render_template('b2bhome.html', discounts=discounts, msg = msg) 
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
        cursor.execute('SELECT * FROM discounts WHERE storeID = % s', (session['id'], )) 
        discounts = cursor.fetchall()     
        print(review)
        #changing SQL output from JSON to a dataframe
        review = pd.DataFrame.from_records(review)
        discounts=pd.DataFrame.from_records(discounts)
        return render_template("b2bhome.html", review=review, discounts=discounts)   
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