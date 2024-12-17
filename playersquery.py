import requests
import json

def generateSDPlayers(header):
    presponse = open("playersresponse.json", "w")

    q = open("query.gql", "r")
    query = q.read()

    t = open("TOresponse.json", "r")
    t_string = t.read()
    TOs = json.loads(t_string)


    player_dict = {}

    for TOId in TOs.values():
        response = requests.post(url="https://api.start.gg/gql/alpha", json={"query": query, "operationName": "PlayersByTournamentsByOwner", "variables": {"perPage" : 20, "ownerId": TOId}}, headers=header)
        response_dict = json.loads(response.text)
        #presponse.write(response.text)
        if ("data" in response_dict):
            for tournament in response_dict["data"]["tournaments"]["nodes"]:
                for event in tournament["events"]:
                    if event["videogame"]["id"] == 43868:
                        for entrant in event['entrants']['nodes']:
                            player_dict[entrant["participants"][0]["player"]["gamerTag"]] = entrant["participants"][0]["player"]["id"]

    #print(player_dict)

    json.dump(player_dict, presponse, indent=4)

    t.close()
    q.close()
    presponse.close()