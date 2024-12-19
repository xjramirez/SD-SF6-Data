import json
import requests
from playersets import queryPlayerSets
from TOquery import TOUsersFromDiscriminator
from playersquery import generateSDPlayers
from playereventsquery import queryplayerevents

def main():
    print("Enter Authorization code:")
    userInput = input()
    header = {"Authorization" : "Bearer " + userInput}
    while(True):
        
        print("q - begin query | u - update TOs and Players | e - end program")
        userInput = input()
        if userInput == "q":
            pr = open("playersresponse.json", "r")
            pr_string = pr.read()
            player_dict = json.loads(pr_string)
            pr.close()

            userInput = None
            while(userInput not in player_dict):
                print("Input 1st Player's tag:")
                userInput = input()
            p1Id = player_dict[userInput]
            print("Player 1 found")

            userInput = None
            while(userInput not in player_dict):
                print("Input 2nd Player's tag:")
                userInput = input()
            p2Id = player_dict[userInput]
            
            print("Searching...")
            list_of_p1s_sets = gettwoplayerssets(p1Id=p1Id, p2Id=p2Id, header=header)
            setsIncludingP2(list_of_p1s_sets, p2ID=p2Id)
        
        elif userInput == "u":
            print("Getting TOs...")
            TOUsersFromDiscriminator(header)
            print("Generating SD Players...")
            generateSDPlayers(header)
            print("Done.")
        
        elif userInput == "e":
            break
    
        else:
            print("Invalid input.")


def setsIncludingP2(sets, p2ID):

    
    win_counter = {}

    for set in sets:
        if len(set["slots"][0]['entrant']['participants']) == 1: #check only 1v1s
            setwise_p1ID = set["slots"][0]['entrant']['participants'][0]['player']["id"]
            setwise_p2ID = set["slots"][1]['entrant']['participants'][0]['player']["id"]

            setwise_p1Name = set["slots"][0]['entrant']['participants'][0]['player']["gamerTag"]
            setwise_p2Name = set["slots"][1]['entrant']['participants'][0]['player']["gamerTag"]
            
            if (setwise_p1ID == p2ID or setwise_p2ID == p2ID):

                if (setwise_p1Name not in win_counter):
                    win_counter[setwise_p1Name] = 0
                if (setwise_p2Name not in win_counter):
                    win_counter[setwise_p2Name] = 0

                if set["winnerId"] == set["slots"][0]['entrant']["id"]:
                    win_counter[setwise_p1Name] = win_counter[setwise_p1Name] + 1
                else :
                    win_counter[setwise_p2Name] = win_counter[setwise_p2Name] + 1

                print(set["event"]['tournament']["name"] + ", " + set["fullRoundText"] + ", " + set["displayScore"]+ "\n")

    for pl, ct in win_counter.items():
        print(pl + ": " + str(ct) + " | ", end="")
    print()
    #print(sets_set)

def gettwoplayerssets(p1Id, p2Id, header):
    q = open("query.gql", "r")
    query = q.read()

    p1events = queryplayerevents(p1Id, header)
    p2events = queryplayerevents(p2Id, header)

    togetherevents = list(set(p1events) & set(p2events))

    sets_list = []

    for event in togetherevents:
        response = requests.post(url="https://api.start.gg/gql/alpha", json={"query": query, "operationName": "PlayerSetsInEvent", "variables": {"eventId": event, "playerId": p1Id}}, headers=header)
        #print("response status code: ", response.status_code)
        #print(response.text)
        response_json = json.loads(response.text)
        for eachset in response_json['data']['player']['sets']['nodes']:
            sets_list.append(eachset)
    


    q.close()
    return sets_list

if __name__ == "__main__":
    main()
    #daset = gettwoplayerssets(3578649, 178361, header={"Authorization" : "Bearer ___"})
    #setsIncludingP2(daset, 178361)