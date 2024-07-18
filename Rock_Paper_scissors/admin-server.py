import Pyro4
import sqlite3

@Pyro4.expose
class UserService:
    def __init__(self):
        self.conn = sqlite3.connect('users.db')
        self.conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)')
        self.conn.commit()

    def find_user(self, username, password):
        cursor = self.conn.execute(f"SELECT id FROM users WHERE username='{username}' AND password='{password}'")
        row = cursor.fetchone()
        return row[0] if row else None

    def add_user(self, username, password):
        try:
            self.conn.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
            self.conn.commit()
            return self.conn.execute(f"SELECT id FROM users WHERE username='{username}'").fetchone()[0]
        except Exception as e:
            print(e)
            return None

daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()                  # find the name server
daemon = Pyro4.Daemon(host="127.0.0.1")
uri = daemon.register(UserService)
ns.register("Manageplayer", uri)          # register the object with a name in the name server
print(f"Admin server is Ready for authentication.")
daemon.requestLoop()
