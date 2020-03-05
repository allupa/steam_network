'''
Koodissa haetaan Steam Web APIn kautta käyttäjien steamID:t ja heidän käyttäjännimensä, jotka yhdistetään kirjastoksi. 
'''

import pandas as pd
import requests
import util
import json

steamIDs = []
myFriends = []
steam_nick_id = {}

#API-key:n haku ja sijoittaminen
config = util.load_config()
with open(config["steam_ids"]["results"], 'r') as f:
    results_json = json.load(f)
    keys = [n for n in results_json.keys()]
    steam_ids = results_json[keys[0]] 
    print(f'Steam ids: {steam_ids}')
api_key = config['steam_api_key']['key']

#Tällä hetkellä testi id (nicon)
steamid = 76561198058128631

#Web API osoitteet, joista voidaan hakea tietoa
api_baseurl = 'http://api.steampowered.com/ISteamUser'
api_getfriends = api_baseurl + '/GetFriendList/v0001/?key={}&steamid={}&relationship=all'.format(steam_api_key, steamid)
api_getplayersummaries = api_baseurl + '/GetPlayerSummaries/v0002/?key={}&steamids='.format(steam_api_key)

#Haetaan webistä steamID:n käyttäjän kaverit listaan steamIDs
r = requests.get(api_getfriends)
data = r.json()
len_friends = len(data['friendslist']['friends'])
for i in range(len_friends):
    steamIDs.append(data['friendslist']['friends'][i]['steamid'])

#Haetaan webistä SteamID:tä vastaava username ja lisätään se listaan
i = 0
for placeholder in range(len(steamIDs)):
    steamID = steamIDs[i]
    re = requests.get(api_getplayersummaries + steamID)
    data1 = re.json()
    myFriends.append(data1['response']['players'][0]['personaname'])
    i += 1

steam_nick_id = dict(zip(myFriends, steamIDs))
print(steam_nick_id)