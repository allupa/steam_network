'''
Koodissa haetaan Steam Web APIn kautta käyttäjien steamID:t ja heidän käyttäjännimensä, jotka yhdistetään kirjastoksi. 
'''

import pandas as pd
import requests
import util
import json
import csv
import sys
from crawler import get_chrome_driver
from review_score_crawler import crawl_review_score


def write_to_node_csv(data):
    # TBD dialect
    with open('network.csv', 'w', encoding="utf-8") as f:
        nodewriter = csv.writer(f, delimiter=' ', quoting=csv.QUOTE_NONNUMERIC)
        nodewriter.writerows(data)


#API-key:n haku ja sijoittaminen
def main():
    config = util.load_config()
    driver = get_chrome_driver(config)
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
    api_baseurl = 'http://api.steampowered.com/ISteamUser'
    for i in steamids:
        #steamid = steamids[i]
        #Web API osoitteet, joista voidaan hakea tietoa
        api_getfriends = api_baseurl + '/GetFriendList/v0001/?key={}&steamid={}&relationship=all'.format(api_key, i)
        api_getplayersummaries = api_baseurl + '/GetPlayerSummaries/v0002/?key={}&steamids={}'.format(api_key, i)
        #Haetaan webistä steamID:n käyttäjän kaverit listaan steamIDs
        print(f'Making request with: {api_getfriends}')
        try:
            r = requests.get(api_getfriends)
            data = r.json()
            friend_nodes = [s for s in data['friendslist']['friends']]
            steamIDs = [n['steamid'] for n in friend_nodes]
            from_to = [n for n in steamIDs]
            for node in from_to:
                steam_data.append([int(i), int(node)])
            req = requests.get(api_getplayersummaries)
            data = req.json()
            persona_name = data['response']['players'][0]['personaname']
            crawl_review_score(persona_name, driver, i)
            for n in from_to:
                api_getfriends2 = api_baseurl + '/GetFriendList/v0001/?key={}&steamid={}&relationship=all'.format(api_key, n)
                r2 = requests.get(api_getfriends2)
                data2 = r2.json()
                print(data2)
                friend_nodes2 = [s for s in data2['friendslist']['friends']]
                steamIDs2 = [n['steamid'] for n in friend_nodes2]
                from_to2 = [n for n in steamIDs2]
                for node in from_to2:
                    steam_data.append([int(n), int(node)])
                r3 = requests.get(api_getplayersummaries)
                data3 = r3.json()
                persona_name = data3['response']['players'][0]['personaname']
                crawl_review_score(persona_name, driver, n)



        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(exc_type, exc_tb.tb_lineno)
            continue
        # except:
        #     print("Unexpected error:", sys.exc_info()[0])
        #     break
        
    write_to_node_csv(steam_data)
    return 0


main()




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