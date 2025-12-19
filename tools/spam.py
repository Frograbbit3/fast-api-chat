import chatify.api as api
import chatify.security as secure
import chatify.data as data
import chatify.config as config


for l in range(50):
    for i in range(1000):
        api.send_message(l, 1, f"stress testing message {i}", http=True)
        print(f"Lobby: {l}, Message: {i}")