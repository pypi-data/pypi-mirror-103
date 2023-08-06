import util
import exceptions
import methods
from exceptions import ResidentNotFoundException, NationNotFoundException, TownNotFoundException, \
    PlayerNotFoundException, OnlinePlayerNotFoundException
__all__ = [
    "util",
    "methods"
    "exceptions",
    "Town",
    "Nation",
    "Resident",
    "Online",
    "Townless",
    "Server"
]

from util import server_data


class Town:
    def __init__(self, name: str):
        if name == "":
            raise TownNotFoundException("Missing argument: name")
        town_data = util.town_data(name)
        if town_data == "That town does not exist!":
            raise TownNotFoundException(town_data)
        self.name = town_data["name"]
        self.nation = town_data["nation"]
        self.residents = town_data["residents"]
        self.nation_residents = town_data["nationResidents"]
        self.claims = town_data["area"]
        self.mayor = town_data["mayor"]
        self.flags = {
            "pvp": town_data["pvp"],
            "mobs": town_data["mobs"],
            "public_spawn": town_data["public"],
            "explosions": town_data["explosion"],
            "fire": town_data["fire"],
            "capital": town_data["capital"]
        }

    def __str__(self) -> str:
        return self.name


class Nation:
    def __init__(self, name: str):
        if name == "":
            raise NationNotFoundException("Missing argument: name")
        nation_data = util.nation_data(name)
        if nation_data == "That nation does not exist!":
            raise NationNotFoundException(nation_data)
        self.name = nation_data["name"]
        self.residents = nation_data["residents"]
        self.towns = nation_data["towns"]
        self.king = nation_data["king"]
        self.capital = nation_data["capitalName"]
        self.claims = nation_data["area"]
        self.coords = {"x": nation_data["capitalX"], "z": nation_data["capitalZ"]}

    def __str__(self) -> str:
        return self.name


class Resident:
    def __init__(self, name: str):
        if name == "":
            raise ResidentNotFoundException("Missing argument: name")
        resident_data = util.resident_data(name)
        if resident_data == "That resident does not exist!":
            raise ResidentNotFoundException(resident_data)
        self.name = resident_data["name"]
        self.town = resident_data["town"]
        self.nation = resident_data["nation"]
        self.rank = resident_data["rank"]

    def __str__(self) -> str:
        return self.name


class Online:
    def __init__(self, name: str):
        if name == "":
            raise OnlinePlayerNotFoundException("Missing argument: name")
        online_data = util.online_player(name)
        if online_data == "That player is not online or does not exist!":
            raise OnlinePlayerNotFoundException(online_data)
        self.nick = online_data["nickname"]
        self.name = online_data["name"]
        self.town = online_data["town"]
        self.nation = online_data["nation"]
        self.rank = online_data["rank"]
        self.isUnderground = online_data["isUnderground"]
        self.coords = online_data[{
            "x": online_data["x"],
            "y": online_data["y"],
            "z": online_data["z"]
        }]

    def __str__(self) -> str:
        return self.name


class Server:
    def __init__(self):
        data = server_data()
        self.online = data["online"]
        self.serverOnline = data["serverOnline"]
        self.max = data["max"]
        self.towny = data["towny"]
        self.storming = data["storming"]
        self.thundering = data["thundering"]
        self.queue = data["queue"]
