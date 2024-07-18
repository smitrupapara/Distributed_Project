import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.primary_server = "127.0.0.1"
        self.backup_server = "127.0.0.1"
        self.primary_port = 5555
        self.backup_port = 5556
        self.primary_addr = (self.primary_server, self.primary_port)
        self.backup_addr = (self.backup_server, self.backup_port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self,retries=5):
        for i in range(retries):
            try:
                self.client.connect(self.primary_addr)
                return self.client.recv(2048).decode()
            except:
                try:
                    self.client.connect(self.backup_addr)
                    return self.client.recv(2048).decode()
                except:
                    pass
        return None

    def switch_to_backup(self):
        if self.current_server == "primary":
            self.client.close()
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(self.backup_addr)
            self.current_server = "backup"
            print("Switched to backup server.")

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)
            if self.current_server == "primary":
                print("Connection to primary server failed. Switching to backup server...")
                self.switch_to_backup()
                return self.send(data)
            else:
                print("Connection to backup server failed.")

