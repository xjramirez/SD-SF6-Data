import requests
import json

def TOUsersFromDiscriminator(header):
    q = open("query.gql", "r")

    #print(headers)

    query = q.read()

    TO_discriminators = {"unprotectedSEX" : "79749e7f", "Corn?": "6ff177b4", "Tru1chi!": "da03708c", "astralxocean":"4d93e8fb"}
    TO_users = {}
    for TO in TO_discriminators.keys():
        response = requests.post(url="https://api.start.gg/gql/alpha", json={"query": query, "operationName": "UserBySlug", "variables": {"slug": "user/" + TO_discriminators[TO]}}, headers=header)
        #print("response status code: ", response.status_code)
        #print(response.text)
        user_json = json.loads(response.text)
        TO_users[TO] = user_json["data"]["user"]["id"]

    q.close()

    t = open("TOresponse.json", "w")
    #print(TO_users)
    json.dump(TO_users, t, indent=4)
    t.close()


