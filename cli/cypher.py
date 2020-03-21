import yaml
import os

type_info = [yaml.safe_load(open("cypher/type/" + t + ".yaml", "r")) for t in ["adept", "explorer", "speaker", "warrior"]]

foci_info = [yaml.safe_load(open(f.path, "r")) for f in os.scandir("cypher/foci")]

flavour_info = [yaml.safe_load(open(f.path, "r")) for f in os.scandir("cypher/flavours")]

#TODO: Make sure all functions convert naming to lower
def get_type_info(ty):
    result = [x for x in type_info if x["name"].lower() == ty.lower()]
    if len(result) == 0:
        return None
    else:
        return result[0]

def get_focus_info(f):
    result = [x for x in foci_info if x["name"].lower() == f.lower()]
    if len(result) == 0:
        return None
    else:
        return result[0]

def get_flavour_info(f):
    result = [x for x in flavour_info if x["name"].lower() == f.lower()]
    if len(result) == 0:
        return None
    else:
        return result[0]

def collate_abilities(ty, focus, flavour = "none"):
    type_data = get_type_info(ty)
    focus_data = get_focus_info(focus)
    flavour_data = {}
    if flavour.lower() != "none":
        flavour_data = get_flavour_info(flavour)
    
    abilities = {}
    for i in range(1, 7):
        abilities[i] = []
        abilities[i] += type_data["abilities"][i]
        abilities[i] += focus_data[i]
        if flavour.lower() != "none":
            abilities[i] += flavour_data[i]
    return abilities
