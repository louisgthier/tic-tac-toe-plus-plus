import socket

import main
from game import Game
import pickle
import threading
import _thread

class Client:
    def __init__(self, address):
        ip,port = address

        print("IP:",ip)
        print("Port:",port)

        # TCP based client socket
        s = socket.socket()

        s.connect(address)

        print("Player connected to a game")

        #threading.Thread(target=main.pygame_loop).start()
        _thread.start_new_thread(Client.game_loop, (self, s))
        main.pygame_loop()
    def game_loop(self,s):
        self.player_number = int(str(s.recv(1024).decode()).split(":",1)[1])
        self.game = Game(0)

        print(f"Player has number {self.player_number}")


        while True:

            # Get the reply
            msgReceived = s.recv(1024)
            self.game = pickle.loads(msgReceived)

            main.draw_game()
            if self.game.turn==self.player_number:
                action = "{play}:"+main.get_action(self.game)
                s.send(action.encode())



if __name__ == "__main__":
    try:
        text = input("Please enter the server IP address: ")
        if ":" in text:
            ip, port = text.split(":")
            port = int(port)

        else:
            ip, port = text, 5500
            if ip == "":
                ip = "localhost"
    except:
        ip, port = "localhost", 5500

    print(f"Trying to connect to {ip}:{port}")
    client = Client((ip, port))

