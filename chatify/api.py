from . import shared, config, security, data, common
from .shared import chatLogs, logins, _SYSHASH, manager, dprint
import json
import requests, time

lobby_manager = None
currentind=0
session = requests.Session()

dprint("Loaded API")
def send_message(lobby, channel, message, username="System", full=False, http=False, allowedUsers=[]):
    table = {
        "lobby":lobby,
        "message":message,
        "user":username,
        "tp": "text",
        "full" : full,
        "allowed_users" : allowedUsers,
        "channel" : channel,
        "code" : _SYSHASH,
    }
    if message == None or message == "":
        return
    if http:
        session.post("http://localhost:5000/send", json=table)
    else:
        set_lobby(int(lobby), table)
        data.save_messages(fancy=True, lobby=lobby)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
def set_lobby(lobby, req, encrypt=True):
    global currentind, chatLogs, logins, lobby_manager
    currentind += 1

    lb = lobby_manager.get_lobby(lobby)

    req["profile_photo"] = logins.get(req["user"], {}).get("profile_photo")
    if encrypt:
        req["message"] = security.encrypt(req["message"])
    # Clean up request
    req.pop("code", None)
    req.pop("lobby", None)

    try:
        if len(req["allowed_users"]) < 1:
            req.pop("allowed_users", None)
    except Exception:
        req["allowed_users"] = []

    selectedChannel = req.get("channel", -1)
    logs = lb.channels[selectedChannel].logs
    logs.append(req)
    lb.channels[selectedChannel].logs_json = json.dumps(logs)

    lobby_manager.return_lobby(lobby, lb)

def get_lobby(lobby):
    global chatLogs
    tmp = []
    if lobby < 0:
        for i in shared.lobbyCount:
            l = lobby_manager.get_lobby(i)
            tmp.append(l.config())
        return tmp
    else:
        try:
            return lobby_manager.get_lobby(lobby).config()
        except Exception as e:
            return {"status": "error", "message": str(e)}
    return {"status": "success", "data": tmp}
def is_admin(user, lobby):
    lobby = int(lobby)
    if lobby < 0:
        # Make sure user exists and has 'admin' key
        if user not in logins or "admin" not in logins[user]:
            return False
        return bool(logins[user]["admin"])

    lobby = lobby_manager.get_lobby(lobby)

    if user in lobby.admins:
        return True

    if user in logins and "admin" in logins[user]:
        return bool(logins[user]["admin"])

    return False


def is_joined(user, lobby):
    for usr in lobby.users:
        if type(usr) == str:
            continue
        if usr["name"] == user:
            return True
    return False

def get_allowed_lobbies(user):
    global logins, chatLogs, lobby_manager
    profile = logins[user]
    lobb = []
    for i in range(shared.lobbyCount):
        lobby = lobby_manager.get_lobby(i)
        if (is_joined(user, lobby)) or (lobby.mode != common.modes.private) or (lobby.user_count < 1):
            lobb.append(i)
    if bool(profile["admin"]):
        lobb = list(range(len(shared.lobbyCount)))
    return lobb

def repair(p, lobby):
    m = p
    for i,part in enumerate(p):
        if type(part) == str:
            m[i]= lobby.create_user(part)
    return m

def get_message(lobby, channel, ID):
    l = lobby_manager.get_lobby(lobby)
    if l:
        chan = l.channels[channel]
        if chan:
            return chan.logs[ID]
    return None

def init():
    data.load_messages()
    security.init(config.configuration['SECURITY']['encryption-key'], config.configuration['SECURITY']['encryption-iv'])