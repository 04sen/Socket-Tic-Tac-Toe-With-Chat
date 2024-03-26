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


#Import necessary library socket.io, threads, custom tkinter, messagebox, and random
import socket
import threading
import customtkinter as tks
from tkinter import messagebox as errorBox
import random


#class def for client
class Client:
    
    #constructor for client 
    def __init__(self):
        
        #Ip address and port number to connect to server
        self.HOST = '127.0.0.1'
        self.PORT = 1234
        
        #AF_INET: we are going to use IPv4 addresses
        #SOCK_STREAM: using TCP connection
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.activeClient = []
        
        #Generate random Ip address and portNum for Client
        self.ipAddress = self.generate_random_ipv4_address()
        self.portNum = self.generate_random_port_number()
        
        #Font declaration
        self.FONT = ("Helvetica", 17)
        self.BUTTON_FONT = ("Helvetica", 15)
        self.SMALL_FONT = ("Helvetica", 13)
        
        #Creating Windows screen in tkinter and setting theme
        tks.set_appearance_mode("dark")
        tks.set_default_color_theme("dark-blue")
        self.root = tks.CTk()
        self.root.geometry("650x600")
        self.root.title("Messenger Client")
        self.root.resizable(False, False)
        
        
        #Binding  server to Host and Port
        try:
            self.client.bind((self.ipAddress,self.portNum))
            print(f"Running the client server on {self.ipAddress},  {self.portNum} ")
        except:
            print(f"Unable to bind to {self.ipAddress} and port {self.ipAddress}")
            
        
    
    #Generate a random IPv4 address while keeping the first octet as '127'
    def generate_random_ipv4_address(self):
        self.octets = ['127']
        for i in range(1, 4):
            self.octets.append(str(random.randint(0, 255)))
        return '.'.join(self.octets)
    
    # Generate a random integer between 1024 and 65535
    def generate_random_port_number(self):
        self.port_number = random.randint(1024, 65535)
        return self.port_number
    
   
        
     #function to send message to a single client
    def send_message_to_client(self,client,message):
        client.sendall(message.encode('utf-8'))
        
        
    #function to disconnect client from the chat app
    def disconnect(self):
        disconnect_msg = f"{self.userName_entry.get()} Left the chat!! "
        self.client.sendall(disconnect_msg.encode('utf-8'))
        self.root.destroy() 
        self.client.shutdown(socket.SHUT_RDWR)
        self.client.close()
        
    
    #Gui for the creation of the system interface
    def gui(self):
        
        #creation of userFrame
        self.userName_frame = tks.CTkFrame(self.root,)
        self.userName_frame.grid(row=0, column=0, sticky=tks.NSEW)

        #creation of UserName entry where the user enters his/her userName
        self.userName_entry = tks.CTkEntry(master=self.userName_frame, placeholder_text="Username",width=175, height = 33)
        self.userName_entry.pack(padx=175, pady=5, )

        #creation of Password entry where the user enters his/her password 
        self.Password_entry = tks.CTkEntry(master=self.userName_frame, placeholder_text="Password",width=175, height = 33, show="*")
        self.Password_entry.pack(padx=175, pady=5)

        #creation of login Button for the user to login to the system
        self.login_button = tks.CTkButton(master=self.userName_frame, text="Login",command=self.connect)
        self.login_button.pack(side=tks.LEFT,padx=65, pady=9)
        
        #creation of leave button for the user to leave the system
        self.Leave_button = tks.CTkButton(master=self.userName_frame, text="Leave", command=self.disconnect)
        self.Leave_button.pack(padx=1, pady=7)
        self.Leave_button.configure(state=tks.DISABLED)
        
        #creation of message box frame
        self.messagebox_frame = tks.CTkFrame(self.root, )
        self.messagebox_frame.grid(row=1, column=0,sticky=tks.NSEW )

        #creation of message box field where all the messages can be seen 
        self.messagebox = tks.CTkTextbox(self.messagebox_frame, width=500, height=410)
        self.messagebox.configure(state=tks.DISABLED)
        self.messagebox.pack(side=tks.LEFT)
        
        #creation of online user message box to display all the online users 
        self.onlineUser = tks.CTkTextbox(self.messagebox_frame, width=145, height=410,)
        self.onlineUser.insert(tks.END, "Online Users:\n")
        self.onlineUser.configure(state=tks.DISABLED)
        self.onlineUser.pack(side=tks.LEFT, padx=5 )

        #creation of the message entry field where the user enters his/her message
        self.messageEntry_frame = tks.CTkFrame(self.root,)
        self.messageEntry_frame.grid(row=2, column=0,sticky=tks.NSEW )
        
        #creation of the message entry field where the user enters his/her message
        self.messageEntry = tks.CTkEntry(self.messageEntry_frame, placeholder_text="Enter Message:", font=self.FONT, width=500, height = 40)
        self.messageEntry.pack(side=tks.LEFT, pady=10, )
        self.messageEntry.configure(state=tks.DISABLED)

        #creation of send button where the user can send the message entered in the message field 
        self.SendButton = tks.CTkButton(self.messageEntry_frame, text="Send", height = 40, font=self.FONT, command=self.send_message)
        self.SendButton.pack(side =tks.LEFT, padx=5)
        self.SendButton.configure(state=tks.DISABLED)
        
        #creates the gui 
        self.root.mainloop()
        
    #function that is used to connect the client to the server
    def connect(self):
        
        #gets the username and password entered by user and stores in username and password 
        self.username = self.userName_entry.get()
        self.password = self.Password_entry.get()
        
        #if username and password empty then it will display error message to users
        if (self.username == '' and self.password == ''):
            errorBox.showerror("UserName and Password","UserName and Password cannot be empty")
            self.root.mainloop()
        #if username is empty then it will display error message
        elif self.username == '':
            errorBox.showerror("UserName", "UserName cannot be empty")
            self.root.mainloop()
        #if password is empty then it will display error message
        elif self.password == '':
            errorBox.showerror("Password", "Password cannot be empty")
            self.root.mainloop()
        
        # try except block
        try:
            # Connect to the server
            self.client.connect((self.HOST, self.PORT))
            self.client.sendall(self.username.encode('utf-8'))
            print("Successfully connected to server")
        
        #if the user wasnt able to connect to server then it will show error message
        except:
            errorBox.showerror("Unable to connect to server", f"Unable to connect to server {self.HOST} {self.PORT}")
            self.root.mainloop()
        
        #starts a thread that listens from messages from server
        threading.Thread(target=self.listen_for_messages_from_server, args=(self.client, )).start()
        
        self.userName_entry.configure(state=tks.DISABLED)
        self.Password_entry.configure(state=tks.DISABLED)
        self.login_button.configure(state=tks.DISABLED)
        self.messageEntry.configure(state=tks.NORMAL)
        self.SendButton.configure(state=tks.NORMAL)
        self.SendButton.configure(state=tks.NORMAL)
        self.Leave_button.configure(state=tks.NORMAL)
    
    #function send_message sends the message to all other clients
    def send_message(self):
        
        #Gets message entered by the user
        self.message = self.messageEntry.get()
        
        #checks if message is not empty
        if self.message != '':
            #sends message to all active clients 
            self.client.sendall(self.message.encode())
            
            #deletes the message entered by the user in the message box
            self.messageEntry.delete(0, len(self.message))
        
        #checks if message is empty, then it will display a error message
        else:
            errorBox.showerror("Empty message", "Message cannot be empty")
            pass
        
    # listens for message from all active clients
    def listen_for_messages_from_server(self,client):
       
       #runs in an infinite loop to listen for messages
       while 1:
            
            #receives upto 2048 bytes of data and decodes using utf-8
            message = client.recv(2048).decode('utf-8')
            print(message)

            #checks if message is not empty
            if message != '':
                #splits the between username and message
                system = message.split(": ")[0]
                content = message.split(": ")[1]
                #adds message in message box
                self.add_message(f"{system}: {content}")
            
            # checks if message entered is empty, then display error message
            else:
                errorBox.showerror("Error", "Message recevied from client is empty")
                pass

    #adds message in message box
    def add_message(self,message):
        self.messagebox.configure(state=tks.NORMAL)
        self.messagebox.insert(tks.END, message + '\n')
        self.messagebox.configure(state=tks.DISABLED)
    
    #adds online user 
    def add_OnlineUser(self,client):
     while 1: 
        self.userName = client.recv(2048).decode('utf-8')
        self.activeClients.append(self.userName)
        self.onlineUser.configure(state=tks.NORMAL)
        self.onlineUser.insert(tks.END, self.userName  + '\n')
        self.onlineUser.configure(state=tks.DISABLED)
        

c1 = Client()
c1.gui()
        