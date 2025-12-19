from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import base64
import os   
from hashlib import sha256
from . import common, config, api
from .shared import logins
import json
lobby_manager = None


def init(key, iv):
    global encryption_key, iv_bytes
    encryption_key = sha256(key.encode()).digest() 
    iv_bytes = iv.encode() if isinstance(iv, str) else iv
def encrypt(plaintext):
    global encryption_key, iv_bytes
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext.encode()) + padder.finalize()
    cipher = Cipher(algorithms.AES(encryption_key), modes.CBC(iv_bytes))
    ct = cipher.encryptor().update(padded_data) + cipher.encryptor().finalize()
    return base64.b64encode(ct).decode()
def decrypt(b64_cipher):
    try:
        ct = base64.b64decode(b64_cipher)
        cipher = Cipher(algorithms.AES(encryption_key), modes.CBC(iv_bytes))
        decrypted = cipher.decryptor().update(ct) + cipher.decryptor().finalize()
        unpadder = padding.PKCS7(128).unpadder()
        return (unpadder.update(decrypted) + unpadder.finalize()).decode()
    except ValueError:
        return b64_cipher
    
def hash(data, times=1):
    if times > 1:
        for _ in range(times):
            data = sha256(data.encode()).hexdigest()
        return data
    return sha256(data.encode()).hexdigest()

def process_login(username, password):
    global logins
    with open("logins.json", "w") as m:
        print("Saved logins!")
        json.dump(logins, m)
    if username in logins.keys():
        token = hash(hash(username) + hash(password))
        if token == logins[username]["token"]:
            return {"status": "success"}
    else:
        logins[username] = common.create_user(username, password)
        return {"status": "created", "new_table": common.create_user(username, password)}
    return {"status": "failed"}

def tokenize_user(token=None, username=None):
    if token is not None:
        for user, data in logins.items():
            if data.get("token") == token:
                data["name"] = user
                return data
    if username is not None:
        for user, data in logins.items():
            if user == username:
                data["name"] = user
                return data
    return None

def check_token(token, lobbyVV=-1):
    lobbyVV = int(lobbyVV) if isinstance(lobbyVV, str) else lobbyVV
    global logins
    for keyed in logins.keys():
        val = logins[keyed]
        val["name"] = keyed
       # print(val)
        if val:
            if val["token"] == token:
                if int(lobbyVV) > -1 or api.is_admin(keyed, -1):
                    lob = lobby_manager.get_lobby(lobbyVV)
                    if lob.is_user(keyed) or api.is_admin(keyed, -1):
                        return keyed
                elif lobbyVV == -1:
                    return keyed
    return False
