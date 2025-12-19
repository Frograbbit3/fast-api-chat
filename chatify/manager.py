from . import common, config
import pickle
import os, time, random, json
from .shared import dprint
class Manager:
    def __init__(self, starting_lobbies):
        self._loaded_lobbies = []
        self.lobbies = [None for _ in range(starting_lobbies)]
        self.seen_lobbies = []
        self.lobby_metadata = {}
        self.lobby_count = len(self.lobbies)
        self.blank_lobby = common.Lobby()
        self.blank_lobby.password = random.randint(1,99999999)
        self.blank_lobby.mode = common.modes.private
        self.blank_lobby.name = "[RESTRICTED LOBBY]"
        self.blank_lobby.real = False
        dprint("Loaded lobbies / lobby manager")
        self.scan_lobbies("default-lobbies")
     
    
    def scan_lobbies(self, folder):
        for filename in os.listdir(folder):
            filepath = os.path.join(folder, filename)
            if os.path.isfile(filepath):
                name = os.path.splitext(filename)[0]
                ext = os.path.splitext(filename)[1]
                if ext == ".json":
                    dprint("Found lobby #", name, "loading..")
                    lobbyID = int(name)
                    lobby = self.get_lobby(lobbyID)
                    with open(filepath, "r") as m:
                        k = m.read()
                        l = json.loads(k)
                        if "password" in l["config"]:
                            lobby.password = l["config"]["password"]
                        lobby.load_json(k)
                        self.seen_lobbies.append(lobbyID)
                        self.return_lobby(lobbyID, lobby)
                

    def save_lobby(self, lobby_num=-1, unload=True):
        if lobby_num < 0:
            for i, lobby in enumerate(self.lobbies.copy()):
                if lobby == None or not i in self._loaded_lobbies:
                    continue
                with open(f"saves/chat{i}.lobby", "wb") as file:
                    file.write(pickle.dumps(lobby))
                    if i in self._loaded_lobbies and unload:
                        self._loaded_lobbies.remove(i)
                        self.lobbies[self.lobbies.index(lobby)] = None
                        dprint(f"Unloaded lobby {i}")
        elif lobby_num in self._loaded_lobbies:
                if self.lobbies[lobby_num] == None:
                    return
                
                if self.lobbies[lobby_num].save == False:
                    dprint(f"Lobby {lobby_num} is not set to save, skipping save.")
                    return
                with open(f"saves/chat{lobby_num}.lobby", "wb") as file:
                    dprint("Saved", lobby_num)
                    file.write(pickle.dumps(self.lobbies[lobby_num]))
                if lobby_num in self._loaded_lobbies and unload:
                    self._loaded_lobbies.remove(lobby_num)
                    self.lobbies[lobby_num] = None
                    dprint(f"Unloaded lobby {lobby_num}")
            
    def load_lobby(self, lobby_num=-1):
        dprint("Loading lobby", lobby_num)
        
        if lobby_num < 0:
            for i, lobby in enumerate(self.lobbies.copy()):
                if os.path.exists(f"saves/chat{i}.lobby"):
                    with open(f"saves/chat{i}.lobby", "rb") as file:
                        self.lobbies[i] = pickle.load(file)
                        self._loaded_lobbies.append(i)
                        self.lobbies[i].last_read = time.time()
                else:
                    self.lobbies[i] = common.Lobby()
                    self.lobbies[i].last_read = time.time()
                    self.save_lobby(i)
        elif not lobby_num in self._loaded_lobbies:
                if os.path.exists(f"saves/chat{lobby_num}.lobby"):
                    with open(f"saves/chat{lobby_num}.lobby", "rb") as file:
                        self.lobbies[lobby_num] = pickle.load(file)
                        self._loaded_lobbies.append(lobby_num)
                        self.lobbies[lobby_num].last_read = time.time()
                else:
                    self.lobbies[lobby_num] = common.Lobby()
                    self.lobbies[lobby_num].last_read = time.time()
                    self.save_lobby(lobby_num)
    def is_loaded(self, lobby_num):
        if lobby_num in self._loaded_lobbies:
            if not isinstance(self.lobbies[lobby_num],int):
                return True
        return False

    def create_lobby(self, data):
        for i in range(self.lobby_count):
            self.load_lobby(i)
            lobby = self.lobbies[i]
            if lobby.real:
                continue
            self.lobbies[i] = data
            self.save_lobby(i, unload=False)
            self.lobby_metadata[i] = data.config()
            self.load_lobby(i)
            return i
        
        return -1


    def is_valid(self, num):
        return (num > -1 and num < self.lobby_count)
    
    def get_lobby(self, lobby_num):
        if self.is_valid(lobby_num):
            self.load_lobby(lobby_num)
            if self.lobbies[lobby_num] == None:
                if lobby_num in self._loaded_lobbies:
                    self._loaded_lobbies.remove(lobby_num)
                    self.load_lobby(lobby_num)
            data = self.lobbies[lobby_num]
            data.last_read=time.time()
            return data
        else:
            return self.blank_lobby

    def get_lobby_config(self, lobby_id):
        #dprint(self.lobby_metadata)
        if self.is_valid(lobby_id):
            if self.lobby_metadata.get(lobby_id) is None:
                lobby = self.get_lobby(lobby_id)
                if lobby:
                    conf = lobby.config()
                    if self.lobby_metadata.get(lobby_id, None) != conf:
                        self.lobby_metadata[lobby_id] = lobby.config()
                    return conf
                return None
            else:
                return self.lobby_metadata[lobby_id]
        else:
            return self.blank_lobby.config()

    def return_lobby(self, lobby_num, lobby_data : common.Lobby):
        self.load_lobby(lobby_num)
        self.lobbies[lobby_num] = lobby_data
        self.lobby_metadata[lobby_num] = lobby_data.config()
        self.save_lobby(lobby_num, unload=False)
        
    def run_tick(self):
        for i, lobby in enumerate(self.lobbies):
            if lobby==None and i in self._loaded_lobbies:
                self._loaded_lobbies.remove(i)
                dprint(f"Correctly fixed unloading of lobby {i}")
            elif not lobby == None and not i in self._loaded_lobbies:
                self._loaded_lobbies.append(i)
                dprint(f"Correctly fixed loading of lobby {i}")
            if not lobby == None and i in self._loaded_lobbies:
                if hasattr(lobby, "last_read"):
                    if time.time() - lobby.last_read > 5:
                        self.save_lobby(i)    
    def tick(self):
        while True:
            self.run_tick()
            time.sleep(1)