def generate_ability(ability, drop_header=1):
    result = ("#" * drop_header) + " " + ability["name"] + "\n"
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

def generate_level_list(abilities, drop_header=2):
    result = ""
    for i in range(1, 7):
        if i in abilities.keys():
            result += ("#" * drop_header) + " Level " + str(i) + "\n\n"
            result += generate_abilities_list(abilities[i])
    return result