from flask import Flask, render_template, url_for, request, session, redirect, flash, jsonify
import mysql.connector 



app = Flask(__name__)
app.config['SECRET_KEY'] = "HELLOWORLD"

@app.route('/post/posts', methods=['POST'])
def create_post():
    
    response = {}
    try:
        if request.method == 'POST':
            connection = mysql.connector.connect(
            host="localhost",
            user="parishram",
            password="yadav08",
            database = "chat_app"
            )
            cursor = connection.cursor() 
                      
            data = request.get_json()
            content = data['content']
            post = [{"content":content}]
            
            if not post:
                return jsonify({"message": "Content are required"}), 400
            
            cursor.execute("INSERT INTO posts (content) VALUES (%s)", [content])
            # connection.commit()
            connection.commit()
            cursor.close()
            
            response['message'] = "Post Created in database Successfully!"
            response['status'] = 201
            response['post'] = post
            return jsonify(response)           

    except mysql.connector.Error as err:
        response["status"] = 400
        response["message"] = err
        return jsonify(response) 


if __name__ == '__main__': 
    app.run(debug=True)