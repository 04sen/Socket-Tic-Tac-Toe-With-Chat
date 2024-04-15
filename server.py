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
        self.activeUsers = []
        self.activeModes = []
        self.HEADERSIZE = 10

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
    def listen_for_msg(self, client, activeUsers, activeMode):

        full_msg = ''
        new_msg = True
        i = 0
        
        #runs in an infinite while loop to keep on listening for messages sent by clients
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
                print(username)
                
                for user in activeUsers:
                    if user == username:
                        print('found')
                        break
                    elif i == self.LIMIT:
                        print('exit')
                        break
                    i = i + 1

                new_msg = True
                full_msg = ''
            
            #Receives upto 1024 byte of data and decodes using utf-8
            message = client.recv(1024)

            if new_msg:
                print(f"new message length: {message[:self.HEADERSIZE]}")
                msglen = int(message[:self.HEADERSIZE])
                new_msg = False

            full_msg += message.decode("utf=8")

            if len(full_msg) - self.HEADERSIZE == msglen:
                print("Full message recvd")
                message = full_msg[self.HEADERSIZE:]
                
                if message == self.EXIT_STRING:
                    user_msg = (f"{activeUsers[i]} ({activeMode[i]}) has disconnected!")
                    self.send_Messages_to_all(user_msg)
                    activeUsers.pop(i)
                    activeMode.pop(i)
                    new_msg = True
                    full_msg = ''
                    i = 0
                    return
                
                elif message.startswith("MOVE"):
                    # Extract the row and column from the move message
                    print("Received move:", message)
                    _, row_str, col_str = message.split()
                    row = int(row_str)
                    col = int(col_str)

                    # Process the move
                    response = self.process_move(row, col, activeUsers[i], activeMode[i]) 
                    self.send_message_to_client(client,response)

                    new_msg = True
                    full_msg = ''
                    i = 0

                else:
                    user_msg = (f"{activeUsers[i]} ({activeMode[i]}) : {message}")
                    print(user_msg)
                    self.send_Messages_to_all(user_msg)

                new_msg = True
                full_msg = ''
                i = 0
                
            
            #else will prompt that message from client is empty
            else:
                print("The message sent from client {username} is empty")
                break
            
    #function to send message to all clients connected to the server
    def send_Messages_to_all(self,message):
        print(message)
        for user in self.activeClients:
            self.send_message_to_client(user[1], message)
            
            
        #function to send message to a single client
    def send_message_to_client(self,client,message):
        client.sendall(bytes(message, 'utf-8'))
    
    def process_move(self,  row, col, username, mode):
        print(f"Processing move by {username} ({mode}) : Row={row}, Column={col}")

        #<-- Have to implement a way to store move -->

        response = "Move processed successfully"
        return response

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
                self.activeClients.append((username,client))
                self.activeUsers.append(username)
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
                self.activeModes.append(menu)
                user_mode_msg = (f"On Mode: {menu}")
                print(user_mode_msg)
                new_msg = True
                full_msg = ''
  
            message = f'{self.activeUsers}' + ", "
            send_msg = f'{username} joined on {menu} Mode!'

            self.send_Messages_to_all(message)
            time.sleep(1)
            self.send_Messages_to_all(send_msg)

            break
            
        threading.Thread(target=self.listen_for_msg, args=(client, self.activeUsers, self.activeModes)).start()
            
    #function to send message to a single client
    """def send_message_to_client(self,client,message):
        client.sendall(message.encode('utf-8'))"""

    #function to Handle TicTacToe Logic
    """def tictactoe(message):
        print('Handle TicTacToe Logic')"""

        
#Calling Server class
Server()
