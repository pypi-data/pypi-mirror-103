from util import online_player, town_data, nation_data, resident_data
from emcpy import Online
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