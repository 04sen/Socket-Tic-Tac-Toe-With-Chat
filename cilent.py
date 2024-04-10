from tkinter import messagebox
import customtkinter  # <- import the CustomTkinter module

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root = customtkinter.CTk()
root.geometry("850x600")
root.title("TikTacToe")
root.resizable(False, False)
options = ["HUMAN","COMUTER"]

#button clicked function
def b_click(b):
    pass

def enter_game():
    username = root.userName_entry.get()

    #if username empty then it will display error message to users
    if (username == ''):
        messagebox.showerror("Error" ,"UserName cannot be empty")
        root.mainloop()

    else:
        root.withdraw()
        gamewindow = customtkinter.CTkToplevel()
        gamewindow.geometry("850x600")
        gamewindow.title("TikTacToe")
        gamewindow.resizable(False, False)

        #making grid frame
        gamewindow.frame = customtkinter.CTkFrame(gamewindow)
        gamewindow.frame.grid(row=3, column=3, padx=150, pady=50)

        #building buttons
        b1 = customtkinter.CTkButton(master=gamewindow.frame, text=" ",font=("Helvetica",20), height=100,width=100,
                                     hover_color=("gray70", "gray30"),fg_color="transparent",command=lambda:b_click(b1))
        b1.grid(row=0,column=0)

        b2 = customtkinter.CTkButton(master=gamewindow.frame, text=" ",font=("Helvetica",20), height=100,width=100,
                                     hover_color=("gray70", "gray30"),fg_color="transparent",command=lambda:b_click(b2))
        b2.grid(row=0,column=1)

        b3 = customtkinter.CTkButton(master=gamewindow.frame, text=" ",font=("Helvetica",20), height=100,width=100,
                                     hover_color=("gray70", "gray30"),fg_color="transparent",command=lambda:b_click(b3))
        b3.grid(row=0,column=2)

        b4 = customtkinter.CTkButton(master=gamewindow.frame, text=" ",font=("Helvetica",20), height=100,width=100,
                                     hover_color=("gray70", "gray30"),fg_color="transparent",command=lambda:b_click(b4))
        b4.grid(row=1,column=0)

        b5 = customtkinter.CTkButton(master=gamewindow.frame, text=" ",font=("Helvetica",20), height=100,width=100,
                                     hover_color=("gray70", "gray30"),fg_color="transparent",command=lambda:b_click(b5))
        b5.grid(row=1,column=1)

        b6 = customtkinter.CTkButton(master=gamewindow.frame, text=" ",font=("Helvetica",20), height=100,width=100,
                                     hover_color=("gray70", "gray30"),fg_color="transparent",command=lambda:b_click(b6))
        b6.grid(row=1,column=2)

        b7 = customtkinter.CTkButton(master=gamewindow.frame, text=" ",font=("Helvetica",20), height=100,width=100,
                                     hover_color=("gray70", "gray30"),fg_color="transparent",command=lambda:b_click(b7))
        b7.grid(row=2,column=0)

        b8 = customtkinter.CTkButton(master=gamewindow.frame, text=" ",font=("Helvetica",20), height=100,width=100,
                                     hover_color=("gray70", "gray30"),fg_color="transparent",command=lambda:b_click(b8))
        b8.grid(row=2,column=1)

        b9 = customtkinter.CTkButton(master=gamewindow.frame, text=" ",font=("Helvetica",20), height=100,width=100,
                                     hover_color=("gray70", "gray30"),fg_color="transparent",command=lambda:b_click(b9))
        b9.grid(row=2,column=2)

      
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
