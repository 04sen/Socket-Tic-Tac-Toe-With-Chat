from tkinter import messagebox
import customtkinter  # <- import the CustomTkinter module
import socket
import random
import time
import threading

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 1234

root = customtkinter.CTk()
root.geometry("850x600")
root.title("TikTacToe")
root.resizable(False, False)
options = ["HUMAN","COMPUTER"]
clicked = True
count = 0  
HEADERSIZE = 10
EXIT_STRING = 'a72b20062ec2c47ab2ceb97ac1bee818f8b6c6cb'

#creating client-side socket and setting ipAddr + portNum
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class Game_window:
    def __init__(self):
        self.gamewindow = customtkinter.CTkToplevel()
        self.gamewindow.geometry("850x600")
        self.gamewindow.title("TikTacToe- Welcome {0}".format(root.userName_entry.get()))
        self.gamewindow.resizable(False, False)
        self.gamewindow.frame = customtkinter.CTkFrame(self.gamewindow)
        self.gamewindow.frame.grid(row=3, column=3, padx=150, pady=50)
         #creation of message box frame
        self.gamewindow.messagebox_frame = customtkinter.CTkFrame(self.gamewindow)
        self.gamewindow.messagebox_frame.place(x=500, y=100)
        #creation of message box field where all the messages can be seen 
        self.gamewindow.textbox = customtkinter.CTkTextbox(self.gamewindow.messagebox_frame, width=300, height=410)
        self.gamewindow.textbox.configure(state=customtkinter.DISABLED)
        self.gamewindow.textbox.pack(side=customtkinter.RIGHT, padx=5, pady=5)
        #creation of online users frame
        self.gamewindow.label_frame = customtkinter.CTkFrame(self.gamewindow)
        self.gamewindow.label_frame.place(x=500, y=50)
        self.gamewindow.onlineUser = customtkinter.CTkTextbox(self.gamewindow.label_frame,width=300, height=50,)
        self.gamewindow.onlineUser.insert(customtkinter.END,"Online Users:\n")
        self.gamewindow.onlineUser.configure(state=customtkinter.DISABLED)
        self.gamewindow.onlineUser.pack(side=customtkinter.RIGHT, padx=5 )
        #creation of entry field
        self.gamewindow.entry_frame = customtkinter.CTkFrame(self.gamewindow)
        self.gamewindow.entry_frame.place(x=500, y=520)
        self.gamewindow.entry = customtkinter.CTkEntry(self.gamewindow.entry_frame, width=200, height=50)
        self.gamewindow.entry.pack(side=customtkinter.LEFT, padx=5)

        #creation of send button
        self.gamewindow.send_button = customtkinter.CTkButton(self.gamewindow.entry_frame, text="Send",height=50, width=50, command=lambda:send_message(self.gamewindow,client))
        self.gamewindow.send_button.pack(side=customtkinter.RIGHT, padx=5)

        #reset button
        br = customtkinter.CTkButton(self.gamewindow, text="Restart",command=lambda:reset_brd())
        br.place(x=150, y=385)
        #quit button
        bq = customtkinter.CTkButton(self.gamewindow, text="Quit",command= lambda: quit_game())   ##quit button does not work as intended make a function that brings back root and quits out of the game window
        bq.place(x=300, y=385)

        self.board = [["" for _ in range(3)] for _ in range(3)]

       
        def button_click(row, col):
            if self.board[row][col] == "":
                print(f"Button clicked: ({row}, {col})")
                current_player = "X" if sum(row.count("X") for row in self.board) == sum(row.count("O") for row in self.board) else "O"
                # Update the board
                self.board[row][col] = current_player
                # Update the button text to the current player
                buttons[row][col].configure(text=current_player)
                send_move(row,col)

        #send the move made by the user
        def send_move(row, col):
            # Convert row and column values to integers
            row_int = int(row)
            col_int = int(col)
            
            root.username = root.userName_entry.get()
            root.username = f'{len(root.username):<{HEADERSIZE}}' + root.username
            client.send(bytes(root.username,'utf-8'))
            time.sleep(0.1)
            # Construct the message string with integers
            message = f"MOVE {row_int} {col_int}"
            message = f'{len(message):< {HEADERSIZE }}' + message

            # Encode and send the message to the server
            client.send(bytes(message, 'utf-8'))  


        def create_brd():
            global buttons
            buttons = []
            for i in range(3):
                row_buttons = []
                for j in range(3):
                    button = customtkinter.CTkButton(master=self.gamewindow.frame, text=" ", font=("Helvetica",20),
                                             height=100, width=100, hover_color=("gray70", "gray30"),
                                             fg_color="transparent", command=lambda row=i, col=j: button_click(row, col),
                                             border_width=3, border_spacing=13, border_color=("white", "white"))
                    button.grid(row=i, column=j, padx=5, pady=5)
                    row_buttons.append(button)
                buttons.append(row_buttons)
        
        create_brd()
        
            
        def highlight_winning_buttons(coords):
            for row, col in coords:
                buttons[row][col].configure(fg_color="green")

        
        def quit_game():
            disconnect(client)
            print('disconnected from server')
            self.gamewindow.destroy()
            root.destroy()

            client.shutdown(socket.SHUT_RDWR)
            client.close()

        def reset_brd():
            root.username = root.userName_entry.get()
            reset_msg = "RESET"
            root.username = f'{len(root.username):<{HEADERSIZE}}' + root.username
            client.send(bytes(root.username,'utf-8'))
            time.sleep(0.1)
            reset_msg = f'{len(reset_msg):<{HEADERSIZE}}' + reset_msg
            client.send(bytes(reset_msg,'utf-8'))
            
            create_brd()
            self.board = [["" for _ in range(3)] for _ in range(3)]

           
           
        def disconnect(client):
            root.username = root.userName_entry.get()
            exit_msg = EXIT_STRING

            root.username = f'{len(root.username):<{HEADERSIZE}}' + root.username
            client.send(bytes(root.username,'utf-8'))

            time.sleep(0.1)
            
            exit_msg = f'{len(exit_msg):<{HEADERSIZE}}' + exit_msg
            client.send(bytes(exit_msg,'utf-8'))

        #starts a thread that listens from messages from server
        thread = threading.Thread(target=listen_for_messages_from_server, args=(self,client ))
        thread.start()

            

#function send_message sends the message to all other clients
def send_message(self,client):
    
    #Gets message entered by the user
    self.message = self.entry.get()
    root.username = root.userName_entry.get()
    
    #checks if message is not empty
    if self.message != '':
        root.username = f'{len(root.username):<{HEADERSIZE}}' + root.username
        client.send(bytes(root.username,'utf-8'))

        time.sleep(0.1)

        self.message = f'{len(self.message):<{HEADERSIZE}}' + self.message
        #sends message to all active clients 
        client.send(bytes(self.message,'utf-8'))
        
        #deletes the message entered by the user in the message box
        self.entry.delete(0, len(self.message))
    
    #checks if message is empty, then it will display a error message
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")
        self.entry.delete(0, customtkinter.END)
        pass


def enter_game():

    username = root.userName_entry.get()

    #if username empty then it will display error message to users
    if (username == ''):
        messagebox.showerror("Error" ,"UserName cannot be empty")
        root.mainloop()

    #else withdraws the old window and calls Game_Window Class
    else:
        connect(root) # <--  Connect to Server
        root.withdraw() # <-- Withdraw root window


        c1=Game_window()


#function that is used to connect the client to the server
def connect(self):

    #Generate a random IPv4 address while keeping the first octet as '127'
    def generate_random_ipv4_address():
        octets = ['127']
        for i in range(1, 4):
            octets.append(str(random.randint(0, 255)))
        return '.'.join(octets)
    # Generate a random integer between 1024 and 65535
    def generate_random_port_number():
        port_number = random.randint(1024, 65535)
        return port_number

    ipAddress = generate_random_ipv4_address()
    portNum = generate_random_port_number() 

    print(ipAddress)
    print(portNum)

        #Binding socket to IP and Port
    try:
        client.bind((ipAddress,portNum))
        print(f"Client set to ({ipAddress}, {portNum})")
    except:
        print(f"Unable to bind to {ipAddress} and port {ipAddress}")

        
    #gets the username user and stores in username 
    self.username = self.userName_entry.get()
    self.menuOption = self.menu.get()
    
    # try except block
    try:
        # Connect to the server
        client.connect((SERVER_HOST, SERVER_PORT))


        self.username = f'{len(self.username):<{HEADERSIZE}}' + self.username


        client.send(bytes(self.username,'utf-8'))
        time.sleep(0.1)
        self.menuOption = f'{len(self.menuOption):<{HEADERSIZE}}' + self.menuOption
        client.send(bytes(self.menuOption,'utf-8'))

        print("Successfully connected to server")
        
    #if the user wasnt able to connect to server then it will show error message
    except:
        messagebox.showerror("Unable to connect to server", f"Unable to connect to server {self.HOST} {self.PORT}")
        root.mainloop()


# listens for message from all active clients
def  listen_for_messages_from_server(self,client):
    #runs in an infinite loop to listen for messages
    while 1:
            #receives upto 1024 bytes of data and decodes using utf-8
            message = client.recv(1024).decode('utf-8')
            print(message)
            
            #checks if message is Active Users
            if message.startswith("["):
                #adds into Label
                add_onlineUser(self.gamewindow,message)
                message = ''
            elif message.startswith("MOVE"):
                _, row_str, col_str = message.split()
                row = int(row_str)
                col = int(col_str)
                current_player = "X" if sum(row.count("X") for row in self.board) == sum(row.count("O") for row in self.board) else "O"
                # Update the board
                self.board[row][col] = current_player
                # Update the button text to the current player
                buttons[row][col].configure(text=current_player)
            elif message.startswith("You win!"):
                #messagebox to send if user wins
                pass
            elif message.startswith("Tie game!"):
                #messagebox to send if tie happens
                pass
            elif message.startswith("Server wins!"):
                #messagebox to sebd if server wins
                pass
            else:
                add_message(self.gamewindow,message)
                message = ''

#adds message in message box
def add_message(self,message):
    self.textbox.configure(state=customtkinter.NORMAL)
    self.textbox.insert(customtkinter.END, message + '\n')
    self.textbox.configure(state=customtkinter.DISABLED)
        
#adds message in message box
def add_onlineUser(self,message):
    self.onlineUser.pack_forget()
    self.onlineUser = customtkinter.CTkTextbox(self.label_frame,width=300, height=50,)
    self.onlineUser.configure(state=customtkinter.NORMAL)
    self.onlineUser.insert(customtkinter.END,"Online Users:\n")
    self.onlineUser.insert(customtkinter.END,message)
    self.onlineUser.configure(state=customtkinter.DISABLED)
    self.onlineUser.pack(side=customtkinter.RIGHT, padx=5 )
   

#creation of userFrame
root.userName_frame = customtkinter.CTkFrame(root,)
root.userName_frame.grid(row=3, column=1, padx=150, pady=200)
#creation of UserName entry where the user enters his/her userName
root.userName_entry = customtkinter.CTkEntry(master=root.userName_frame, placeholder_text="Enter Username:",width=175, height = 33)
root.userName_entry.pack(padx=175, pady=5, )

root.menu = customtkinter.CTkComboBox(master=root.userName_frame, values=options)
root.menu.pack(pady = 5, padx = 175)

#creation of login Button for the user to login to the system
root.login_button = customtkinter.CTkButton(master=root.userName_frame, text="Enter", command=enter_game)
root.login_button.pack(side=customtkinter.LEFT,padx=200, pady=9)
#creating a label
label_frame = customtkinter.CTkFrame(root, width=500, height=100)
label_frame.place(x=150, y=80)
label = customtkinter.CTkLabel(master=label_frame, text="WELCOME TO Tic Tac Toe the game \n please enter your username to continue to play the game   ",width=500, height=50)
label.pack()
root.mainloop()