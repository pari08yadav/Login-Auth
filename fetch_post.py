from flask import Flask, render_template, url_for, request, session, redirect, flash, jsonify
import mysql.connector 


app = Flask(__name__)
app.config['SECRET_KEY'] = "HELLOWORLD"

#get specific post by post id
@app.route('/post/post_by_id/<int:post_id>', methods=['POST'])
def get_post_by_id(post_id):
    
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
            cursor.execute('SELECT * FROM posts WHERE id=%s', (post_id,))
            post = cursor.fetchone()
            cursor.close()
            
            if not post:
                return jsonify({"message": "The Post You Want To Find Is Not Exist."})
            
            post_data = {"id":post[0], "content":post[2]}
            return jsonify(post_data)

    except Exception as e:
        response["status"] = 400
        response["message"] = "An error occured" + str(e)
        return jsonify(response)

if __name__ == '__main__': 
    app.run(debug=True)