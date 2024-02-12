from flask import Flask, render_template, url_for, request, session, redirect, flash, jsonify
import mysql.connector 


app = Flask(__name__)
app.config['SECRET_KEY'] = "HELLOWORLD"


@app.route('/post/update/<int:post_id>', methods=['PUT'])
def post_updation(post_id):
    
    response = {}
    try:
        if request.method == 'PUT':
            connection = mysql.connector.connect(
            host="localhost",
            user="parishram",
            password="yadav08",
            database = "chat_app"
            
            )
            cursor = connection.cursor()
            data = request.get_json()
            new_content = data['content']
            
            if not new_content:
                return jsonify({"message": "Content is Required for updation."})
            
            cursor.execute('UPDATE posts SET content = %s WHERE id = %s', (new_content, post_id))
            connection.commit()
            cursor.close()

            updated_data = {"id":post_id, "updated_content":new_content}
            response['message'] = "Updation Is Done Successfully"
            return jsonify(updated_data)            
        
    except Exception as e:
        response["status"] = 400
        response["message"] = "An error occured in post_updation page" + str(e)
        return jsonify(response)
                        
if __name__ == '__main__': 
    app.run(debug=True)