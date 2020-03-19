from flask import Flask
import markdown2

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

@app.route("/subconscious/<player>")
def get_info(player):
    f = open("subconscious/" + player + ".md", "r")
    return stylesheet + markdown2.markdown(f.read()) + """
        <script>
        setTimeout(function() {
            window.location.reload(true)
        }, 30000);
        </script>
    """