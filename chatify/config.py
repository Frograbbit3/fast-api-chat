import configparser
import os

configuration = None  # This will hold the actual config object
debug = False
def generate_config():
    if not os.path.exists("config.ini"):
        with open("config.ini", "w") as configfile:
            config = configparser.ConfigParser()
            config['SECURITY'] = {
                'encryption-key': 'rVWxjr21gPj1XNBjvqoD2958huztj5orcIvpqQU3ZLxGSdY5t1',
                'encryption-iv': '3043369271225841'
            }
            config["GENERAL"] = {
                'lobby-count': '10',
                'max-size' : "100MB"
            }

            config["OTHER"] = {
                "debug" : 'False'
            }
            config.write(configfile)

def init():
    global configuration, debug
    generate_config()
    conf = configparser.ConfigParser()
    conf.read('config.ini')
    configuration = conf
    debug = configuration["OTHER"]["debug"].lower() in ('true', '1', 'yes')

print("Loaded config")
