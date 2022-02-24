import requests
import json
import Condition
import sys, traceback

matchURL = "https://na1.api.riotgames.com/lol/match/v4/matches/"

headers = {
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Riot-Token": "",
    "Accept-Language": "en-US,en;q=0.9",
}

class Manager:
    def __init__(self):
        self.conditions = []
        self.conditions.append(Condition.Penta())
        #self.conditions.append(Condition.Win())
        #self.conditions.append(Condition.Lose())
        self.conditions.append(Condition.Feed())
        self.conditions.append(Condition.GG())
    
    def handle(self, name, summonerName, Id):
        game = requests.get(matchURL + Id, headers=headers).json()
        try:
            pi = game["participantIdentities"]
            player = pi[0]["player"]
        except:
            print("problem with game object")
#        print(game)
        for condition in self.conditions:
            if condition.validate(game, summonerName):
                condition.printMessage(name, summonerName, game)
