import requests
import json

webHook = "https://discordapp.com/api/webhooks/674693097619456001/S9gWLZeWyX15llE8978qNCwpkOjukNwt2rLu7FZcFkcEAxQB4Qj" \
          "HnnrGeadJ8LSbqXUj"

getNameOfChamp = "http://ddragon.leagueoflegends.com/cdn/10.6.1/data/en_US/champion.json"

headers = {
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Riot-Token": "",
    "Accept-Language": "en-US,en;q=0.9",
}


# Condition Interface
class Condition:

    def __init__(self):
        pass

    def getPlayerId(self, summonerName, game):
        players = game["participantIdentities"]
        playerId = ""
        for player in players:
            if player["player"]["summonerName"] == summonerName:
                return str(player["participantId"])

    def getParticipants(self, game):
        return game["participants"]

    def getStats(self, game, summonerName):
        playerId = self.getPlayerId(summonerName, game)
        participants = self.getParticipants(game)
        for player in participants:
            if str(player["participantId"]) == playerId:
                return player["stats"]

    def getRole(self, game, summonerName):
        playerId = self.getPlayerId(summonerName, game)
        participants = self.getParticipants(game)
        for player in participants:
            if str(player["participantId"]) == playerId:
                timeline = player["timeline"]
        role = str(timeline["role"])
        return role

    def getWin(self, game, summonerName):
        playerStats = self.getStats(game, summonerName)
        return bool(playerStats["win"])

    def getChamp(self, game, summonerName):
        champName = ""
        playerId = self.getPlayerId(summonerName, game)
        participants = self.getParticipants(game)
        champId = ""
        for player in participants:
            if str(player["participantId"]) == playerId:
                champId = player["championId"]
        response = requests.get(getNameOfChamp, headers=headers).json()
        champions = response["data"]
        for champ in champions:
            key = str(champions[champ]["key"])
            if key == str(champId):
                return champions[champ]["name"]
        return "error"

    def getCreepScore(self, game, summonerName):
        stats = self.getStats(game, summonerName)
        return (str(stats["totalMinionsKilled"] + stats["neutralMinionsKilled"]))

    def getVisionScore(self, game, summonerName):
        stats = self.getStats(game, summonerName)
        return (str(stats["visionScore"]))

    def validate(self, game):
        pass

    def printMessage(self, name, summonerName, game):
        pass

    def send(self, message):
        data = {}
        data["content"] = message
        requests.post(webHook, data=json.dumps(data), headers={
                      "Content-Type": "application/json"})


class Penta(Condition):
    def __init__(self):
        super()
        self.conditionId = 0

    def validate(self, game, summonerName):
        playerStats = self.getStats(game, summonerName)
        if int(playerStats["pentaKills"]) >= 1:
            return True

    def printMessage(self, name, summonerName, game):
        playerStats = self.getStats(game, summonerName)
        message = ""
        if int(playerStats["pentaKills"]) > 1:
            message = summonerName + ", that mother fucking LEGEND, got " + \
                int(playerStats["pentaKills"]) + \
                " penta kills in his last game"
        else:
            message = f"{summonerName}, that mother fucking LEGEND, got a penta kill last game"

        self.send(message)


class Win(Condition):
    def __init__(self):
        super()
        self.conditionId = 1

    def validate(self, game, summonerName):
        playerStats = self.getStats(game, summonerName)
        return bool(playerStats["win"])

    def printMessage(self, name, summonerName, game):
        message = name + " won his game!"
        self.send(message)


class Lose(Condition):
    def __init__(self):
        super()
        self.conditionId = 2

    def validate(self, game, summonerName):
        playerStats = self.getStats(game, summonerName)
        return False if bool(playerStats["win"]) else True

    def printMessage(self, name, summonerName, game):
        message = name + " lost his game!"
        self.send(message)


class Feed(Condition):
    def __init__(self):
        super()
        self.conditionId = 3

    def validate(self, game, summonerName):
        playerStats = self.getStats(game, summonerName)
        kills = playerStats["kills"]
        deaths = playerStats["deaths"]
        role = self.getRole(game, summonerName)
        assists = playerStats["assists"]
        visionScore = self.getVisionScore(game, summonerName)
        if role != "DUO_SUPPORT":
            if deaths > 0 and kills > 0:
                if float(kills) / float(deaths) <= .5 and deaths >= 7:
                    return True
                if float(kills) / float(deaths) < .25 and deaths < 7:
                    return True
            elif kills == 0:
                if deaths >= 4:
                    return True
        elif role == "DUO_SUPPORT":
            if deaths > 0 and kills > 0:
                if float(kills) / float(deaths) < .4 and int(visionScore) <= 20 and assists < 3 * deaths:
                    return True
            if kills == 0 and deaths > 0:
                if deaths >= 5 and int(visionScore) <= 20 and assists < 3 * deaths:
                    return True
        return False

    def printMessage(self, name, summonerName, game):
        playerStats = self.getStats(game, summonerName)
        champName = self.getChamp(game, summonerName)
        win = self.getWin(game, summonerName)
        role = self.getRole(game, summonerName)
        if win == True:
            msg = "won"
        elif win == False:
            msg = "lost"
        creepScore = self.getCreepScore(game, summonerName)
        if role != "DUO_SUPPORT":
            self.send(
                f"{name} fed his ass off last game as {champName}, with {playerStats['deaths']} deaths and only {playerStats['kills']} kills! He {msg}, with {creepScore} cs!")
        if role == "DUO_SUPPORT":
            self.send(
                f"{name} sucks at playing support as {champName}, going {playerStats['kills']} and {playerStats['deaths']}, and having {playerStats['assists']} assists, and a vision score of {playerStats['visionScore']}! He {msg}, with {creepScore} cs!")


class GG(Condition):
    def __init__(self):
        super()
        self.conditionId = 4

    def validate(self, game, summonerName):
        playerStats = self.getStats(game, summonerName)
        kills = playerStats["kills"]
        deaths = playerStats["deaths"]
        role = self.getRole(game, summonerName)
        assists = playerStats["assists"]
        visionScore = self.getVisionScore(game, summonerName)
        if role != "DUO_SUPPORT":
            if deaths > 0 and kills > 0:
                if float(kills) / float(deaths) >= 2.5 and kills >= 4:
                    return True
            elif deaths == 0 and kills >= 4:
                return True
        elif role == "DUO_SUPPORT":
            if deaths > 0 and kills > 0:
                if float(assists) >= float(deaths) * 3 and int(visionScore) >= 50 and float(deaths) <= 10:
                    return True
            if deaths == 0:
                if float(assists) >= 3 and int(visionScore) >= 50:
                    return True
        return False

    def printMessage(self, name, summonerName, game):
        playerStats = self.getStats(game, summonerName)
        champName = self.getChamp(game, summonerName)
        win = self.getWin(game, summonerName)
        role = self.getRole(game, summonerName)
        assists = playerStats["assists"]
        damageDealt = playerStats["totalDamageDealt"]
        if win == True:
            msg = "won"
        elif win == False:
            msg = "lost"
        creepScore = self.getCreepScore(game, summonerName)
        if role != "DUO_SUPPORT" and damageDealt >= long(30000):
            self.send(f"{name} popped off last game as {champName}, with {playerStats['kills']} kills and {playerStats['deaths']} deaths! He did {damageDealt} total damage. And he {msg}, with {creepScore} cs!")
        if role != "DUO_SUPPORT" and damageDealt < long(30000):
            self.send(f"{name} popped off last game as {champName}, with {playerStats['kills']} kills and {playerStats['deaths']} deaths! He {msg}, with {creepScore} cs!")
        if role == "DUO_SUPPORT":
            self.send(f"{name} was an absolute legend as support {champName}, going {playerStats['kills']} and {playerStats['deaths']}, while having {assists} assists, and a vision score of {playerStats['visionScore']}! He {msg}, with {creepScore} cs!")

