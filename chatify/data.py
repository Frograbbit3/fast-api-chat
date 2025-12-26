from PIL import Image
from io import BytesIO
import base64
import os
import json
from . import security as secure
from . import config
from .shared import logins
lobby_manager = None
config.init()
lobbyCount = int(config.configuration["GENERAL"]["lobby-count"])
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__)) 
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..")) 

def resizeb64(image_data, isBase64=True, size=(0,0), user=""):
    try:
        if not isBase64:
            img = Image.open(image_data) # Remove the data URI prefix if included
        else:
            if image_data.startswith("data:"):
                image_data = image_data.split(",")[1]
            img = Image.open(BytesIO(base64.b64decode(image_data)))
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        if size[0] > 0:
            img = img.resize(size)
        BytesIO()
        fileName= str(secure.hash(image_data)) + ".jpg"
        if user != "":
            if not os.path.exists(os.path.join(BASE_DIR, "static", "uploads", user)):
                os.mkdir(os.path.join(BASE_DIR, "static", "uploads", user))
            img.save(os.path.join(BASE_DIR, "static", "uploads", user, fileName), format="JPEG")
            return f"/static/uploads/{user}/{fileName}"
        else:
            img.save(os.path.join(BASE_DIR, "static", "uploads", fileName), format="JPEG")
            return f"/static/uploads/{fileName}"
    except Exception as e:
        print(f"Error: {e}. Saving raw file")
        nm = secure.hash(image_data)
        saveb64(image_data,  f"{nm}.jpg")
        if user != "":
            if not os.path.exists(os.path.join(BASE_DIR, "static", "uploads", user)):
                os.mkdir(os.path.join(BASE_DIR, "static", "uploads", user))
            return f"/static/uploads/{user}/{nm}.jpg"
        else:
            return f"/static/uploads/{nm}.jpg"
    
    
def saveb64(b64, name, user=""):
    try:        
        if b64.startswith("data:"):
            b64 = b64.split(",")[1]
        if user != "":
            if not os.path.exists(os.path.join(BASE_DIR, "static", "uploads", user)):
                os.mkdir(os.path.join(BASE_DIR, "static", "uploads", user))
            with open(os.path.join(BASE_DIR, "static", "uploads", user, name), "wb") as m:
                m.write(base64.b64decode(b64))
            return f"/static/uploads/{user}/{name}"
        else:
            with open(os.path.join(BASE_DIR, "static", "uploads", name), "wb") as m:
                m.write(base64.b64decode(b64))
            return f"/static/uploads/{name}"
    except Exception as m:
        pass

def save_messages(fancy=False, lobby=-1):
    global chatLogs, logins
    try:   
        with open("logins.json", "w") as m:
            #print("Saved logins!")
            json.dump(logins, m)
        lobby = int(lobby)
        #print(chatLogs)
        '''
        if int(lobby) > -1:
            with open(f"saves/chats{lobby}.json", "w") as m:
                if fancy:
                    json.dump(chatLogs[lobby].get_json(), m)
                else:
                    json.dump(chatLogs[lobby].get_json(), m)
        else:
            for i, lobbyNum in enumerate(chatLogs):
                with open(f"saves/chats{i}.json", "w") as m:
                    if fancy:
                        json.dump(lobbyNum.get_json(), m)
                    else:
                        json.dump(lobbyNum.get_json(), m)
        '''
        #lobby_manager.save_lobby(lobby)
    except Exception as e:
        print(f"Failed to save: {e}")
        pass

def load_messages():
    global chatLogs, logins, lobbyCount
    try:
        with open("logins.json", "r") as m:
            loaded = json.load(m)
            logins.clear()
            logins.update(loaded)
        #lobby_manager.load_lobby(-1)
        '''
        for i in range(lobbyCount):
            try:
                with open(f"saves/chats{i}.json", "r") as m:
                    newLobby = common.Lobby()
                    newLobby.load_json(m.read())
                    chatLogs.append(newLobby)
            except FileNotFoundError:
                chatLogs.append(common.Lobby())  # or handle as needed
        '''
    except Exception as e:
        print(f"Failed to load messages: {e}")
        return [], {}
    

def generateRequired():
    if not os.path.exists("static/uploads"):
        os.mkdir("static/uploads")
    if not os.path.exists("saves"):
        os.mkdir("saves")
    if not os.path.exists("default-lobbies"):
        os.mkdir("default-lobbies")

def generateLobbies(count):
    return



print("Loaded data")