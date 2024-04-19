# Copyright (c) [2024] [Sachinandan Das Sen, Shamal Kurmar, Shivneel Narayan]
# This file is part of [CS310-2024], which is released under the MIT License.
# See LICENSE.md for details or visit https://opensource.org/licenses/MIT.

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
        self.player_status = " " 
        self.board = [["" for _ in range(3)] for _ in range(3)]

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
        #creation of Player Status Label:
        self.gamewindow.player_status_label = customtkinter.CTkLabel(self.gamewindow, text= "Waiting for Connection...", 
                                                                     fg_color="#3b3b3b",font=("Helvetica",15), padx =10, pady =10,corner_radius=5)
        self.gamewindow.player_status_label.place(x=220 ,y=450) 
        #creation of entry field
        self.gamewindow.entry_frame = customtkinter.CTkFrame(self.gamewindow)
        self.gamewindow.entry_frame.place(x=500, y=520)
        self.gamewindow.entry = customtkinter.CTkEntry(self.gamewindow.entry_frame, width=200, height=50)
        self.gamewindow.entry.pack(side=customtkinter.LEFT, padx=5)

        #creation of send button
        self.gamewindow.send_button = customtkinter.CTkButton(self.gamewindow.entry_frame, text="Send",height=50, width=50, command=lambda:send_message(self.gamewindow,client))
        self.gamewindow.send_button.pack(side=customtkinter.RIGHT, padx=5)

         #reset button
        self.gamewindow.br = customtkinter.CTkButton(self.gamewindow, text="Restart",command=lambda:reset_brd())
        self.gamewindow.br.place(x=150, y=385)
        #quit button
        bq = customtkinter.CTkButton(self.gamewindow, text="Quit",command= lambda: quit_game())   ##quit button does not work as intended make a function that brings back root and quits out of the game window
        bq.place(x=300, y=385)  

        if root.menu.get() == "HUMAN":
            self.gamewindow.br.configure(state="disabled")

        create_brd()
        disable_all_buttons()
        
        #starts a thread that listens from messages from server
        thread = threading.Thread(target=listen_for_messages_from_server, args=(self,client ))
        thread.start()

        #---------------------------------------------------------------------------------

        def button_click(row, col):
            global winner
            winner = False
            #checks if button is clicked
            if not winner and self.board[row][col] == "":
                print(f"Button clicked: ({row}, {col})")
                current_player = "X" if sum(row.count("X") for row in self.board) == sum(row.count("O") for row in self.board) else "O"
                # Update the board
                self.board[row][col] = current_player
                # Update the button text to the current player
                buttons[row][col].configure(text=current_player)
                send_move(row,col)
        
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

        def reset_brd():
            reset_msg = "RESET"
            reset_msg = f'{len(reset_msg):<{HEADERSIZE}}' + reset_msg
            client.send(bytes(reset_msg,'utf-8'))
            
            create_brd()
            self.board = [["" for _ in range(3)] for _ in range(3)]     
        
        #---------------------------------------------------------------------------------

        #send the move made by the user
        def send_move(row, col):
            # Convert row and column values to integers
            row_int = int(row)
            col_int = int(col)
            
            # Construct the message string with integers
            if self.player_status == " X":
                message = f"X MOVE {row_int} {col_int}"
                message = f'{len(message):< {HEADERSIZE }}' + message
                client.send(bytes(message, 'utf-8'))  
                disable_all_buttons()
            elif self.player_status == "O":
                message = f" O MOVE {row_int} {col_int}"
                message = f'{len(message):< {HEADERSIZE }}' + message

            message = f"MOVE {row_int} {col_int}"
            message = f'{len(message):< {HEADERSIZE }}' + message

            # Encode and send the message to the server
            client.send(bytes(message, 'utf-8')) 

        #---------------------------------------------------------------------------------
                  
        def quit_game():
            disconnect(client)
            print('disconnected from server')
            self.gamewindow.destroy()
            root.destroy()

            client.shutdown(socket.SHUT_RDWR)
            client.close()
                   
        def disconnect(client):
            root.username = root.userName_entry.get()
            exit_msg = EXIT_STRING

            root.username = f'{len(root.username):<{HEADERSIZE}}' + root.username
            client.send(bytes(root.username,'utf-8'))

            time.sleep(0.1)
            
            exit_msg = f'{len(exit_msg):<{HEADERSIZE}}' + exit_msg
            client.send(bytes(exit_msg,'utf-8'))       

        #---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------

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
            if message.startswith("|"):
                #adds into Label
                add_onlineUser(self.gamewindow,message)
                message = ''
            elif message.startswith("COMPUTER_MOVE"):
                _, row_str, col_str = message.split()
                row = int(row_str)
                col = int(col_str)
                current_display = "X" if sum(row.count("X") for row in self.board) == sum(row.count("O") for row in self.board) else "O"
                # Update the board
                self.board[row][col] = current_display
                # Update the button text to the current player
                buttons[row][col].configure(text=current_display)

            elif message.startswith("You win!") or message.startswith("Server wins!") or message.startswith("Tie game!") or message.startswith("X wins!") or message.startswith("O wins!"):
                for i in range(3):
                    if self.board[i][0] == self.board[i][1] == self.board[i][2] != "":
                        winner = True
                        highlight_winning_buttons([(i, 0), (i, 1), (i, 2)])
                        messagebox.showinfo("Winner", f"Player {self.board[i][0]} is the winner")

                # Vertical
                for i in range(3):
                    if self.board[0][i] == self.board[1][i] == self.board[2][i] != "":
                        winner = True
                        highlight_winning_buttons([(0, i), (1, i), (2, i)])
                        messagebox.showinfo("Winner", f"Player {self.board[0][i]} is the winner")                   

                # Diagonals
                if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":

                    winner = True
                    messagebox.showinfo("Winner", f"Player {self.board[0][0]} is the winner")
                    highlight_winning_buttons([(0, 0), (1, 1), (2, 2)])

                elif self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
                    winner = True
                    messagebox.showinfo("Winner", f"Player {self.board[0][2]} is the winner")
                    highlight_winning_buttons([(0, 2), (1, 1), (2, 0)])
                else:
                    add_message(self.gamewindow,message)
                    message = ''
                disable_all_buttons()
                
            elif message == "You are connected, You are O":
                self.player_status = "O"
                self.gamewindow.player_status_label.configure(text="You are Player O\nWait for your Turn")
                disable_all_buttons()
                print("Waiting for Move")
            
            elif message == "You are connected, You are X":
                self.player_status = "X"
                self.gamewindow.player_status_label.configure(text="You are Player X\nMake a MOVE")
                enable_all_buttons()
            
            elif message.startswith("Player X"):
                if self.player_status == "X":
                    disable_all_buttons()
                    self.gamewindow.player_status_label.configure(text="Waiting for Player O")
                elif self.player_status == "O":
                    enable_all_buttons()
                    _, _, row_str, col_str = message.split()
                    row = int(row_str)
                    col = int(col_str)
                    current_display = "X" if sum(row.count("X") for row in self.board) == sum(row.count("O") for row in self.board) else "O"
                    # Update the board
                    self.board[row][col] = current_display
                    # Update the button text to the current player
                    buttons[row][col].configure(text=current_display)
                    self.gamewindow.player_status_label.configure(text="Make A Move...")
                print(message)
                
            elif message.startswith("Player O"):
                if self.player_status == "O":
                    disable_all_buttons()
                    self.gamewindow.player_status_label.configure(text="Waiting for Player O")
                elif self.player_status == "X":
                    enable_all_buttons()
                    _, _, row_str, col_str = message.split()
                    row = int(row_str)
                    col = int(col_str)
                    current_display = "X" if sum(row.count("X") for row in self.board) == sum(row.count("O") for row in self.board) else "O"
                    # Update the board
                    self.board[row][col] = current_display
                    # Update the button text to the current player
                    buttons[row][col].configure(text=current_display)
                    self.gamewindow.player_status_label.configure(text="Make A Move...")
                print(message)
            else:
                add_message(self.gamewindow,message)
                message = ''

#---------------------------------------------------------------------------------

#function send_message sends the message to all other clients
def send_message(self,client):
    
    #Gets message entered by the user
    self.message = self.entry.get()
    root.username = root.userName_entry.get()
    
    #checks if message is not empty
    if self.message != '':
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
   
#---------------------------------------------------------------------------------

def highlight_winning_buttons(coords):
    for row, col in coords:
        buttons[row][col].configure(fg_color="green")
        
def disable_all_buttons():
    for row in buttons:
        for button in row:
            button.configure(state="disabled")

def enable_all_buttons():
    for row in buttons:
        for button in row:
            button.configure(state="enabled")
            
#---------------------------------------------------------------------------------

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