import yaml

#abilities = ["Telepathic", "Distortion", "Erase Memories", "Far Step", "Hedge Magic", "Magic Training", "Onslaught", "Push", "Resonance Field", "Scan", "Shatter", "Ward"]

#abilities = ["Driver","Driving on the Edge","Block","Danger Sense","Decipher","Endurance","Find the Way","Fleet of Foot","Improved Edge","Knowledge Skills","Muscles of Iron","No Need for Weapons","Physical Skills","Practiced in Armor","Practiced With All Weapons","Surging Confidence","Trained Without Armor"]

#abilities = ["Improved Recovery","Push on Through","Bash","Combat Prowess","Control the Field","Improved Edge","No Need for Weapons","Overwatch","Physical Skills","Practiced in Armor","Quick Throw","Swipe","Trained Without Armor"]


abilities = ["Anecdote", "Babel", "Demeanor of Command", "Encouragement", "Enthrall", "Erase Memories", "Fast Talk", "Inspire Aggression", "Interaction Skills", "Practiced With Medium Weapons", "Spin Identity", "Terrifying Presence", "Understanding", "Lab Analysis", "Knowledge Skills", "Datajack", "Hacker", "Machine Interface", "Scramble Machine", "Tech Skills", "Tinker"]


output = "### Abilities"
for a in yaml.safe_load(open("cypher/abilities.yaml")): 
    if a["name"] in abilities:
        output += "\n\n#### " + a["name"]
        output += "\n\n**Type**: " + a["activation"]
        output += "\n\n**Cost**: " + a["cost"]
        output += "\n\n" + a["description"]
print(output)