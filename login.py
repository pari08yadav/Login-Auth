from flask import Flask, render_template, url_for, request, session, redirect, flash, jsonify
import mysql.connector 
import jwt
import datetime
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = "HELLOWORLD"

@app.route('/post/login', methods=['POST'])
def login():   
    # loginform = LoginForm()
    response = {}
    message = ''
    try:
        if request.method == 'POST':
            
            data = request.get_json()
            username = data["username"]
            password = data["password"]
            
            connection = mysql.connector.connect(
            host="localhost",
            user="parishram",
            password="yadav08",
            database = "chat_app"
            
            )
            cursor = connection.cursor()
            # cursor = db_connection()
            cursor.execute("SELECT user_id FROM users WHERE username=%s AND password=%s", (username, password))
            # print("aaaaaaaaaaaaaaaaaaaa")
        
            record = cursor.fetchone()
            # connection.commit()
                
            if record:
                #Generate token
                token = jwt.encode({'username':random.randrange(1,9999), "exp":datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'], algorithm='HS256')
                
                #Update Token into user table 
                cursor.execute("UPDATE users SET token=%s WHERE username=%s", (token, username))
                connection.commit()
                                                       

                response["status"] = 200
                response["data"] = {"user_id": record[0],"token":token}
                response['message'] = "You are loggedin successfully"
                return jsonify(response)
            
            response['status'] = 400
            response['message'] = "Invalid credential"
            return jsonify(response)
    
    except Exception as e:
        response["status"] = 400
        response["message"] = "An error occured on post login page" + str(e)
        return jsonify(response) 
    
     
if __name__ == '__main__': 
    app.run(debug=True)