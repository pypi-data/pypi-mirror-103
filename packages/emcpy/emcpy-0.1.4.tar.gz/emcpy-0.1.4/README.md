# EarthMC Python API


## Installation
Run the following to install:

```python
pip install emcpy
```


## Usage

### Nation
#### A nation on EarthMC towny

```python
from emcpy import Nation

# Define the Nation
# Defining the nation to "" or a nation that does not exist will raise a NationNotFoundException
nation = Nation("name")

# Get the attributes
name = nation.name  # Name
claims = nation.claims  # Amount of claims/plots
king = nation.king  # King of this nation
towns = nation.towns  # List of towns
capital = nation.capital  # Capital of the nation
coords = nation.coords  # Dict of x and z
residents = nation.residents  # List of residents
```

### Town
#### A town on EarthMC towny

```python
from emcpy import Town

# Define the Town
# Defining the town to "" or a town that does not exist will raise a TownNotFoundException
town = Town("name")

# Get the attributes
name = town.name  # Name
claims = town.claims  # Amount of claims/plots
mayor = town.mayor  # Mayor of the town
nation = town.nation  # Nation that the town is part of
flags = town.flags  # Dict of flags
residents = town.residents  # List of residents
nation_residents = town.nation_residents  # List of nation residents
```

### Resident
#### A player in a town

```python
from emcpy import Resident

# Define the resident
# Defining the resident to "" or a resident that does not exist will raise a ResidentNotFoundException
resident = Resident("name")

# Get the attributes
name = resident.name  # Name
nation = resident.nation  # Nation that the resident is part of
town = resident.town  # Town that the resident is part of
rank = resident.rank  # Rank in the town/nation
```

### Online Player
#### A player online on the server
```python
from emcpy import Online

# Define the player
# Defining the player to "",  a player that does not exist or a player that is offline will raise a OnlinePlayerNotFoundException
online = Online("name")

# Get the attributes
name = online.name # Name
town = online.town # Town that the player is part of
rank = online.rank # Rank in the town/nation
nation = online.nation # Nation that the player is part of
nickname = online.nick # Nickname of the player
isUnderground = online.isUnderground # Is the player visible on the map
coords = online.coords # Dict of {'x', 'y', 'z'}. If isUnderground is True, coords = 0, 64, 0
```

### Server
#### Info on the server
```python
from emcpy import Server

server = Server()

# Get the attributes
isOnline = server.serverOnline # Is the server online
onlinePlayer = server.online # Amount of online players
serverMax = server.max # Max amount of players that can be online on the server
queue = server.queue # Amount of players in the queue
towny = server.towny # Amount of players on the Towny server 
thundering = server.thundering # Is it thundering
storming = server.storming # Is it storming
```

## Useful methods
```python
from methods import getAllOnline, getAllTowns, getAllResidents, getAllNations, getPlayerFace, getOnlineKings, getTownless

# getAllResidents gets all the residents from every town on the server
allResidents = getAllResidents()

# getAllOnline gets all the online players on the towny server
allOnline = getAllOnline()

# getAllTowns gets all the towns on the server
allTowns = getAllTowns()

# getAllNations get all the nations on the server
allNations = getAllNations()

# getPlayerFace gets the face of the player
playerFace = getPlayerFace("name")

# getOnlineKings gets all the nation leaders currently online
kings = getOnlineKings()

# getTownless gets all the currently townless players online
townless = getTownless()
```

## Credits
### Credits to Warriorrrr and Owen77Stubbs for the data links