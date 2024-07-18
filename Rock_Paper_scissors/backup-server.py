import socket
from _thread import *
import pickle
from game import Game

primary_server = "127.0.0.1"
primary_port = 5555
backup_server="127.0.0.1"
backup_port=5556

# Set up backup server socket
backup_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    backup_socket.bind((backup_server, backup_port))
except socket.error as e:
    str(e)
backup_socket.listen(2)
print("Waiting for a connection, backup server started")

# Global variables
games = None
is_primary = False
primary_conn = None


def receive_from_primary():
    global games, primary_conn, is_primary
    while True:
        try:
            data = primary_conn.recv(4096)
            if not data:
                break
            else:
                games = pickle.loads(data)
        except:
            break
    print("Disconnected from primary server")
    is_primary = True
    primary_conn = None


# Main loop for backup server
while True:
    if is_primary:
        # Try to connect to primary server
        try:
            primary_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Connected to primary server")
        except:
            print("Failed to connect to primary server")
            # continue

        # Start a new thread to receive game data from primary server
        start_new_thread(receive_from_primary, ())

    else:
        # Accept connections from clients
        conn, addr = backup_socket.accept()
        print("Connected to client:", addr)

        # Send game data to client
        conn.sendall(pickle.dumps(games))

        # Start a new thread for the client
        def threaded_client():
            global games
            while True:
                try:
                    data = conn.recv(4096)
                    if not data:
                        break
                    else:
                        games = pickle.loads(data)
                except:
                    break
            print("Disconnected from client")
            conn.close()

        start_new_thread(threaded_client, ())
