from json import JSONDecodeError
from requests import get

# Players


def resident_data(name):
    url = f"http://earthmc-api.herokuapp.com/residents/{name}"
    r = get(url)
    data = r.json()
    return data


def townless():
    url = f"http://earthmc-api.herokuapp.com/townlessplayers"
    r = get(url)
    data = r.json()
    return data


def online_player(name):
    url = f"http://earthmc-api.herokuapp.com/onlineplayers/{name}"
    r = get(url)
    try:
        data = r.json()
    except JSONDecodeError:
        data = "That player is not online or does not exist!"
    return data

# Towns


def town_data(name):
    url = f"http://earthmc-api.herokuapp.com/towns/{name}"
    r = get(url)
    data = r.json()
    return data


# Nations


def nation_data(name):
    url = f"http://earthmc-api.herokuapp.com/nations/{name}"
    r = get(url)
    try:
        data = r.json()
    except JSONDecodeError:
        data = "That nation does not exist!"
    return data


# Server


def server_data():
    url = "http://earthmc-api.herokuapp.com/serverinfo/"
    r = get(url)
    data = r.json
    return data
