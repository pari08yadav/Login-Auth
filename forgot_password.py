from flask import Flask, request, jsonify
import mysql.connector 

app = Flask(__name__)
app.config['SECRET_KEY'] = "HELLOWORLD"

@app.route('/post/forgot_password', methods=['POST'])
def forgot_pass():
    response = {}
    message = ''
    try:
        if request.method == 'POST':
            
            data = request.get_json()
            username = data["username"]
            new_password = data["new_password"]
            
            connection = mysql.connector.connect(
            host="localhost",
            user="parishram",
            password="yadav08",
            database = "chat_app"
            
            )
            cursor = connection.cursor()
            
            # cursor.execute("SELECT password FROM users WHERE username=%s", (username,))
            
            # old_password = cursor.fetchone()
            
            # if old_password:
            #     response['message'] = {"password": old_password}
            #     return jsonify(response)
            
            cursor.execute('UPDATE users SET password = %s WHERE username = %s', (new_password, username) )
            connection.commit()
            cursor.close()
            
            response['message'] = {"your new password is: " : new_password}
            return jsonify(response)
            
    except Exception as e:
        response["status"] = 400
        response["message"] = "An error occured on post login page" + str(e)
        return jsonify(response) 

if __name__ == '__main__':
    app.run(debug=True)