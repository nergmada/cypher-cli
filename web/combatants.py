def generate_npc_profiles(player, logger):
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
            result += "**Modifiers: " + npc["modifiers"] + "**\n\n"
            result += "Description: \n\n" + npc["description"] + "\n\n"
    return result
