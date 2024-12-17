import json
from headtoheadquery import queryPlayerSets
from TOquery import TOUsersFromDiscriminator
from playersquery import generateSDPlayers

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
            queryPlayerSets(p1Id, header)
            setsIncludingP2(p2Id)
            break
        
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


def setsIncludingP2(p2ID):
    h2h = open("headtoheadresponse.json", 'r')
    h2h_string = h2h.read()
    headtoheadresponse = json.loads(h2h_string)

    h2h.close()

    data = headtoheadresponse["data"]
    player = data["player"]
    sets = player["sets"]
    nodes = sets["nodes"]

    sets_set = []
    win_counter = {}

    for set in nodes:
        setwise_p1ID = set["slots"][0]['entrant']['participants'][0]['player']["id"]
        setwise_p2ID = set["slots"][1]['entrant']['participants'][0]['player']["id"]

        setwise_p1Name = set["slots"][0]['entrant']['participants'][0]['player']["gamerTag"]
        setwise_p2Name = set["slots"][1]['entrant']['participants'][0]['player']["gamerTag"]
        
        if (setwise_p1ID == p2ID or setwise_p2ID == p2ID) and set['event']["videogame"]["id"] == 43868:
            sets_set.append(set['id'])

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

if __name__ == "__main__":
    main()