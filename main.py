import io, json
import requests
import time
import base64

import traceback

from websockets.sync.client import connect

config_file = io.open('./config.json', 'r')
config = json.loads(config_file.read())
config_file.close()

local_server = config["local_server"] + ":" + str(config["local_port"])

if config["local_https"]:
    local_server = "https://" + local_server
else:
    local_server = "http://" + local_server

print(local_server)

remote_server = config["remote_server"] + ":" + str(config["remote_port"]) + config["remote_path"]

if config["remote_https"]:
    remote_server = "wss://" + remote_server
else:
    remote_server = "ws://" + remote_server


print(remote_server)

def form_response(r, id):
    response = {"type": "response", "status": r.status_code, "content": base64.b64encode(r.content).decode("ASCII"), "id": id}
    return json.dumps(response)

while True:
    try:
        with connect(remote_server) as websocket:
            print("Pairing with code " + config["remote_pairing_code"])
            websocket.send(json.dumps({"type": "pairing", "code": config["remote_pairing_code"]}))
            while True:
                try:
                    message = websocket.recv(timeout=1.0)
                    received = json.loads(message)
                    print("Received", received)
                    id = received["id"]
                    match received["type"]:
                        case "request":
                            url = local_server + "/" + received["url"]
                            match received["method"]:
                                case "GET":
                                    r = requests.get(url)
                                    websocket.send(form_response(r, id))
                                case "POST":
                                    r = requests.post(url, received["body"])
                                    websocket.send(form_response(r, id))
                        case "other":
                            pass
                except TimeoutError:
                    pass
    except KeyboardInterrupt:
        break
    except Exception as e:
        print("Connection error, retrying in 3s")
        traceback.print_exc()
        time.sleep(3.0)