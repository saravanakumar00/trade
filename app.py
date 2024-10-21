from flask import Flask,request,render_template,url_for,redirect
import sqlite3

app=Flask(__name__) 

conn=sqlite3.connect('users.db',check_same_thread=False)
cursor=conn.cursor()
cursor.execute('''
               CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fullname TEXT NOT NULL,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                password TEXT NOT NULL
               );

''')
@app.route('/')
def index():
     return render_template('registration.html')

@app.route('/register' ,methods=['GET','POST'])
def register_user():
    if request.method=='POST':
         
        fname=request.form.get('fullname')
        username=request.form.get('username')
        email=request.form.get('email')
        phone=request.form.get('phone-number')
        password=request.form.get('Password')
        conf_password=request.form.get('confirm-password')
        print(fname,username)
        if password != conf_password:
                return "Passwords do not match!"
        cursor.execute('''

            insert into users(fullname,username,email,phone,password) values(?,?,?,?,?)
            ''',(fname,username,email,phone,password))
        conn.commit()
        return render_template('login.html')
    return render_template('registration.html')


# Dashboard fuction 

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# login Fuction 
@app.route('/login' ,methods=['GET','POST'])
def login():
    if request.method=='POST':
        log_username=request.form['username_or_email']
        log_password=request.form['password']
        if '@'in log_username:
            cursor.execute('select * from users where email=? and password=?',(log_username,log_password))
        else :
            cursor.execute('select * from users where username=? and password=?',(log_username,log_password))
        user=cursor.fetchone()
        if user:
            return redirect(url_for('dashboard')) # redirect to dashboard function
        else:
            return "Invalid username/email or password. Please try again."
        
    return render_template('login.html')

if __name__=='__main__':
    app.run(debug=True)

























