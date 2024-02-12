from flask import Flask, request, session, jsonify
import mysql.connector 
import jwt
import datetime
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = "HELLOWORLD"


@app.route('/post/logout', methods=['POST'])
def logput():
    
    response = {}
    message = ''
    try:
        if request.method == 'POST':
            data = request.get_json()
            username = data['username']
            password = data['password']
            
            connection = mysql.connector.connect(
            host="localhost",
            user="parishram",
            password="yadav08",
            database = "chat_app"
            
            )
            cursor = connection.cursor()
            
            cursor.execute("SELECT token FROM users WHERE username=%s AND password=%s", (username, password))
            
            users_token = cursor.fetchone()
            
            # if users_token:
            #     response['message'] = {"User's token is :" : users_token, "status":200}
            #     return jsonify(response)
                
            if 'token' in session and session['token'] == users_token:
                session.clear()
                response['message'] = "Logout Successfully"
                return jsonify(response)
            
            else:
                response['message'] = "invalid token"
                response['status'] = 400
                return jsonify(response)
    
    except Exception as e:
        response["status"] = 400
        response["message"] = "An error occured on logout page" + str(e)
        return jsonify(response)
    
    
if __name__ == '__main__':
    app.run(debug=True)