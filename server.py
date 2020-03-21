from flask import Flask
import markdown2
from cli.ability_search import ability_search, get_all_abilities
from cli.markdown.abilities import generate_ability, generate_abilities_list

app = Flask(__name__)

#@app.route("/message/<sender>/<receiver>")
#def message(sender, receiver):
#    return sender + " sent a message to " + receiver
#
#@app.route("/update/<player>")
#def get_update(player):
#    return "player has no new info" 

stylesheet = """
<!--Import Google Icon Font-->
<link href="http://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
<!--Import materialize.css-->
<!-- Compiled and minified CSS -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.8/css/materialize.min.css">
  
"""

def md_to_html(mds):
    result = stylesheet
    for md in mds:
        result += markdown2.markdown(md)
    return result

def refresh_script():
    return """
        <script>
        setTimeout(function() {
            window.location.reload(true)
        }, 30000);
        </script>
    """

@app.route("/subconscious/<player>")
def get_info(player):
    f = open("subconscious/" + player.lower() + "/shared.md", "r")
    p = open("subconscious/" + player.lower() + "/private.md", "r")
    return md_to_html([f.read(), p.read()]) + refresh_script()

#TODO: Add a team endpoint


@app.route("/abilities/<ability>")
def get_ability(ability):
    data = ability_search(ability)
    if len(data) == 0:
        return md_to_html(["Not Found"])
    else:
        return md_to_html([generate_ability(data[0])])

@app.route("/abilities")
def get_abilities():
    abilities = get_all_abilities()
    return md_to_html([generate_abilities_list(abilities)])