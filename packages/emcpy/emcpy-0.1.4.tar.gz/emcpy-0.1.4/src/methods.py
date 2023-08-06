from util import online_player, town_data, nation_data, resident_data, townless
import requests
"""
More useful Methods will be added soon
Give suggestions!
"""
def getAllOnline():
    data = online_player("")
    return data

def getAllTowns():
    data = town_data("")
    return data

def getAllNations():
    data = nation_data("")
    return data

def getAllResidents():
    data = resident_data("")
    return data

def getTownless():
    _all = []
    _townless = townless()
    for i in _townless:
        _all += [i]
    return _all

def getPlayerFace(name: str):
    if name == "":
        raise FileNotFoundError("Missing argument: name")
    data = requests.get(f'https://earthmc.net/map/tiles/faces/16x16/{name}.png')
    if data.status_code == 404:
        raise FileNotFoundError("File not found")
    return f'https://earthmc.net/map/tiles/faces/16x16/{name}.png'

def getOnlineKings():
    _all = []
    players = getAllOnline()
    for player in players:
        try:
            if player["rank"] == "Nation Leader":
                _all += [player]
        except KeyError:
            pass
    return _all
