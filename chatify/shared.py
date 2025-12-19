from . import config
import humanfriendly
import json
import os
config.init()

chatLogs = []
online_users = []
logins = {}
if os.path.exists("logins.json"):
    logins = json.load(open("logins.json","r"))
lobbyCount = int(config.configuration["GENERAL"]["lobby-count"])
_SYSHASH = "f210e7697846313bbae2dc6ffc50dde498f06f1695f4f6cbbf589fcdda9569fa"
lobby_manager= None
ver = "v1.9.2s"
debug = config.debug
key_string = config.configuration['SECURITY']['encryption-key']
iv = config.configuration['SECURITY']['encryption-iv']
max_size = humanfriendly.parse_size(config.configuration['GENERAL']['max-size'])
#_SYSHASH = security.hash("systemomg", times=100000)

def init():
    global lobby_manager
    from . import manager
    if not os.path.exists("default-lobbies"):
        os.mkdir("default-lobbies")
    lobby_manager = manager.Manager(lobbyCount)

def manager():
    global lobby_manager
    return lobby_manager

def dprint(*args):
    args = [str(arg) for arg in args]
    if debug:
        msg = " ".join(args)
        print("[DEBUG]:", msg)