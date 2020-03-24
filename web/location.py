def generate_location(player, logger):
    location = logger.load_location_data(player["location"]["region"], player["location"]["setting"])
    if "npc_data" not in location.keys():
        return ""
    result = "## NPCs At Location\n"
    for npc in location["npc_data"].values():
        if npc["known"]:
            result += "### " + npc["name"] + "\n"
            result += "_Health: " + str(npc["health"]) + "_\n\n"
            result += "_Armour: " + str(npc["armour"]) + "_\n\n"
            result += "_Level: " + str(npc["level"]) + "_\n\n"
            if "modifiers_visible" in npc.keys():
                result += "**Modifiers: " + npc["modifiers"] + "**\n\n"
            if "desription_visible" in npc.keys():
                result += "Description: \n\n" + npc["description"] + "\n\n"
    return result

def generate_gallery(player, logger):
    location = logger.load_location_data(player["location"]["region"], player["location"]["setting"])
    result = ""
    if "assets" in location.keys():
        for asset in location["assets"]:
            result += f"<img class='responsive-img' src='/assets/{logger.get_campaign()}/{asset}'>\n"
    return result