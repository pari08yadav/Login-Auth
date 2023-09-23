from flask import Flask, render_template, url_for, request, session, redirect, flash
import mysql.connector
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo

connection = mysql.connector.connect(
  host="localhost",
  user="parishram",
  password="yadav08",
  database = "chat_app"
)
cursor = connection.cursor()

# value = cursor.execute('INSERT INTO user (username, password) VALUES ("Rohit Srivastava", "rahit008")')
# connection.commit()
# print(type(value))
# print(value)
# print("Hello world")

app = Flask(__name__)
app.config['SECRET_KEY'] = "Your_secret_string"

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=35)])
    confirm_password = PasswordField("Confirm_Password", validators=[DataRequired(), Length(min=6, max=35), EqualTo('password')])
    submit = SubmitField("Sign-Up")
    
    
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=35)])
    confirm_password = PasswordField("Confirm_Password", validators=[DataRequired(), Length(min=6, max=35), EqualTo('password')])
    submit = SubmitField("Login")

@app.route('/home')
def home():
    if 'username' in session:
        session['loggedin'] = True
        username = session['username']
        msg = "You are loggedin Successfully!"
        return render_template('home.html',username=username, message=msg)
    else:
        return redirect(url_for('login'))


@app.route('/')
def index():
    loginform = LoginForm()
    return render_template("index.html", form = loginform)


@app.route('/login', methods=['GET', 'POST'])
def login():   
    loginform = LoginForm()
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        connection = mysql.connector.connect(
        host="localhost",
        user="parishram",
        password="yadav08",
        database = "chat_app"
        )
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM user WHERE username=%s AND password=%s', (username,password))
        record = cursor.fetchone()
        connection.commit()
        
        if record:
            session['loggedin'] = True
            session['username'] = record[1]
            return redirect(url_for('home'))
        else:
            message = "Incorrect username/password. Try again!"
    return render_template('login.html', form=loginform, message=message)


@app.route('/register', methods=['GET', 'POST'])
def register():
    registerform = RegisterForm()
    message = ''
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        connection = mysql.connector.connect(
        host="localhost",
        user="parishram",
        password="yadav08",
        database = "chat_app"
        )
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM user WHERE username=%s AND password=%s', (username,password))
        record = cursor.fetchone()
        connection.commit()
        
        if record:
            flash("Account already exist !")
            return redirect(url_for('login'))
        else:
            cursor.execute('INSERT INTO user VALUES (%s, %s)', (username, password))
            connection.commit()
            message = "Your Registration is done Successfully! "
            return render_template("home.html", message=message)
            
    
    elif request.method == 'POST':
        message = 'Please fill the form !'
    return render_template("register.html", form=registerform, message = message)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return render_template('logout.html')
     
if __name__ == '__main__': 
    app.run(debug=True)