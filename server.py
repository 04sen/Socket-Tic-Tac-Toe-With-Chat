# Copyright (c) [2024] [Sachinandan Das Sen, Shamal Kurmar, Shivneel Narayan]
# This file is part of [CS310-2024], which is released under the MIT License.
# See LICENSE.md for details or visit https://opensource.org/licenses/MIT.


#Import necessary library socket.io and threads
import socket
import threading
import time

#class def for Server
class Server:
    #Constructor for Server
    def __init__(self):
        
        #Ip address and Port Number for Server
        self.HOST = '127.0.0.1'
        self.PORT = 1234
        self.LIMIT = 20
        self.activeClients = []
        self.waitingUsers = []
        self.HEADERSIZE = 10
        self.internal_boards = []
        self.game_session = []
        #if user sends this hashed string it will exit program
        #probablity (approx) = 3.421×10^−72 %
        self.EXIT_STRING = 'a72b20062ec2c47ab2ceb97ac1bee818f8b6c6cb'
        
        #AF_INET: we are going to use IPv4 addresses
        #SOCK_STREAM: using TCP connection
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        #Bind server to Host and Port
        try:
            self.server.bind((self.HOST,self.PORT))
            print(f"Running the server on {self.HOST},  {self.PORT} ")
        except:
            print(f"Unable to bind to {self.HOST} and port {self.PORT}")
        
        #set Server Limit
        self.server.listen(self.LIMIT)
        
        #While loop that keeps listening for clients
        while True:
            client, address = self.server.accept()
            print(f"successfully connected client ({address[0]},{address[1]})")
            threading.Thread(target=self.handle_client(client,)).start()
          
    #listen_fro_msg_implentation
    def listen_for_msg(self, client, internal_board):
        full_msg = ''
        new_msg = True
        i = 0

        #runs in an infinite while loop to keep on listening for messages sent by clients
        while True:
            for user in self.activeClients:
                if user[1] == client:
                    print("found")
                    break
                elif i == self.LIMIT:
                    print('not found')
                    break
                i = i + 1

            if self.activeClients[i][2] == "HUMAN":
                self.pair_clients(self.waitingUsers)
                for session in self.game_session:
                    if client in session:
                        if self.check_win(session[2], "X"):
                            self.send_Messages_to_all("X wins!")
                            return  # Stop further processing as the game is over
                        elif self.check_win(session[2], "O"):
                            self.send_Messages_to_all("O wins!")
                            return  # Stop further processing as the game is a tie
                        elif not any(' ' in row for row in session[2]):
                            self.send_Messages_to_all("Tie game!")
                            return  # Stop further processing as the game is a tie
            
            
            #Receives upto 1024 byte of data and decodes using utf-8
            message = client.recv(1024)

            if new_msg:
                msglen = int(message[:self.HEADERSIZE])
                new_msg = False

            full_msg += message.decode("utf=8")

            if len(full_msg) - self.HEADERSIZE == msglen:
                message = full_msg[self.HEADERSIZE:]
               
                if message == self.EXIT_STRING:
                        
                        user_msg = (f"{self.activeClients[i][0]} ({self.activeClients[i][2]}) has disconnected!")
                        self.send_Messages_to_all(user_msg)
                        self.activeClients.pop(i)
                        print(self.activeClients)
                        current_activeUsers = ""

                        for user in self.activeClients:
                            current_activeUsers = f'| {user[0]} |' + current_activeUsers
                        
                        self.send_Messages_to_all(current_activeUsers)

                        new_msg = True
                        full_msg = ''
                        i = 0

                        return
                
                elif message == "RESET":
                    internal_board[i] = self.create_brd() #Resets the server side Board
            
                    new_msg = True
                    full_msg = ''
                    i = 0

                elif message.startswith("MOVE") and self.activeClients[i][2] == "COMPUTER":
                    # Extract the row and column from the move message
                    print("Received move:", message)
                    _, row_str, col_str = message.split()
                    row = int(row_str)
                    col = int(col_str)

                    # Process the move
                    self.process_move_computer(self.activeClients[i][1], row,col,self.internal_boards[i])

                    new_msg = True
                    full_msg = ''
                    i = 0

                elif message.startswith("MOVE") and self.activeClients[i][2] == "HUMAN":
                    for session in self.game_session:
                        if client in session:
                            self.process_move_human(client,message, session[2])

                            new_msg = True
                            full_msg = ''
                            i = 0
                else:
                    user_msg = (f"{self.activeClients[i][0]} ({self.activeClients[i][2]}) : {message}")
                    self.send_Messages_to_all(user_msg)

                new_msg = True
                full_msg = ''
                i = 0

            else:
                print("The message sent from client {username} is empty")
                break
        client.close() 
   
#---------------------------------------------------------------------------------
    
    def process_move_computer(self, client, row, col,board):
        # Check if the spot is already taken or not
        if board[row][col] == ' ':
            board[row][col] = 'X'  # Client's move
            if self.check_win(board, 'X'):
                client.sendall("You win!".encode('utf-8'))
                return  # Stop further processing as the game is over
            elif not any(' ' in row for row in board):
                client.sendall("Tie game!".encode('utf-8'))
                return  # Stop further processing as the game is a tie
            else:
                self.server_move(board, client)  # Server makes a move if game not ended
        else:
            client.sendall("Invalid move".encode('utf-8'))

    def server_move(self, board, client):
    # Simple random move logic by the server
        import random
        empty = [(r, c) for r in range(3) for c in range(3) if board[r][c] == ' ']
        if empty:
            row, col = random.choice(empty)
            board[row][col] = 'O'
            if self.check_win(board, 'O'):
                client.sendall(f"COMPUTER_MOVE {row} {col}".encode('utf-8'))
                client.sendall("Server wins!".encode('utf-8'))
            else:
                client.sendall(f"COMPUTER_MOVE {row} {col}".encode('utf-8'))
        else:
            client.sendall("Tie game!".encode('utf-8'))

#---------------------------------------------------------------------------------

    def process_move_human(self,client,message,board):
        if self.check_win(board, "X"):
            client.sendall("X wins!".encode('utf-8'))
            return  # Stop further processing as the game is over
        elif self.check_win(board, "O"):
            client.sendall("O wins!".encode('utf-8'))
            return  # Stop further processing as the game is a tie
        elif not any(' ' in row for row in board):
            client.sendall("Tie game!".encode('utf-8'))
            return  # Stop further processing as the game is a tie
        else:
            for session in self.game_session:
                if client in session:
                    _, _, self.shared_board = session
                    _, row_str, col_str = message.split()
                    row, col = int(row_str), int(col_str)
                    player = 'X' if session.index(client) == 0 else 'O'
                    if  self.shared_board[row][col] == ' ':
                        self.shared_board[row][col] = player
                        self.update_game(session, f'Player {player} {row} {col}')
                        break

    def update_game(self,session,message):
        client1, client2, _ = session
        for client in (client1,client2):
            self.send_message_to_client(client,message)

    def pair_clients(self,activeClients):
        if len(activeClients) >= 2:
            client1 = activeClients.pop(0)
            client2 = activeClients.pop(0)
            self.shared_board = self.create_brd()
            self.game_session.append((client1,client2,self.shared_board))
            self.send_message_to_client(client1, "You are connected, You are X")
            self.send_message_to_client(client2, "You are connected, You are O")   

#---------------------------------------------------------------------------------

    def check_win(self, board, player):
        # Check horizontal, vertical and diagonal wins
        for i in range(3):
            if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
                return True
        if board[0][0] == board[1][1] == board[2][2] == player or board[0][2] == board[1][1] == board[2][0] == player:
            return True
        return False
    
    def create_brd(self,):
        game_board = [[' ' for _ in range(3)] for _ in range(3)]
        return game_board   
    
#---------------------------------------------------------------------------------

    #function to send message to all clients connected to the server
    def send_Messages_to_all(self,message):
        print(message)
        for user in self.activeClients:
            self.send_message_to_client(user[1], message)           
       
        #function to send message to a single client
    def send_message_to_client(self,client,message):
        client.sendall(bytes(message, 'utf-8'))

#---------------------------------------------------------------------------------

    #Function to handle client
    def handle_client(self,client, ):

        full_msg = ''
        new_msg = True
        
        
        #server will listen for client userName
        while True:
            #Receives upto 1024 byte of data
            username = client.recv(1024)

            if new_msg:
                print(f"new message length: {username[:self.HEADERSIZE]}")
                msglen = int(username[:self.HEADERSIZE])
                new_msg = False

            full_msg += username.decode("utf=8")

            if len(full_msg) - self.HEADERSIZE == msglen:
                print("Full message recvd")
                username = full_msg[self.HEADERSIZE:]
                user_joined_msg = (f"{username}: joined!")
                print(user_joined_msg)
                new_msg = True
                full_msg = ''
            
            #Receives upto 20 byte of data since only 2 options are available
            menu = client.recv(20)

            if new_msg:
                print(f"new message length: {menu[:self.HEADERSIZE]}")
                msglen = int(menu[:self.HEADERSIZE])
                new_msg = False

            full_msg += menu.decode("utf=8")

            if len(full_msg) - self.HEADERSIZE == msglen:
                print("Full message recvd")
                menu = full_msg[self.HEADERSIZE:]
                user_mode_msg = (f"On Mode: {menu}")
                print(user_mode_msg)
                new_msg = True
                full_msg = ''


            self.activeClients.append((username, client, menu) )
            if menu == "HUMAN":
                self.waitingUsers.append(client)
  
            send_msg = f'{username} joined on {menu} Mode!'


            current_activeUsers = ""
            for user in self.activeClients:
                current_activeUsers = f'| {user[0]} |' + current_activeUsers

            self.send_Messages_to_all(current_activeUsers)

            time.sleep(1)

            self.send_Messages_to_all(send_msg)

            time.sleep(1)

            if menu =="COMPUTER":
                self.board = self.create_brd()
                self.internal_boards.append(self.board)
                self.send_message_to_client(client,"You are connected, You are X")

            break
            
        threading.Thread(target=self.listen_for_msg, args=(client,self.internal_boards)).start()


#Calling Server class
Server()
