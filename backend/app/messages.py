from app import app
from flask import jsonify, Response, request
import json
import mysql.connector as sql

@app.route('/api/messages')
def messages():
    connection = sql.connect(user="leaguelog", password="theleaguelog", host="10.0.0.4", port="3307", database="theleaguelog")
    cursor = connection.cursor()
    query = "select * from messages"
    cursor.execute(query)

    js = []
    for message in cursor:
        js.append({'id': str(message[0]), 'case': str(message[1]), 'message': str(message[2])})
        
    return Response(json.dumps(js),  mimetype='application/json')

@app.route('/api/addMessage', methods=["POST"])
def addMessage():
    connection = sql.connect(user="leaguelog", password="theleaguelog", host="10.0.0.4", port="3307", database="theleaguelog")
    cursor = connection.cursor()
    body = request.json
    query = f"INSERT INTO messages (`case`, `message`) VALUES({body['case']}, '{body['message']}');"
    print("query " + query)
    cursor.execute(query)
    connection.commit()
    return jsonify({"success": "true"})

@app.route('/api/removeMessage', methods=["POST"])
def removeMessage():
    connection = sql.connect(user="leaguelog", password="theleaguelog", host="10.0.0.4", port="3307", database="theleaguelog")
    cursor = connection.cursor()
    body = request.json
    query = f"DELETE FROM messages WHERE (id= {body['id']});"
    print("query " + query)
    cursor.execute(query)
    connection.commit()
    return jsonify({"success": "true"})