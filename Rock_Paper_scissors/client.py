import pygame
from network import Network
import pickle
pygame.font.init()
import Pyro4
import tkinter as tk
import time


UserService = Pyro4.Proxy("PYRONAME:Manageplayer@127.0.0.1")
# global name
name = "baby"

start_game=0
    
def login():
    username = username_entry.get()
    password = password_entry.get()
    global name
    name = username

    global user_id
    user_id = UserService.find_user(username, password)
    if user_id is not None and username!="":
        status_label.config(text=f"User {username} logged in with ID {user_id}")
        login_window.destroy()
        global start_game
        start_game=1
    else:
        status_label.config(text="Invalid username or password",fg="red", font=("Georgia", 15))
        start_game=0

def signup():
    username = username_entry.get()
    password = password_entry.get()

    user_id = UserService.add_user(username, password)
    if user_id is not None and username!="" and password!="":
        status_label.config(text="Signup success",fg="#00CC00",font=("Georgia", 15))
    else:
        status_label.config(text="Error signing up user",fg="red", font=("Georgia", 15))

login_window = None

def create_login_window():
    global login_window, username_entry, password_entry, status_label

    login_window = tk.Tk()
    login_window.configure(bg="#323232")
    login_window.title("Login")

    image = tk.PhotoImage(file="./images/title.png").subsample(6,6)
    labelimg = tk.Label(login_window, image=image)
    labelimg.pack(pady=(20,0))

    username_label = tk.Label(login_window, text="Username", font=("Georgia", 20))
    username_label.pack(pady=(40,7),padx=(10,270))
    username_entry = tk.Entry(login_window,width=25,font=("Georgia", 22))
    username_entry.pack(pady=(0,15))
    

    password_label = tk.Label(login_window, text="Password", font=("Georgia", 20))
    password_label.pack(pady=7,padx=(10,270))
    password_entry = tk.Entry(login_window, show="*",width=25,font=("Georgia", 22))
    password_entry.pack()

    status_label = tk.Label(login_window, text="")
    status_label.pack(pady=7)

    login_button = tk.Button(login_window, text="Login", command=login,width=5,font=("Georgia", 20),height=2)
    login_button.pack(side=tk.LEFT, padx=(85,5),pady=(0,80))

    signup_button = tk.Button(login_window, text="Signup", command=signup,width=5,font=("Georgia", 20),height=2)
    signup_button.pack(side=tk.LEFT,padx=(5,5),pady=(0,80))            

    quit_button = tk.Button(login_window, text="Quit", command=login_window.quit,width=5,font=("Georgia", 20),height=2)
    quit_button.pack(side=tk.LEFT,padx=(5,85),pady=(0,80))

    screen_width = login_window.winfo_screenwidth()
    screen_height = login_window.winfo_screenheight()

    # Calculate the x and y coordinates of the top-left corner of the window
    x = int((screen_width - 500) / 2)  # Replace 500 with the desired width of the window
    y = int((screen_height - 500) / 2)  # Replace 500 with the desired height of the window

    # Set the position and size of the window
    login_window.geometry("500x500+{}+{}".format(x, y))

    login_window.mainloop()

create_login_window()

width = 900
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rock Paper Scissors | Player: " + name +" | Player ID: " + str(user_id))



class Button:
    def __init__(self,text, x, y, color2):
        self.x = x
        self.y = y
        self.text = text
        self.color = (0,0,0)
        self.width = 120
        self.height = 60
        self.color2 = color2

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("Georgia", 35)
        text = font.render(self.text, 1, self.color2)
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redrawWindow(win, game, p, games_played, games_won_p0, games_won_p1):
    img = pygame.image.load("./images/bg.png")
    img = pygame.transform.scale(img, (900, 700))
    win.blit(img, (0, 0))

    if not(game.connected()):
        font = pygame.font.SysFont("Georgia", 70)
        text = font.render("Waiting for Player...", 1, (255,255,255), True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("Georgia", 30)

        font1 = pygame.font.SysFont("Georgia", 25, True)

        text1 = font1.render("Player: "+name, 1, (204, 255,255))
        win.blit(text1, (25, 30))

        text2 = font1.render("Games Played: "+str(games_played), 1, (204, 255,255))
        win.blit(text2, (350, 30))

        if p == 0:
            text3 = font1.render("Games Won: "+str(games_won_p0), 1, (204, 255,255))
        else:
            text3 = font1.render("Games Won: "+str(games_won_p1), 1, (204, 255,255))

        win.blit(text3, (680, 30))

        text = font.render("Your Move", 1, (255, 255,255))
        win.blit(text, (180, 220))

        text = font.render("Opponent's Move", 1, (255, 255, 255))
        win.blit(text, (460, 220))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1, (255,255,255))
            text2 = font.render(move2, 1, (255,255,255))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (255,255,255))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (255,255,255))
            else:
                text1 = font.render("Waiting...", 1, (255,255,255))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (255,255,255))
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (255,255,255))
            else:
                text2 = font.render("Waiting...", 1, (255,255,255))

        if p == 1:
            win.blit(text2, (200, 320))
            win.blit(text1, (520, 320))
        else:
            win.blit(text1, (200, 320))
            win.blit(text2, (520, 320))

        img = pygame.image.load("./images/rock.png")
        img = pygame.transform.scale(img, (150, 170))
        win.blit(img, (160, 430))

        img = pygame.image.load("./images/Paper.png")
        img = pygame.transform.scale(img, (150, 170))
        win.blit(img, (360, 430))

        img = pygame.image.load("./images/Scissors.png")
        img = pygame.transform.scale(img, (150, 170))
        win.blit(img, (560, 430))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()


btns = [Button("Rock", 175, 600, (241,79,187)), Button("Paper", 375, 600, (61,169,250)), Button("Scissors", 575, 600, (246,210,43))]


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)
    games_played = 0
    games_won_p0 = 0
    games_won_p1 = 0

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            redrawWindow(win, game, player, games_played, games_won_p0, games_won_p1)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("Georgia", 50)
            if (game.winner() == 1 and player == 1):
                text = font.render("You Won!", 1, (0,255,0))
                games_won_p1 = games_won_p1 + 1

            elif (game.winner() == 0 and player == 0):
                text = font.render("You Won!", 1, (0,255,0))
                games_won_p0 = games_won_p0 + 1

            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (0,0,255))

            else:
                text = font.render("You Lost...", 1, (255, 0, 0))

            win.blit(text, (350,100))
            pygame.display.update()
            pygame.time.delay(2000)
            games_played = games_played + 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

        redrawWindow(win, game, player, games_played, games_won_p0, games_won_p1)

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))

        img = pygame.image.load("./images/bg.png")
        img = pygame.transform.scale(img, (900, 700))
        win.blit(img, (0, 0))

        # font = pygame.font.SysFont("comicsans", 60)
        # text = font.render("Click to Play!", 1, (0, 0, 0))
        # win.blit(text, (100, 200))

        img = pygame.image.load("./images/title.png")
        img = pygame.transform.scale(img, (850, 150))
        win.blit(img, (25, 70))

        img = pygame.image.load("./images/home-logo.png")
        img = pygame.transform.scale(img, (300, 300))
        win.blit(img, (300, 250))

        img = pygame.image.load("./images/button.png")
        img = pygame.transform.scale(img, (250, 100))
        win.blit(img, (310, 560))
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

if start_game==1:
    while True:
        menu_screen()
