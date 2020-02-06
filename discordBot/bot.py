import json
import requests
import time


summoners = ["4TFC4"]
getSummoner = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"


getLastGameId = "https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/"
query = "?endIndex=1"


getMatch = "https://na1.api.riotgames.com/lol/match/v4/matches/"


webHook = "https://discordapp.com/api/webhooks/674693097619456001/S9gWLZeWyX15llE8978qNCwpkOjukNwt2rLu7FZcFkcEAxQB4Qj" \
          "HnnrGeadJ8LSbqXUj"
body = "bradys feeding again :/"


headers = {
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Riot-Token": "RGAPI-effc7286-46e4-4f2f-9b2c-8c00b9838e20",
    "Accept-Language": "en-US,en;q=0.9",
}


match = ""


def main():
    result = requests.get(getSummoner + summoners[0], headers=headers)
    id = result.json()["accountId"]


    while True:
        result = requests.get(getLastGameId + id + query, headers=headers)
        currentMatch = str(result.json()["matches"][0]["gameId"])
        global match
        if currentMatch != match:
            match = currentMatch
            result = requests.get(getMatch + str(match), headers=headers).json()
            players = result["participantIdentities"]
            playerId = ""
            for player in players:
                if player["player"]["summonerName"] == summoners[0]:
                    playerId = player["participantId"]
                    break
            kills = result["participants"][playerId-1]["stats"]["kills"]
            deaths = result["participants"][playerId-1]["stats"]["deaths"]


            if float(kills) / float(deaths) < .5:
                data = {}
                data["content"] = str(kills) + " kills and " + str(deaths) + " deaths, " + body
                result = requests.post(webHook, data=json.dumps(data), headers={"Content-Type": "application/json"})
            else:
                print("didnt feed, good job")
        time.sleep(60)




if __name__ == '__main__':
    main()