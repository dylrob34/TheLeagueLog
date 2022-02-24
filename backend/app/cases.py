from app import app
from flask import jsonify, Response, request
import json
import mysql.connector as sql

@app.route('/api/cases')
def cases():
    connection = sql.connect(user="leaguelog", password="theleaguelog", host="10.0.0.4", port="3307", database="theleaguelog")
    cursor = connection.cursor()
    query = "select * from cases"
    cursor.execute(query)

    js = []
    for case in cursor:
        js.append({'case': str(case[1]), 'description': str(case[2]), 'id': str(case[0])})
        
    return Response(json.dumps(js),  mimetype='application/json')

@app.route('/api/addCase', methods=["POST"])
def addCase():
    connection = sql.connect(user="leaguelog", password="theleaguelog", host="10.0.0.4", port="3307", database="theleaguelog")
    cursor = connection.cursor()
    body = request.json
    query = f"INSERT INTO cases VALUES({body['id']}, '{body['case']}', '{body['description']}');"
    cursor.execute(query)
    connection.commit()
    return jsonify({"success": "true"})

@app.route('/api/removeCase', methods=["POST"])
def removeCase():
    connection = sql.connect(user="leaguelog", password="theleaguelog", host="10.0.0.4", port="3307", database="theleaguelog")
    cursor = connection.cursor()
    body = request.json
    query = f"DELETE FROM cases WHERE (id= '{body['id']}');"
    cursor.execute(query)
    connection.commit()
    return jsonify({"success": "true"})