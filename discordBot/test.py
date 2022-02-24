import mysql.connector as sql

print("Hello World!")

connection = sql.connect(user="leaguelog", password="theleaguelog", host="10.0.0.4", port="3307", database="theleaguelog")

print("connected to server")

cursor = connection.cursor()

query = "select * from summoner"

cursor.execute(query)


class Summoner:

    def __init__(self, n):
        self.name = n
    
    def getLastGame(self):
        return {"kills": 8, "deaths": 2}
    
    def getMessage(self):
        kd = self.getLastGame()
        message = self.name + " had " + str(kd["kills"]) + " kills and " + str(kd["deaths"]) + " deaths"
        return message

summoners = []

for s in cursor:
    summoners.append(Summoner(s[0]))

for s in summoners:
    print(s.getMessage())
