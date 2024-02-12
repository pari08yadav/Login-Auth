from flask import Flask, render_template, url_for, request, session, redirect, flash, jsonify
import mysql.connector 
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = "HELLOWORLD"

@app.route('/post/register', methods=['POST'])
def register():
    message = ''
    response = {}
    try:
        if request.method == 'POST':
            
            # registerform = RegisterForm()

            data = request.get_json()
            username = data["username"]
            password = data["password"]
            
            if len(username) == 0 or len(username) < 4 or len(username) > 20:
                response["status"] = 400
                response["message"] = "Username is invalid, It must be alphanumeric, at least 4 character log and maximum 20 chars "
                return jsonify(response)          
           
            if not re.findall('^[a-z0-9]+$',username):
                response["status"] = 400
                response["message"] = "Username is invalid, It must be alphanumeric"
                return jsonify(response)                    
            
            connection = mysql.connector.connect(
            host="localhost",
            user="parishram",
            password="yadav08",
            database = "chat_app"
            )
            cursor = connection.cursor()
            cursor.execute("SELECT user_id,username FROM users WHERE username =%s",[username])
            record = cursor.fetchone()

            if record:
                response["status"] = 400
                response["message"] = "Username has been already used by someone, please enter another"
                return jsonify(response)                

            cursor.execute('INSERT INTO users VALUES (%s, %s, %s, %s)', (None, username, password, None))
            connection.commit()
            
            response["status"] = 200
            response["message"] = "Your Registration is done Successfully! "
            return jsonify(response)   
                     
    except Exception as e:
        response["status"] = 400
        response["message"] = "An error occured: " + str(e)
        return jsonify(response)          

if __name__ == '__main__': 
    app.run(debug=True)