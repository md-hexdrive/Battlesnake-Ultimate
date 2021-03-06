import os
import random
import json

import cherrypy
import behaviour
import constants

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""


class Battlesnake(object):
    

    default_config = {
        "apiversion": "1",
        "author": "",  # TODO: Your Battlesnake Username
        #"color": "#279ce4",  # TODO: Personalize
        #"color": "#596b75",  # TODO: Personalize
        #"color": "#272f33",  # TODO: Personalize
        "color": "#3a464d",  # TODO: Personalize
        "head": "shac-tiger-king",  # TODO: Personalize
        "tail": "bolt",  # TODO: Personalize
    }
    custom_config=None

    def __init__(self, custom_config=None):
        self.custom_config = custom_config

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        # This function is called when you register your Battlesnake on play.battlesnake.com
        # It controls your Battlesnake appearance and author permissions.
        # TIP: If you open your Battlesnake URL in browser you should see this data


        if self.custom_config != None:
            return self.custom_config
        return self.default_config

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        # TODO: Use this function to decide how your snake is going to look on the board.
        data = cherrypy.request.json

        print("START")
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".
        # TODO: Use the information in cherrypy.request.json to decide your next move.
        data = cherrypy.request.json

        #         # Choose a random direction to move in
        #         possible_moves = ["up", "down", "left", "right"]
        #         move = random.choice(possible_moves)
        move = behaviour.snake_behaviour(data)

        print(f"MOVE: {move}")
        return {"move": move}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json
        me = data["you"]
        if me in data["board"]["snakes"]:
            print("you won!!")
        else:
            print("you lost")

        print("END")
        return "ok"


if __name__ == "__main__":
    custom_config = None

    if os.path.exists(constants.appearance_file):
        with open(constants.appearance_file, "r") as appearance:
            print("Loading snake appearance configuration")
            custom_config = json.load(appearance)
            print("Appearance", custom_config)
    server = Battlesnake(custom_config)
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update({
        "server.socket_port":
        int(os.environ.get("PORT", "8080")),
    })
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
