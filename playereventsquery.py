import requests
import json

def queryplayerevents(playerId, header):
    q = open("query.gql", "r")
    query = q.read()



    response = requests.post(url="https://api.start.gg/gql/alpha", json={"query": query, "operationName": "EventsByPlayer", "variables": {"PlayerId": playerId}}, headers=header)
    #print("response status code: ", response.status_code)
    #print(response.text)
    response_json = json.loads(response.text)


    q.close()

    e = open("playereventsresponse.json", "w")
    #print(TO_users)
    json.dump(response_json, e, indent=4)
    e.close()

    playerevents = []
    for event in response_json['data']['player']['user']['events']['nodes']:
        playerevents.append(event['id'])

    return playerevents

if __name__ == "__main__":
    queryplayerevents({"Authorization" : "Bearer ___"})