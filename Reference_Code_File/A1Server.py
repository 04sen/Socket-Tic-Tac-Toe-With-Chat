"""""""""""
CS310 - Computer Networks 
Semester 1, 2023
Assignment 1

Group Members:
Name: Bhargav Pala
ID: S11188676

Name: Yash Maharaj
ID: S11196606
"""""""""""

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
            print(f"successfully connected to client {address[0]} {address[1]}")
            threading.Thread(target=self.handle_client, args=(client, )).start()
            
    
   #listen_fro_msg_implentation
    def listen_for_msg(self, client, username):
        
        #runs in an infinite while loop to keep on listening for messages sent by clients
        while True:
            #Receives upto 1024 byte of data and decodes using utf-8
            response = client.recv(1024).decode('utf-8')
            
            #If message is not empty it will be sent to all other clients
            if response != '':
                final_msg = username + ': ' + response
                self.send_Messages_to_all(final_msg)
            
            #else will prompt that message from client is empty
            else:
                print("The message sent from client {username} is empty")
                break
            
    #function to send message to all clients connected to the server
    def send_Messages_to_all(self,message):
        print(message)
        for user in self.activeClients:
            self.send_message_to_client(user[1], message)
            
            
     #Function to handle client
    def handle_client(self,client):
    
        #server will listen for client userName
        while True:
            
            #Receives upto 1024 byte of data and decodes using utf-8
            username = client.recv(1024).decode('utf-8')
            
            #if user name is not empty, then it will append it in the activeClients list and send to all connected clients 
            if username != '':
                self.activeClients.append((username, client))
                user_joined_msg = (f"{username}: joined the chat!!")
                print(user_joined_msg)
                self.send_Messages_to_all(user_joined_msg)
                break
            
            #if client username is empty 
            else:
                print("Client username is empty")
            
        threading.Thread(target=self.listen_for_msg, args=(client, username,  )).start()
            
    #function to send message to a single client
    def send_message_to_client(self,client,message):
        client.sendall(message.encode('utf-8'))

#Calling Server class
Server()