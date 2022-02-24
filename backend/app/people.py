from app import app
from flask import jsonify, Response, request
import json
import mysql.connector as sql

@app.route('/api/people')
def people():
    connection = sql.connect(user="leaguelog", password="theleaguelog", host="10.0.0.4", port="3307", database="theleaguelog")
    cursor = connection.cursor()
    query = "select * from summoner"
    cursor.execute(query)

    js = []
    i = 0
    for people in cursor:
        js.append({'name': str(people[1]), 'summonerName': str(people[0]), 'id': i})
        i = i + 1
        
    return Response(json.dumps(js),  mimetype='application/json')

@app.route('/api/addPeople', methods=["POST"])
def addPeople():
    connection = sql.connect(user="leaguelog", password="theleaguelog", host="10.0.0.4", port="3307", database="theleaguelog")
    cursor = connection.cursor()
    body = request.json
    query = f"INSERT INTO summoner VALUES('{body['summonerName']}', '{body['name']}');"
    cursor.execute(query)
    connection.commit()
    return jsonify({"success": "true"})

@app.route('/api/removePeople', methods=["POST"])
def removePeople():
    connection = sql.connect(user="leaguelog", password="theleaguelog", host="10.0.0.4", port="3307", database="theleaguelog")
    cursor = connection.cursor()
    body = request.json
    query = f"DELETE FROM summoner WHERE (summonerName= '{body['summonerName']}');"
    cursor.execute(query)
    connection.commit()
    return jsonify({"success": "true"})