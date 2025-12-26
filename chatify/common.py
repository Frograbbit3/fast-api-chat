import random
import json
import time
from . import security
from .shared import dprint
class LobbyModes:
    def __init__(self):
        self.public = "public"
        self.private = "private"
        self.unlisted = "unlisted"
        self.silent = "silent"
        self.text = "text"

class Perms:
    def __init__(self):
        self.SEND_FILES = 1
        self.SEND_MESSAGES = 2
        self.SEND_REACTIONS = 3
        self.CHANGE_MESSAGES = 4
        self.DELETE_MESSAGES = 5
        self.MANAGE_CHANNELS = 6
modes = LobbyModes()
perms = Perms()
class Channel:
    def __init__(self, name, type=None):
        self.name = self.channelify(name)
        self.type = type or modes.text
        self.logs = []
        self.id = random.randint(9**31, 10**31)
        self.logs_json = json.dumps(self.logs)
        pass
    def channelify(self, txt):
        return "#"+txt.lower().replace(" ", "-")
    def messages(self):
        return self.logs
    def get_json(self):
        return {
            "name" : self.name,
            "type" : self.type,
            "id" : self.id,
            "logs" : self.logs
        }
    def load_json(self, js):
        self.name = js["name"]
        self.type = js["type"]
        self.id = js["id"]
        self.logs = js["logs"]

class Role:
    def __init__(self, name, color, perms, default=False):
        self.name = name
        self.color = color
        self.perms = perms
        pass
    def get_json(self):
        return {
            "name" : self.name,
            "color": self.color,
            "perms": self.perms
        }
    def load_json(self, js):
        self.name = js["name"]
        self.color = js["color"]
        self.perms = js["perms"]
class Lobby:
    def __init__(self, id=None):
        self.id = id or random.randint(9**31,10**31)
        self.users = [self.create_user("System")]
        self.admins = ["System"]
        self.mode = modes.public
        self.user_count = 1
        self.admin_count = 1
        self.channels = [Channel("general")]
        self.name = "Lobby %s"
        self.tbl = {}
        self.roles = [Role("Testing role 1", "#FF0000",[perms.SEND_MESSAGES,perms.SEND_FILES,perms.SEND_REACTIONS])]
        self.last_read = time.time()
        self.password = ""
        self.description = ""
        self.real = False
        self.save = True
    def refresh_user_count(self):
        self.user_count = len(self.users)
        self.admin_count = len(self.admins)
    
    def config(self):
        roles = []
        for rol in self.roles:
            roles.append(rol.get_json())
        return {
            "name" : self.name,
            "users" : self.users,
            "admins" : self.admins,
            "mode" : self.mode,
            "user_count" : self.user_count,
            "admin_count" : self.admin_count,
            "roles" : roles,
            "description" : self.description,
            "real" : self.real,
            "save" : self.save,
        }
    
    def get_json(self, isString=True):
        config =self.config()
        channels = []
        for ch in self.channels:
            channels.append(ch.get_json())
        roles = []
        for rl in self.roles:
            roles.append(rl.get_json())
        config["roles"] = roles
        self.tbl = {"config" : config, "channels" : channels}
       # dprint(self.tbl)
       # exit()
        if isString:
            return self.tbl
        else:
            return json.dumps(self.tbl)
        
    def load_json(self, js):
        loaded = json.loads(js)
        self.name = loaded["config"]["name"]
        self.users = loaded["config"]["users"]
        self.admins = loaded["config"]["admins"]
        self.mode = loaded["config"]["mode"]
        self.user_count = loaded["config"]["user_count"]
        self.admin_count = loaded["config"]["admin_count"]
        self.description = loaded["config"]["description"]
        self.real = loaded["config"]["real"]
        self.save = loaded["config"]["save"]
        self.roles.clear()
        for role in loaded["config"]["roles"]:
            newRole = Role("","","",False)
            newRole.load_json(role)
            self.roles.append(newRole)
        self.channels.clear()
        for channel in loaded["channels"]:
            newChannel = Channel("[Loading]")
            newChannel.load_json(channel)
            self.channels.append(newChannel)
    def create_user(self, username):
        return {
            "name" : username,
            "roles" : []
        }
    def add_user(self, username):
        profile = self.create_user(username)
        if profile not in self.users:
            self.users.append(self.create_user(username))
            self.refresh_user_count()
    def is_user(self, username):
        for user in self.users:
            if username == user["name"] or self.mode == modes.public:
                return True
        return False
    #def remove_user


def create_user(username, password, admin=False):
    return {
        "token": security.hash(security.hash(username) + security.hash(password)),
        "admin": admin,
        "profile_photo": "/static/default.jpg",
        "name": username, 
    }

dprint("Loaded common")