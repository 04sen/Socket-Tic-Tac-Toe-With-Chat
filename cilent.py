from tkinter import messagebox
import customtkinter  # <- import the CustomTkinter module
from PIL import Image, ImageTk
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root = customtkinter.CTk()
root.geometry("850x600")
root.title("TikTacToe")
root.resizable(False, False)
options = ["HUMAN","COMUTER"]
clicked = True
count = 0  
class Game_window:
    def __init__(self):
        gamewindow = customtkinter.CTkToplevel()
        gamewindow.geometry("850x600")
        gamewindow.title("TikTacToe")
        gamewindow.resizable(False, False)
        gamewindow.frame = customtkinter.CTkFrame(gamewindow)
        gamewindow.frame.grid(row=3, column=3, padx=150, pady=50)
        b1 = customtkinter.CTkButton(master=gamewindow.frame, text=" ",font=("Helvetica",20), height=100,width=100,
                                            hover_color=("gray70", "gray30"),fg_color="transparent",command=lambda:b_click(b1),border_width=3,border_spacing= 13,
                                            border_color=("white","white"))
        b2 = customtkinter.CTkButton(master=gamewindow.frame, text=" ",font=("Helvetica",20), height=100,width=100,
                                    hover_color=("gray70", "gray30"),fg_color="transparent",command=lambda:b_click(b2),border_width=3,border_spacing= 13,
                                    border_color=("white","white"))
        b3 = customtkinter.CTkButton(master=gamewindow.frame, text=" ",font=("Helvetica",20), height=100,width=100,
                                    hover_color=("gray70", "gray30"),fg_color="transparent",command=lambda:b_click(b3),border_width=3,border_spacing= 13,
                                    border_color=("white","white"))
        b4 = customtkinter.CTkButton(master=gamewindow.frame, text=" ",font=("Helvetica",20), height=100,width=100,
                                    hover_color=("gray70", "gray30"),fg_color="transparent",command=lambda:b_click(b4),border_width=3,border_spacing= 13,
                                    border_color=("white","white"))
        b5 = customtkinter.CTkButton(master=gamewindow.frame, text=" ",font=("Helvetica",20), height=100,width=100,
                                    hover_color=("gray70", "gray30"),fg_color="transparent",command=lambda:b_click(b5),border_width=3,border_spacing= 13,
                                    border_color=("white","white"))
        b6 = customtkinter.CTkButton(master=gamewindow.frame, text=" ",font=("Helvetica",20), height=100,width=100,
                                    hover_color=("gray70", "gray30"),fg_color="transparent",command=lambda:b_click(b6),border_width=3,border_spacing= 13,
                                    border_color=("white","white"))
        b7 = customtkinter.CTkButton(master=gamewindow.frame, text=" ",font=("Helvetica",20), height=100,width=100,
                                    hover_color=("gray70", "gray30"),fg_color="transparent",command=lambda:b_click(b7),border_width=3,border_spacing= 13,
                                    border_color=("white","white"))
        b8 = customtkinter.CTkButton(master=gamewindow.frame, text=" ",font=("Helvetica",20), height=100,width=100,
                                            hover_color=("gray70", "gray30"),fg_color="transparent",command=lambda:b_click(b8),border_width=3,border_spacing= 13,
                                            border_color=("white","white"))
        b9 = customtkinter.CTkButton(master=gamewindow.frame, text=" ",font=("Helvetica",20), height=100,width=100,
                                            hover_color=("gray70", "gray30"),fg_color="transparent",command=lambda:b_click(b9),border_width=3,border_spacing= 13,
                                            border_color=("white","white"))
        b1.grid(row=0,column=0)
        b2.grid(row=0,column=1)
        b3.grid(row=0,column=2)
        b4.grid(row=1,column=0)
        b5.grid(row=1,column=1)
        b6.grid(row=1,column=2)
        b7.grid(row=2,column=0)
        b8.grid(row=2,column=1)
        b9.grid(row=2,column=2)
        br = customtkinter.CTkButton(gamewindow, text="Restart")
        br.place(x=150, y=375)
        def disable_all_buttons():
            b1.configure(state="disabled")
            b2.configure(state="disabled")
            b3.configure(state="disabled")
            b4.configure(state="disabled")
            b5.configure(state="disabled")
            b6.configure(state="disabled")
            b7.configure(state="disabled")
            b8.configure(state="disabled")
            b9.configure(state="disabled")

        #check if won
        def check_winner():
            global winner
            winner = False
            #horizontal
            if b1.cget("text") == "X" and b2.cget("text") == "X" and b3.cget("text") == "X":
                b1.configure(fg_color="green")
                b2.configure(fg_color="green")
                b3.configure(fg_color="green")
                winner = True
                messagebox.showinfo("Winner", "Player X is the winner")
                disable_all_buttons()
            elif b4.cget("text") == "X" and b5.cget("text") == "X" and b6.cget("text") == "X":
                b4.configure(fg_color="green")
                b5.configure(fg_color="green")
                b6.configure(fg_color="green")
                winner = True
                messagebox.showinfo("Winner", "Player X is the winner")
                disable_all_buttons()
            elif b7.cget("text") == "X" and b8.cget("text") == "X" and b9.cget("text") == "X":
                b7.configure(fg_color="green")
                b8.configure(fg_color="green")
                b9.configure(fg_color="green")
                winner = True
                messagebox.showinfo("Winner", "Player X is the winner")
                disable_all_buttons()
            #vertical
            elif b1.cget("text") == "X" and b4.cget("text") == "X" and b7.cget("text") == "X":
                b1.configure(fg_color="green")
                b4.configure(fg_color="green")
                b7.configure(fg_color="green")
                winner = True
                messagebox.showinfo("Winner", "Player X is the winner")
                disable_all_buttons()
            elif b2.cget("text") == "X" and b5.cget("text") == "X" and b8.cget("text") == "X":
                b2.configure(fg_color="green")
                b5.configure(fg_color="green")
                b8.configure(fg_color="green")
                winner = True
                messagebox.showinfo("Winner", "Player X is the winner")
                disable_all_buttons()
            elif b3.cget("text") == "X" and b6.cget("text") == "X" and b9.cget("text") == "X":
                b3.configure(fg_color="green")
                b6.configure(fg_color="green")
                b9.configure(fg_color="green")
                winner = True
                messagebox.showinfo("Winner", "Player X is the winner")
                disable_all_buttons()
            #diagnols
            elif b1.cget("text") == "X" and b5.cget("text") == "X" and b9.cget("text") == "X":
                b1.configure(fg_color="green")
                b5.configure(fg_color="green")
                b9.configure(fg_color="green")
                winner = True
                messagebox.showinfo("Winner", "Player X is the winner")
                disable_all_buttons()
            elif b3.cget("text") == "X" and b5.cget("text") == "X" and b7.cget("text") == "X":
                b3.configure(fg_color="green")
                b5.configure(fg_color="green")
                b7.configure(fg_color="green")
                winner = True
                messagebox.showinfo("Winner", "Player X is the winner")
                disable_all_buttons()
        #check for O
            elif b1.cget("text") == "O" and b2.cget("text") == "O" and b3.cget("text") == "O":
                b1.configure(fg_color="green")
                b2.configure(fg_color="green")
                b3.configure(fg_color="green")
                winner = True
                messagebox.showinfo("Winner", "Player O is the winner")
                disable_all_buttons()
            elif b4.cget("text") == "O" and b5.cget("text") == "O" and b6.cget("text") == "O":
                b4.configure(fg_color="green")
                b5.configure(fg_color="green")
                b6.configure(fg_color="green")
                winner = True
                messagebox.showinfo("Winner", "Player O is the winner")
                disable_all_buttons()
            elif b7.cget("text") == "O" and b8.cget("text") == "O" and b9.cget("text") == "O":
                b7.configure(fg_color="green")
                b8.configure(fg_color="green")
                b9.configure(fg_color="green")
                winner = True
                messagebox.showinfo("Winner", "Player O is the winner")
                disable_all_buttons()
            #vertical
            elif b1.cget("text") == "O" and b4.cget("text") == "O" and b7.cget("text") == "O":
                b1.configure(fg_color="green")
                b4.configure(fg_color="green")
                b7.configure(fg_color="green")
                winner = True
                messagebox.showinfo("Winner", "Player O is the winner")
                disable_all_buttons()
            elif b2.cget("text") == "O" and b5.cget("text") == "O" and b8.cget("text") == "O":
                b2.configure(fg_color="green")
                b5.configure(fg_color="green")
                b8.configure(fg_color="green")
                winner = True
                messagebox.showinfo("Winner", "Player O is the winner")
                disable_all_buttons()
            elif b3.cget("text") == "O" and b6.cget("text") == "O" and b9.cget("text") == "O":
                b3.configure(fg_color="green")
                b6.configure(fg_color="green")
                b9.configure(fg_color="green")
                winner = True
                messagebox.showinfo("Winner", "Player O is the winner")
                disable_all_buttons()
            #diagnols
            elif b1.cget("text") == "O" and b5.cget("text") == "O" and b9.cget("text") == "O":
                b1.configure(fg_color="green")
                b5.configure(fg_color="green")
                b9.configure(fg_color="green")
                winner = True
                messagebox.showinfo("Winner", "Player O is the winner")
                disable_all_buttons()
            elif b3.cget("text") == "O" and b5.cget("text") == "O" and b7.cget("text") == "O":
                b3.configure(fg_color="green")
                b5.configure(fg_color="green")
                b7.configure(fg_color="green")
                winner = True
                messagebox.showinfo("Winner", "Player O is the winner")
                disable_all_buttons()
            
        #button clicked function
        def b_click(b):
            global clicked, count
            
            if b.cget("text") == " " and clicked == True:
                b.configure(text = "X")
                clicked = False
                count += 1
                check_winner()
            elif b.cget("text") == " " and clicked == False:
                b.configure(text = "O")
                clicked = True
                count += 1
                check_winner()
            else:
                messagebox.showerror("Error", "This box has already been selected\nPick another box...")
def enter_game():
    username = root.userName_entry.get()

    #if username empty then it will display error message to users
    if (username == ''):
        messagebox.showerror("Error" ,"UserName cannot be empty")
        root.mainloop()

    else:
        root.withdraw()
        c1=Game_window()
#creation of userFrame
root.userName_frame = customtkinter.CTkFrame(root,)
root.userName_frame.grid(row=3, column=1, padx=150, pady=200)
#creation of UserName entry where the user enters his/her userName
root.userName_entry = customtkinter.CTkEntry(master=root.userName_frame, placeholder_text="Enter Username:",width=175, height = 33)
root.userName_entry.pack(padx=175, pady=5, )

menu = customtkinter.CTkComboBox(master=root.userName_frame, values=options)
menu.pack(pady = 5, padx = 175)

#creation of login Button for the user to login to the system
root.login_button = customtkinter.CTkButton(master=root.userName_frame, text="Enter", command=enter_game)
root.login_button.pack(side=customtkinter.LEFT,padx=200, pady=9)



root.mainloop()
