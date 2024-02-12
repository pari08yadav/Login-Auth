from flask import Flask, render_template, url_for, request, session, redirect, flash, jsonify
import mysql.connector 


app = Flask(__name__)
app.config['SECRET_KEY'] = "HELLOWORLD"


@app.route('/post/delete/<int:post_id>', methods=['DELETE'])
def post_deletion(post_id):
     
    response = {}
    try:
        
        if request.method == 'DELETE':
            connection = mysql.connector.connect(
            host="localhost",
            user="parishram",
            password="yadav08",
            database = "chat_app"
            
            )
            cursor = connection.cursor()
            cursor.execute('DELETE FROM posts WHERE id = %s', (post_id,))
            connection.commit()
            cursor.close()
            
            message = {"id":post_id, "message":"content of given ID is deleted"}
            return jsonify(message)
    
    except:
        response["status"] = 400
        response["message"] = "An error occured in post_updation page"
        return jsonify(response)

if __name__ == '__main__': 
    app.run(debug=True)