import requests
import json

def queryPlayerSets(p1ID, header):
    ps = open("playersetsresponse.json", 'w')
    q = open("query.gql", "r")
    #print(headers)

    query = q.read()

    response = requests.post(url="https://api.start.gg/gql/alpha", json={"query": query, "operationName": "RecentSetsForPlayer", "variables": {"Player1Id":p1ID, "perPage":75}}, headers=header)
    #print("response status code: ", response.status_code)
    response_dict = json.loads(response.text)
    json.dump(response_dict, ps, indent=2)

    ps.close()
    q.close()

if __name__ == "__main__":
    queryPlayerSets(1361665, {"Authorization" : "Bearer ___"})