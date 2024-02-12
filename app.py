from flask import Flask, render_template, url_for, request, session, redirect, flash, jsonify
import mysql.connector 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo
import re
import jwt
import datetime
import random


app = Flask(__name__)
app.config['SECRET_KEY'] = "HELLOWORLD"

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=35)])
    confirm_password = PasswordField("Confirm_Password", validators=[DataRequired(), Length(min=6, max=35), EqualTo('password')])
    user_id = StringField('User Id', validators=[DataRequired(), Length(min=6, max=6, message='user id should be of 6 digit')])
    submit = SubmitField("Sign-Up")
    
    
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=35)])
    submit = SubmitField("Login")
    
    
def db_connection():
    try:
        connection = mysql.connector.connect(
        host="localhost",
        user="parishram",
        password="yadav08",
        database = "chat_app"
        )
        # cursor = connection.cursor()
        return connection.cursor()
    except Exception as e:
        print("DB Connction Errror:" + str(e))
        return False


@app.route('/name_list',methods=['GET','POST'])
def name_list():
    args = request.args
    
    print(request)
    print(args["name"])
    
    json_ = [{"name":"Ajay","education":"Graduate"},
             {"name":"Vijay","education":"Master"},
             {"name":"Dinesh","education":"Master"},
             {"name":"Rajesh","education":"Master"}
             ]
    
    return jsonify(json_)


@app.route('/home')
def home():
    if 'username' in session:
        # print(type(sesssion))
        # session['loggedin'] = True
        print("session data type",type(session))
        username = session['username']
        msg = "You are loggedin Successfully!"
        return render_template('home.html',username=username, message=msg)
    else:
        return redirect(url_for('login'))


@app.route('/')
def index():
    loginform = LoginForm()
    return render_template("index.html", form = loginform)


# @app.route('/post/login', methods=['POST'])
# def login():   
#     # loginform = LoginForm()
#     response = {}
#     message = ''
#     try:
#         if request.method == 'POST':
            
#             data = request.get_json()
#             username = data["username"]
#             password = data["password"]
            
#             connection = mysql.connector.connect(
#             host="localhost",
#             user="parishram",
#             password="yadav08",
#             database = "chat_app"
            
#             )
#             cursor = connection.cursor()
#             # cursor = db_connection()
#             cursor.execute("SELECT user_id FROM users WHERE username=%s AND password=%s", (username, password))
#             # print("aaaaaaaaaaaaaaaaaaaa")
        
#             record = cursor.fetchone()
#             # connection.commit()
                
#             if record:
#                 #Generate token
#                 token = jwt.encode({'username':random.randrange(1,9999), "exp":datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'], algorithm='HS256')
                
#                 #Update Token into user table 
#                 cursor.execute("UPDATE users SET token=%s WHERE username=%s", (token, username))
#                 connection.commit()
                                                       

#                 response["status"] = 200
#                 response["data"] = {"user_id": record[0],"token":token}
#                 response['message'] = "You are loggedin successfully"
#                 return jsonify(response)
            
#             response['status'] = 400
#             response['message'] = "Invalid credential"
#             return jsonify(response)
    
#     except Exception as e:
#         response["status"] = 400
#         response["message"] = "An error occured on post login page" + str(e)
#         return jsonify(response) 
        

# @app.route('/post/register', methods=['POST'])
# def register():
    
#     message = ''
#     response = {}
#     try:
#         if request.method == 'POST':
            
#             # registerform = RegisterForm()

#             data = request.get_json()
#             username = data["username"]
#             password = data["password"]
            
#             if len(username) == 0 or len(username) < 4 or len(username) > 20:
#                 response["status"] = 400
#                 response["message"] = "Username is invalid, It must be alphanumeric, at least 4 character log and maximum 20 chars "
#                 return jsonify(response)          
           
#             if not re.findall('^[a-z0-9]+$',username):
#                 response["status"] = 400
#                 response["message"] = "Username is invalid, It must be alphanumeric"
#                 return jsonify(response)                    
            
#             cursor = db_connection()
#             cursor.execute("SELECT user_id,username FROM users WHERE username =%s",[username])
#             record = cursor.fetchone()

#             if record:
#                 response["status"] = 400
#                 response["message"] = "Username has been already used by someone, please enter another"
#                 return jsonify(response)                

#             cursor.execute('INSERT INTO users VALUES (%s, %s, %s, %s)', (None, username, password, None))
#             cursor.commit()
            
#             response["status"] = 200
#             response["message"] = "Your Registration is done Successfully! "
#             return jsonify(response)   
                     
#     except Exception as e:
#         response["status"] = 400
#         response["message"] = "An error occured: " + str(e)
#         return jsonify(response)          


# create post and insert into database
# @app.route('/post/posts', methods=['POST'])
# def create_post():
    
#     response = {}
#     try:
#         if request.method == 'POST':
#             cursor = db_connection()           
#             data = request.get_json()
#             content = data['content']
#             post = [{"content":content}]
            
#             if not post:
#                 return jsonify({"message": "Content are required"}), 400
            
#             cursor.execute("INSERT INTO posts (content) VALUES (%s)", [content])
#             cursor.commit()
#             cursor.close()
            
#             response['message'] = "Post Created in database Successfully!"
#             response['status'] = 201
#             response['post'] = post
#             return jsonify(response)           

#     except:
#         response["status"] = 400
#         response["message"] = "An error occured"
#         return jsonify(response) 
        

#get specific post by post id
# @app.route('/post/post_by_id/<int:post_id>', methods=['POST'])
# def get_post_by_id(post_id):
    
#     response = {}
#     try:
        
#         if request.method == 'POST': 
#             cursor = db_connection()
#             cursor.execute('SELECT * FROM posts WHERE id=%s', (post_id,))
#             post = cursor.fetchone()
#             cursor.close()
            
#             if not post:
#                 return jsonify({"message": "The Post You Want To Find Is Not Exist."})
            
#             post_data = {"id":post[0], "content":post[2]}
#             return jsonify(post_data)

#     except Exception as e:
#         response["status"] = 400
#         response["message"] = "An error occured" + str(e)
#         return jsonify(response)
        
    
# Update a post by Id
# @app.route('/post/update/<int:post_id>', methods=['POST'])
# def post_updation(post_id):
    
#     response = {}
#     try:
#         if request.method == 'POST':
#             cursor = db_connection()
#             data = request.get_json()
#             new_content = data['content']
            
#             if not new_content:
#                 return jsonify({"message": "Content is Required for updation."})
            
#             cursor.execute('UPDATE posts SET content = %s WHERE id = %s', (new_content, post_id))
#             cursor.commit()
#             cursor.close()

#             updated_data = {"id":post_id, "updated_content":new_content}
#             response['message'] = "Updation Is Done Successfully"
#             return jsonify(updated_data)            
        
#     except Exception as e:
#         response["status"] = 400
#         response["message"] = "An error occured in post_updation page" + str(e)
#         return jsonify(response)
                        

 #Delete post by user ID
# @app.route('/post/delete/<int:post_id>', methods=['POST'])
# def post_deletion(post_id):
     
#     response = {}
#     try:
        
#         if request.method == 'POST':
#             cursor = db_connection()
#             cursor.execute('DELETE FROM posts WHERE id = %s', (post_id,))
#             cursor.commit()
#             cursor.close()
            
#             message = {"id":post_id, "message":"content of given ID is deleted"}
#             return jsonify(message)
    
#     except:
#         response["status"] = 400
#         response["message"] = "An error occured in post_updation page"
#         return jsonify(response)
 

#Comments on posts 
# @app.route('/comments/<int:post_id>', methods=['POST'])
# def comments(post_id):
#     response = {}
#     # try:
#     if request.method == 'POST':
#         connection = mysql.connector.connect(
#         host="localhost",
#         user="parishram",
#         password="yadav08",
#         database = "chat_app"
#         )
#         cursor = connection.cursor()
            
#         data = request.get_json()
#         comment = data['comment']
            
#         if not comment:
#             return jsonify({"message": "There is no comment for the post"})
            
#         cursor.execute('INSERT INTO posts (comments) VALUES (%s) WHERE id=%s ', (comment, post_id))
#         connection.commit()
#         cursor.close()
    
#         message = {"post_id":post_id, "comment":comment}
#         return jsonify(message)
        
    # except:
    #     response["status"] = 400
    #     response["message"] = "An error occured in comment page" 
    #     return jsonify(response)
        
        


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return render_template('logout.html')
     
if __name__ == '__main__': 
    app.run(debug=True)