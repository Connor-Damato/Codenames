import sys
import socket
import selectors
import types
import json
from CodeGame import CodeGame
import threading

servers = []
players = {}
universalID = 0
id_lock = threading.Lock()
sel = selectors.DefaultSelector()


class data:
    def __init__(self, username, password, server_ID, action, action_data):
        self.username = username
        self.password = password
        self.server_ID = server_ID
        self.action = action
        self.action_data = action_data


class GameServer:
    def __init__(self, id, name):
        self.id = generate_server_ID()
        self.name = name
        self.game = CodeGame()


def main():
    host = "127.0.0.1"  # Standard loopback interface address (localhost)
    port = 65432  # Port to listen on (non-privileged ports are > 1023)

    # host, port = sys.argv[1], int(sys.argv[2])
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind((host, port))
    lsock.listen()
    print(f"Listening on {(host, port)}")
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)
    try:
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    service_connection(key, mask)
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        sel.close()


def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            interpret_data(data)
        else:
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(f"Echoing {data.outb!r} to {data.addr}")
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]


def start_game_server():
    GameServer()
    servers.append(GameServer)
    return


def generate_player_ID():
    with id_lock:
        universalID += 1
        return universalID


def generate_server_ID():
    return len(servers)


def get_server_by_ID(server_id):
    for server in servers:
        if server.id == server_id:
            return server


# data format (player id, server id (or NEW), command, data)
def interpret_data(data):
    command = json.load(data)

    if command[0] is None:
        id = generate_player_ID()
        players.update(id, None)
        return id
    elif command[1] == "NEW":
        start_game_server()
    elif command[1] == "FETCH":
        return [servers]
    else:
        match command[2]:
            case "MOVE":
                return True
            case "HINT":
                return True
            case "BOARD":
                return True
            case "WINNER":
                return True
            case "JOIN":
                # add new player object to given server
                server = get_server_by_ID(command[1])
                server.game.players.append(command[0])
                players.update(command[0], command[1])
            case "PING":
                return None
            case "PING_FAIL":
                players.remove(command[0])
                get_server_by_ID(command[1]).game.players.rem(command[0])


if __name__ == "__main__":
    main()
