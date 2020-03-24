from flask import Flask, send_file
import mistune
import os
import yaml
from cli.ability_search import ability_search, get_all_abilities
from cli.logger import Logger

from web.abilities import generate_ability, generate_abilities_list
from web.player import generate_profile, generate_private_info
from web.location import generate_location, generate_gallery

from random import randrange

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


def player_menu(logs, player_name):
    return f"""
        <nav>
            <div class="nav-wrapper">
            <ul id="nav-mobile" class="right hide-on-med-and-down">
                <li><a href="/{logs}/status" target="_blank">Team Status</a></li>
                <li><a href="/{logs}/{player_name}" target="_blank">Your status</a></li>
                <li><a href="/roll/d20/{player_name}" target="_blank">Roll D20</a></li>
                <li><a href="/roll/d6/{player_name}" target="_blank">Roll D6</a></li>
                <li><a href="/abilities" target="_blank">Full Abilities List</a></li>
            </ul>
            </div>
        </nav>
    """

def div(inner, cls):
    return "<div class='" + cls + "'>" + inner + "</div>" 

def page(inner):
    return div(inner, "container")

def player_dashboard(players):
    colours = ["deep-purple lighten-3", "indigo lighten-3", "blue lighten-3", "red lighten-3"]
    result = ""
    i = 0
    for player in players:
        html = md_to_html([generate_profile(player, 3)])
        result += div(html, "card col s12 m6 " + colours[i]) + "\n\n"
        i += 1
        i = i % 4
    return div(result, "row")

def md_to_html(mds):
    result = stylesheet
    for md in mds:
        result += mistune.markdown(md)
    return result

def refresh_script():
    return """
        <script>
        setTimeout(function() {
            window.location.reload(true)
        }, 10000);
        </script>
    """

@app.route("/<logs>/status")
def get_status(logs):
    logger = Logger("logs/" + logs, read_only=True)
    if not logger.has_main_file():
        return md_to_html(["log not found"])
    if not logger.has_players():
        return md_to_htm(["no players registered"])
    players = logger.get_players()

    rendered_output = player_dashboard(players)

    log = logger.read_log()
    output = "# Logs:\n\n"
    for line in log:
        output += "\\" + line + "\n\n"
    return page(rendered_output + div(md_to_html([output]), "deep-orange lighten-4")) + refresh_script()
    

@app.route("/<logs>/<player>")
def get_info(logs, player):
    logger = Logger("logs/" + logs, read_only=True)
    if not logger.has_main_file():
        return md_to_html(["log not found"])
    if not logger.has_players():
        return md_to_htm(["no players registered"])
    player = logger.load_player_data(player)
    if player is None:
        return md_to_htm(["Player not found"])
    
    result = player_menu(logs, player["player_name"])
    result += page(
        md_to_html([generate_profile(player), generate_private_info(player), generate_location(player, logger)]) + generate_gallery(player, logger)        
        )
    result += refresh_script()
    return result

#TODO: Add a team endpoint



@app.route("/abilities/<ability>")
def get_ability(ability):
    data = ability_search(ability)
    if len(data) == 0:
        return md_to_html(["Not Found"])
    else:
        return page(md_to_html([generate_ability(data[0])]))

@app.route("/abilities")
def get_abilities():
    abilities = get_all_abilities()
    return page(md_to_html([generate_abilities_list(abilities)]))


@app.route("/roll/d20/<player>")
def roll_d20(player):
    result = randrange(1, 21)
    print(player + " rolled a " + str(result) + " on a d20")
    return page(md_to_html(["# You rolled a " + str(result) + " on a d20"]))

@app.route("/roll/d6/<player>")
def roll_d6(player):
    result = randrange(1, 7)
    print(player + " rolled a " + str(result) + " on a d6")
    return page(md_to_html(["# You rolled a " + str(result) + " on a d6"]))

@app.route("/assets/<campaign>/<id>")
def get_asset(campaign, id):
    return send_file(f"campaigns/{campaign}/assets/{id}")

