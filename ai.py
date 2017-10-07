from flask import Flask, request
from structs import *
import structs
import math
import json
import numpy
import utils


app = Flask(__name__)


##########################################""""

def print_map(map):
    s = ""
    l = []
    for i in range(40):
        l.append([])
        for j in range(40):
            l[i].append(9)

    for i in range(20):
        for j in range(20):
            if not (map[i][j].Content is None):
                l[map[i][j].X][map[i][j].Y] = map[i][j].Content


    for i in range(40):
        for j in range(40):
            s += str(l[i][j])+" "
        s += "\n"

    return s
################################################"


def move_to_target(pos,target):
    x = pos["X"]
    y = pos["Y"]
    xt = target.X
    yt = target.Y
    if (xt !=  x):
        return Point(int(x + math.copysign(1,xt-x)), int(y) )
    elif yt !=y:
        return Point(int(x),int( y + math.copysign(1,yt-y)))
    else:
        return Point(x,y)


####################################################
def find_resource(map, pos):
    xp = pos["X"]
    yp = pos["Y"]
    resource_position = None
    resource_distance = 1000
    for line in map:
        for tile in line:
            if tile.Content == 4 and Point(tile.X,tile.Y).Distance(Point(xp,yp),Point(tile.X,tile.Y)) <= resource_distance:
                resource_position, resource_distance = Point(tile.X,tile.Y), Point(tile.X,tile.Y).Distance( Point(xp,yp),Point(tile.X,tile.Y))
    if resource_position is not None :
        return resource_position
    else:
        raise Exception("aucune ressource en vue  !")

###################################################""



######################################################


def create_action(action_type, target):
    actionContent = ActionContent(action_type, target.__dict__)
    return json.dumps(actionContent.__dict__)

def create_move_action(target):
    return create_action("MoveAction", target)

def create_attack_action(target):
    return create_action("AttackAction", target)

def create_collect_action(target):
    return create_action("CollectAction", target)

def create_steal_action(target):
    return create_action("StealAction", target)

def create_heal_action():
    return create_action("HealAction", "")

def create_purchase_action(item):
    return create_action("PurchaseAction", item)

def create_upgrade_action(item):
    return create_action("UpgradeAction", item)

def deserialize_map(serialized_map):
    """
    Fonction utilitaire pour comprendre la map
    """
    serialized_map = serialized_map[1:]
    rows = serialized_map.split('[')
    column = rows[0].split('{')
    deserialized_map = [[Tile() for x in range(20)] for y in range(20)]
    for i in range(len(rows) - 1):
        column = rows[i + 1].split('{')

        for j in range(len(column) - 1):
            infos = column[j + 1].split(',')
            end_index = infos[2].find('}')
            content = int(infos[0])
            x = int(infos[1])
            y = int(infos[2][:end_index])
            deserialized_map[i][j] = Tile(content, x, y)

    return deserialized_map

def bot():
    """
    Main de votre bot.
    """
    map_json = request.form["map"]

    # Player info

    encoded_map = map_json.encode()
    map_json = json.loads(encoded_map)
    p = map_json["Player"]
    pos = p["Position"]
    x = pos["X"]
    y = pos["Y"]
    house = p["HouseLocation"]
    player = Player(p["Health"], p["MaxHealth"], Point(x,y),
                    Point(house["X"], house["Y"]), 0,
                    p["CarriedResources"], p["CarryingCapacity"])

    # Map
    serialized_map = map_json["CustomSerializedMap"]
    deserialized_map = deserialize_map(serialized_map)
   # print_map(deserialized_map)
    otherPlayers = []
    #s = print_map(deserialized_map)
    #print(s)
    #print("bonjour " + " " + str(x) + " " + str(y))
    for player_dict in map_json["OtherPlayers"]:
        for player_name in player_dict.keys():
            player_info = player_dict[player_name]
            if player_info == 'notAPlayer':
                continue
            p_pos = player_info["Position"]

            player_info = PlayerInfo(player_info["Health"],
                                     player_info["MaxHealth"],
                                     Point(p_pos["X"], p_pos["Y"]))

            otherPlayers.append({player_name: player_info })

    # return decision

    #case : backpack full
   # if player.CarriedRessources == player.CarryingCapacity:
       # targetpos = Point(house["X"], house["Y"])
        #targetType = 2 #target house
       # print("target house")
    #case: target ressources
    #else:
       # targetpos = find_resource(deserialized_map,pos)
        #targetType = 4 #target resource
        #print("target reouserce")
   # print("qtite transportee :" +str(player.CarriedRessources))


    #met a jour l'estime des ressources totales
    #if x == house["X"] and y == house["Y"]  and player.CarriedRessources == 0 and structs.laststate.lastCarriedRessources !=0:
      #  structs.laststate.estimatedTotalRessources += structs.laststate.lastCarriedRessources


    #print("estimated total ressource :" + str(structs.laststate.estimatedTotalRessources))
    #case : achat d'une upgrade si possible
    #if x == house["X"] and y == house["Y"] and structs.laststate.estimatedTotalRessources == structs.laststate.upgradesPrices[0] and structs.laststate.lastAction != "UpgradeAction":
        #upgrade = structs.laststate.upgradesList[0]
        #del(structs.laststate.upgradesList[0])
        #print("upgrade pruchased : " + upgrade)
        #structs.laststate.estimatedTotalRessources -= structs.laststate.upgradesPrices[0]
        #del(structs.laststate.upgradesPrices[0])
        #structs.laststate.lastAction = "UpgradeAction"

        #structs.laststate.maj(x,y,"UpgradeAction", player.CarriedRessources)
        #return create_upgrade_action(str(upgrade))



    #case : mining
    #if Point(x,y).Distance(Point(x,y),targetpos) <= 1.1 and targetType == 4:
        #structs.laststate.maj(x, y, "CollectAction", player.CarriedRessources)
        #return create_collect_action(targetpos)
   #case : moving toward target
    #else:
        #p = move_to_target(pos, targetpos)
        #print(p)
        #structs.laststate.maj(x, y, "MoveAction", player.CarriedRessources)
        if numpy.rand(1,2)%2==2:
            return create_move_action(Point(0,1))
        else
            return create_move_action(Point(0,-1))
        #return create_move_action(p)

@app.route("/", methods=["POST"])
def reponse():
    """
    Point d'entree appelle par le GameServer
    """
    return bot()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)






