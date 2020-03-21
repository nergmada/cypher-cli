def generate_ability(ability):
    result = "# " + ability["name"] + "\n"
    result += "_Activation: " + ability["activation"] +"_\n\n"
    result += "**Cost: " + ability["cost"] +"**\n\n"
    result += ability["description"]
    return result

def generate_ability_link(ability):
    return "[" + ability + "](/abilities/" + ability.replace(" ", "_") + ")\n\n"    

def generate_abilities_list(abilities):
    result = ""
    for ability in abilities:
        result += generate_ability_link(ability)
    return result

def generate_level_list(abilities):
    result = ""
    for i in range(1, 7):
        if i in abilities.keys():
            result += "## Level " + str(i) + "\n\n"
            result += generate_abilities_list(abilities[i])
    return result