#Import necessary library socket.io and threads
import socket
import threading

#class def for Server
class Server:
    
    #Constructor for Server
    def __init__(self):
        
        #Ip address and Port Number for Server
        self.HOST = '127.0.0.1'
        self.PORT = 1234
        self.LIMIT = 20
        self.activeClients = []
        self.HEADERSIZE = 10
        
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
            
    
    """   #listen_fro_msg_implentation
    def listen_for_msg(self, client, username):
        
        #runs in an infinite while loop to keep on listening for messages sent by clients
        while True:
            #Receives upto 1024 byte of data and decodes using utf-8
            response = client.recv(1024).decode('utf-8')
            
            #If message is not empty it will be sent to all other clients
            if response != '':
                #if response is an integer
                if isinstance(response,int):
                    self.tictactoe(response) 

                final_msg = username + ': ' + response
                self.send_Messages_to_all(final_msg)
            
            #else will prompt that message from client is empty
            else:
                print("The message sent from client {username} is empty")
                break"""
            
    #function to send message to all clients connected to the server
    """def send_Messages_to_all(self,message):
        print(message)
        for user in self.activeClients:
            self.send_message_to_client(user[1], message)"""

            
            
     #Function to handle client
    def handle_client(self,client, ):

        full_msg = ''
        new_msg = True
        
        #server will listen for client userName
        while True:
            #Receives upto 16 byte of data
            username = client.recv(16)

            if new_msg:
                print(f"new message length: {username[:self.HEADERSIZE]}")
                msglen = int(username[:self.HEADERSIZE])
                new_msg = False

            full_msg += username.decode("utf=8")

            if len(full_msg) - self.HEADERSIZE == msglen:
                print("Full message recvd")
                self.activeClients.append((full_msg[self.HEADERSIZE:],client))
                user_joined_msg = (f"{full_msg[self.HEADERSIZE:]}: joined!")
                print(user_joined_msg)
                new_msg = True
                full_msg = ''


            #UNEXPECTED ERROR! 
            #PASSES HUMAN VALUE INTO activeMode List 
            #BUTTTTTTTTTTT PASSES COMPUTER VALUE INTO activeClients LIST ABOVE??????

            
            #Receives upto 16 byte of data
            menu = client.recv(16)

            if new_msg:
                print(f"new message length: {menu[:self.HEADERSIZE]}")
                msglen = int(menu[:self.HEADERSIZE])
                new_msg = False

            full_msg += menu.decode("utf=8")

            if len(full_msg) - self.HEADERSIZE == msglen:
                print("Full message recvd")
                self.activeModes.append((full_msg[self.HEADERSIZE:],client))
                us = (f"On Mode: {full_msg[self.HEADERSIZE:]}")
                print(us)
                new_msg = True
                full_msg = ''
            
        #threading.Thread(target=self.listen_for_msg, args=(client, username,  )).start()
            
    #function to send message to a single client
    """def send_message_to_client(self,client,message):
        client.sendall(message.encode('utf-8'))"""

    #function to Handle TicTacToe Logic
    """def tictactoe(message):
        print('Handle TicTacToe Logic')"""

        
#Calling Server class
Server()
