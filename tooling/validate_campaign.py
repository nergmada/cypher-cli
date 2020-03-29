campaign_name = "cascada"

import os
import yaml

def get_expected_locales(location):
    adjacent = []
    for nxt in location["adjacent"]:
        region_and_setting = nxt.split("/")
        if len(region_and_setting) == 2:
            adjacent.append(nxt)
        else:
            adjacent.append(location["region"] + "/" + nxt)
    return adjacent



campaign_path = "campaigns/" + campaign_name

def validate_npc(npc_name):
    print("Validating " + npc_name)
    
    data = yaml.safe_load(open(campaign_path + "/npcs/" + npc_name + ".yaml"))
    if data is None:
        print("ERR: could not load YAML for " + npc_name)
        return False
    keys = ['level', 'health', 'armour', 'damage', 'modifiers', 'description']
    for key in keys:
        if key not in data.keys():
            print("ERR: NPC " + npc_name + " does not have key " + key)
            return False
        elif type(data[key]) is not str and type(data[key]) is not int:
            print("ERR: NPC " + npc_name + " key " + key + " is not type int or str")
            return False
    if data["identifier"] != npc_name:
        print("ERR: NPC " + npc_name + " has different identifier " + data["identifier"])
        return False


def validate_location_data(location, file_name):
    print("Validating " + file_name)
    keys = ['name', 'lighting','gravity', 'scale', 'elemental', 'description']
    if "region" not in location.keys() or "setting" not in location.keys():
        print("The region or setting key is not found in " + file_name)
    location_name = location["region"] + "/" + location["setting"]
    if location["setting"] + ".yaml" != file_name:
        print("The location " + location_name + " does not have a setting that matches file name " + file_name)
    # Check data keys exists
    for key in keys:
        if key not in location.keys():
            print("ERR: Location " + location_name + " missing key " + key)
            return False
        elif type(location[key]) is not str:
            # check keys are correct type
            print("ERR: Location " + location_name + " wrong type for key " + key)
            return False
    # check assets exist
    if "assets" not in location.keys():
        print("ERR: Location " + location_name + " does not have an assets array")
        return False
    else:
        # check the corresponding file exists
        for asset in location["assets"]:
            if not os.path.isfile(campaign_path + "/assets/" + asset):
                print("ERR: Asset " + asset + " for location " + location_name + " not found")
                return False
    if "npcs" not in location.keys():
        print("ERR: Location " + location_name + " does not have an NPC array")
        return False
    else:
        for npc in location["npcs"]:
            if not os.path.isfile(campaign_path + "/npcs/" + npc + ".yaml"):
                print("ERR: NPC " + npc + " in location " + location_name + " not found")
                continue
            validate_npc(npc)

regions = [x.name for x in os.scandir(campaign_path + "/locations")]

existing_locales = []
expected_locales = {}


for region in regions:
    region_path = campaign_path + "/locations/" + region
    settings = [(x.name, yaml.safe_load(open(x.path))) for x in os.scandir(region_path)]
    for setting in settings:
        existing_locales.append(region + "/" + setting[0])
        expected_locales[region + "/" + setting[0]] = get_expected_locales(setting[1])
        validate_location_data(setting[1], setting[0])

for from_locale in expected_locales.keys():
    for to_locale in expected_locales[from_locale]:
        if to_locale +".yaml" not in existing_locales:
            print("The location " + to_locale + " does not appear in existing locations but was referenced by " + from_locale)