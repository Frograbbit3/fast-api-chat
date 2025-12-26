import chatify.api as api


for l in range(50):
    for i in range(1000):
        api.send_message(l, 1, f"stress testing message {i}", http=True)
        print(f"Lobby: {l}, Message: {i}")