
import requests
import json

summonerURL = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"

lastGameIdURL = "https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/"
query = "?endIndex=1"

headers = {
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Riot-Token": "",
    "Accept-Language": "en-US,en;q=0.9",
}

class Summoner:

    def __init__(self, name, summonerName):
        self.name = name
        self.summonerName = summonerName
        self.accountId = requests.get(summonerURL + summonerName, headers=headers).json()["accountId"]
        try:
            self.lastGameId = self.getLastGameId()
        except:
            self.lastGameId = False
        while not self.lastGameId:
            try:
                self.lastGameId = self.getLastGameId()
            except:
                pass
    
    def getLastGameId(self):
        return str(requests.get(lastGameIdURL + self.accountId + query, headers=headers).json()["matches"][0]["gameId"])
    
    def update(self):
        try:
            currentId = str(requests.get(lastGameIdURL + self.accountId + query, headers=headers).json()["matches"][0]["gameId"])
        except:
           return False
        if currentId == self.lastGameId:
            return False
        else:
            self.lastGameId = currentId
            return True

    def __str__(self):
        return self.name + " has a summoner name of " + self.summonerName + " and their account id is " + self.accountId
