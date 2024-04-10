from tkinter import messagebox
import customtkinter  # <- import the CustomTkinter module

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root = customtkinter.CTk()
root.geometry("850x600")
root.title("TikTacToe")
root.resizable(False, False)
options = ["HUMAN","COMUTER"]

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
      
#creation of userFrame
root.userName_frame = customtkinter.CTkFrame(root,)
root.userName_frame.grid(row=200, column=100, padx=150, pady=200)
#creation of UserName entry where the user enters his/her userName
root.userName_entry = customtkinter.CTkEntry(master=root.userName_frame, placeholder_text="Enter Username:",width=175, height = 33)
root.userName_entry.pack(padx=175, pady=5, )

menu = customtkinter.CTkComboBox(master=root.userName_frame, values=options)
menu.pack(pady = 5, padx = 175)

#creation of login Button for the user to login to the system
root.login_button = customtkinter.CTkButton(master=root.userName_frame, text="Enter", command=enter_game)
root.login_button.pack(side=customtkinter.LEFT,padx=200, pady=9)



root.mainloop()
