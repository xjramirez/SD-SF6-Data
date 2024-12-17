import requests
import json

def queryPlayerSets(p1ID, header):
    h2h = open("headtoheadresponse.json", 'w')
    q = open("query.gql", "r")
    #print(headers)

    query = q.read()

    response = requests.post(url="https://api.start.gg/gql/alpha", json={"query": query, "operationName": "RecentSetsForPlayer", "variables": {"Player1Id":p1ID, "perPage":75}}, headers=header)
    #print("response status code: ", response.status_code)
    response_dict = json.loads(response.text)
    json.dump(response_dict, h2h, indent=2)

    h2h.close()
    q.close()

if __name__ == "__main__":
    queryPlayerSets(1361665, {"Authorization" : "Bearer 95514707613d135294e79a53380eb4dc"})