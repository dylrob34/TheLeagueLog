import mysql.connector as sql
import json
import requests
import time
import Summoner
import Manager

Summoner = Summoner.Summoner
Manager = Manager.Manager

def load():
    summoners = []

    connection = sql.connect(user="leaguelog", password="theleaguelog", host="10.0.0.4", port="3307", database="theleaguelog")
    cursor = connection.cursor()
    query = "select * from summoner"
    cursor.execute(query)

    for people in cursor:
        summoners.append(Summoner(people[1], people[0]))
    
    return summoners

def main():
    manager = Manager()
    
    summoners = load()

    while True:
        for summoner in summoners:
#            print(summoner)
            if summoner.update():
                manager.handle(summoner.name, summoner.summonerName, summoner.lastGameId)
            time.sleep(3)


if __name__ == '__main__':
    main()
