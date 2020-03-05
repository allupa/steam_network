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
    with open('gamesID_network.csv', 'w', encoding="utf-8") as f:
        nodewriter = csv.writer(f, delimiter=' ', quoting=csv.QUOTE_NONNUMERIC)
        nodewriter.writerows(data)


#API-key:n haku ja sijoittaminen
def main():
    from_to = []
    config = util.load_config()
    with open(config["steam_ids"]["results"], 'r') as f:
        results_json = json.load(f)
        keys = [n for n in results_json.keys()]
        steamids = results_json[keys[0]] 
    print("Closing config...")
    api_key = config['steam_api_key']['key']
    steam_data = []
    print("Starting to iterate...")
    for i in range(10):
        steamid = steamids[i]
        #Web API osoitteet, joista voidaan hakea tietoa
        api_getownedgames = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v001/?key={}&steamid={}&format=json&include_appinfo=1&include_played_free_games=1'.format(api_key, steamid)
        #Haetaan webistä steamID:n käyttäjän kaverit listaan steamIDs
        print(f'Making request with: {api_getownedgames}')
        try:
            r = requests.get(api_getownedgames)
            data = r.json()
            game_nodes = [s for s in data['response']['games']]
            gameIDs = [n['name'] for n in game_nodes]
            print(steamid)
            from_to = [n for n in gameIDs]
            for node in from_to:
                steam_data.append([int(steamid), node])
            

        except KeyError:
            print("Failed request, KeyError")
            continue

    write_to_node_csv(steam_data)
    return 0


main()
