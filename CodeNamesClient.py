# echo-client.py

import socket
import json


class send_data:
    def __init__(self, username, password, server_ID, action, action_data):
        self.username = username  # String
        self.password = password  # String
        self.server_ID = server_ID  # int
        self.action = action  # String
        self.action_data = action_data  # String


class receive_data:
    def __init__(self, game_state, server_list, action_data):
        self.game_state = game_state  # CodeGame
        self.server_list = server_list  # [String]
        self.action_data = action_data  # String


def main():
    HOST = "127.0.0.1"  # The server's hostname or IP address
    PORT = 65432  # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            login_data = send_data("user", "pass", None, "LOGIN", None)
            s.sendall(json.dump(login_data))
            received_data = json.load(s.recv(1024))
            if received_data.server_list is not None:
                break

    print(f"Received {data!r}")


if __name__ == "__main__":
    main()
