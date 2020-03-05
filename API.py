'''
Koodissa haetaan Steam Web APIn kautta käyttäjien steamID:t ja heidän käyttäjännimensä, jotka yhdistetään kirjastoksi. 
'''

import pandas as pd
import requests
import util
import json
import csv
import sys


def write_to_node_csv(data):
    # TBD dialect
    with open('network.csv', 'w', encoding="utf-8") as f:
        nodewriter = csv.writer(f, delimiter=' ', quoting=csv.QUOTE_NONNUMERIC)
        nodewriter.writerows(data)


#API-key:n haku ja sijoittaminen
def main():
    from_to = []
    steamIDs = []
    myFriends = []
    steam_nick_id = {}
    config = util.load_config()
    with open(config["steam_ids"]["results"], 'r') as f:
        results_json = json.load(f)
        keys = [n for n in results_json.keys()]
        steamids = results_json[keys[0]] 
    print("Closing config...")
    api_key = config['steam_api_key']['key']
    steam_data = []
    counter = 0
    print("Starting to iterate...")
    for i in range(10):
        steamid = steamids[i]
        #Web API osoitteet, joista voidaan hakea tietoa
        api_baseurl = 'http://api.steampowered.com/ISteamUser'
        api_getfriends = api_baseurl + '/GetFriendList/v0001/?key={}&steamid={}&relationship=all'.format(api_key, steamid)
        api_getplayersummaries = api_baseurl + '/GetPlayerSummaries/v0002/?key={}&steamids='.format(api_key)
        #Haetaan webistä steamID:n käyttäjän kaverit listaan steamIDs
        print(f'Making request with: {api_getfriends}')
        try:
            r = requests.get(api_getfriends)
            data = r.json()
            friend_nodes = [s for s in data['friendslist']['friends']]
            steamIDs = [n['steamid'] for n in friend_nodes]
            print(steamid)
            from_to = [n for n in steamIDs]
            for node in from_to:
                steam_data.append([int(steamid), int(node)])
            
            #Haetaan webistä SteamID:tä vastaava username ja lisätään se listaan
            # i = 0
            # for _ in range(2):
            #     steamID = steamIDs[i]
            #     print("Steamid: ", steamID)
            #     re = requests.get(api_getplayersummaries + steamID)
            #     print(re)
            #     data1 = re.json()
            #     myFriends.append(data1['response']['players'][0]['personaname'])
            #     i += 1
            
            # steam_nick_id = dict(zip(myFriends, steamIDs))
            # myFriends = []
            # print(f'Appending a steam nick to list... {counter}')
            # steam_data.append([steam_nick_id])
            # counter += 1
        except KeyError:
            print("Failed request, KeyError")
            continue
        # except:
        #     print("Unexpected error:", sys.exc_info()[0])
        #     break
        
    write_to_node_csv(steam_data)
    return 0


main()
