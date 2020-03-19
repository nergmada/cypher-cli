import re
import yaml
from collections import OrderedDict

raw_abilities = open("cypher-raw/abilities.txt")

with open('cypher/abilities.yaml', 'w') as outfile:
    for line in raw_abilities:
        result = re.match(r"([?',\w\s-]*)(?:\((.*)\))?: (.*)\. ([;\w\s,]+)\.", line)
        cost = "none"
        if result.group(2) is not None:
            cost = result.group(2)
        outfile.write("- name: " + result.group(1) + "\n")
        outfile.write("  activation: " + result.group(4) + "\n")
        outfile.write("  cost: " + cost + "\n")
        outfile.write("  description: " + result.group(3) + "\n")
        

