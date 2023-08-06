import json
import requests

ddragonVersion = 'https://ddragon.leagueoflegends.com/api/versions.json'
response = requests.get(ddragonVersion)
json_object = response.json()
latestVersion = json_object[0]


def leaguenames(championID):
    url = 'http://ddragon.leagueoflegends.com/cdn/' + latestVersion + '/data/en_US/champion.json'
    r = requests.get(url)
    json_obj = r.json()
    data = json_obj['data']
    for name, attributes in data.items():
        if attributes['key'] == str(championID):
            return name



