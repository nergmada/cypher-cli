from cli.markdown.abilities import generate_level_list

def generate_stats(stats, pool):
    result = ""
    result += "**Might**: " + str(stats["might"]) + " (" + str(pool["might"]) + ") | "
    result += "**Speed**: " + str(stats["speed"]) + " (" + str(pool["speed"]) + ") | "
    result += "**Intellect**: " + str(stats["intellect"]) + " (" + str(pool["intellect"]) + ")"
    return result

def generate_bio(t, f, d):
    result = "_"
    result += "Type: " + t + " | "
    result += "Focus: " + f + " | "
    result += "Descriptor: " + d + "_"
    return result



def new_line(txt):
    return txt + "\n\n"

def generate_profile(profile):
    result = "# " + profile["identifier"] + " (XP: " + str(profile["xp"]) + ")"
    result = new_line(result)
    result += generate_bio(profile["type"], profile["focus"], profile["descriptor"])
    result = new_line(result)
    result += generate_stats(profile["stats"], profile["pool"])
    result = new_line(result)
    result += generate_level_list(profile["abilities"])
    return result

def generate_private_info(profile):
    result = "## Description"
    result = new_line(result)
    result += profile["description"]
    result = new_line(result)
    result += "## Updates"
    result = new_line(result)
    if "live" in profile.keys():
        for update in profile["live"]:
            result += "### " + update["name"]
            result = new_line(result)
            result += update["info"]
            result = new_line(result)
    return result