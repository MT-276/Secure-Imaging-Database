#-------------------------------------------------------------------------------
# Name:        Account_login_GUI.py
#
# Author:      MS Productions
#
# Created:     09 04 2023
# Copyright:   (c)MS Productions
#
# Lead Dev : Meit Sant
#-------------------------------------------------------------------------------

from tkinter import *
import tkinter.messagebox as mb
from tkinter import simpledialog
from PIL import ImageTk, Image
import ED, os, sys, time, sqlite3
global Username, Password,UName,Pwd,AccType

connector = sqlite3.connect('Image_database.db')
connector.execute("CREATE TABLE IF NOT EXISTS Acc_database (Acc_ID INTEGER PRIMARY KEY AUTOINCREMENT, AccNAME VARCHAR(30), Pwd VARCHAR(30),AccType Varchar(30))")

def Login():
    global Username, Password,UName,Pwd,AccType
    UName = Username.get()
    Pwd = Password.get()

    query = "SELECT * FROM Acc_database WHERE AccNAME = ? AND Pwd = ?"
    result = connector.execute(query, (UName, Pwd)).fetchone()
    if result:
        AccType = result[3]
        Login_win.destroy()
    else:
        mb.showerror("Error", "Invalid username or password")

def Register():
    global Username, Password
    UName = Username.get()
    Pwd = Password.get()

    if admin_var.get() == 1:
        admin_password = simpledialog.askstring("Admin Password", "Enter Admin Password:", show='*')
        if admin_password == ";lkjasdf1212":
            query = "INSERT INTO Acc_database (AccNAME, Pwd, AccType) VALUES (?, ?, ?)"
            connector.execute(query, (UName, Pwd, "Admin"))
            connector.commit()
            mb.showinfo("Success", "Registration successful")
            Username.delete(0, END)
            Password.delete(0, END)
        else:
            mb.showerror("Error", "Incorrect Admin Password")
    else:
        query = "INSERT INTO Acc_database (AccNAME, Pwd) VALUES (?, ?)"
        connector.execute(query, (UName, Pwd))
        connector.commit()
        mb.showinfo("Success", "Registration successful")
        Username.delete(0, END)
        Password.delete(0, END)

def UI():
    global Login_win, Username, Password, admin_var

    Login_win = Tk()

    Login_window_colour = '#28293F'
    Frame_colour = '#1C2028'
    Font = ("Bahnschrift Bold", 12)

    Login_win.title("Secure Imaging Database")
    Login_win.geometry('400x500')
    Login_win.configure(bg=Login_window_colour)

    Frame_ = Frame(Login_win, background=Frame_colour)
    Frame_.place(x=30, y=25, relheight=0.9, relwidth=0.85)


    image_path = "./Assets/Acc_img.png"                                                   # Load the image
    image = Image.open(image_path)
    new_size = (100, 100)
    image = image.resize(new_size, Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)


    image_label = Label(Frame_, image=photo, borderwidth=0, highlightthickness=0)         # Create a label to display the image

    image_label.image = photo                                                             # Store reference to avoid garbage collection
    image_label.place(relx=0.4, rely=0.15)

    Label(Frame_, text="Username :", font=("Bahnschrift", 15), fg="white", bg=Frame_colour).place(relx=0.1, rely=0.49)
    Username = Entry(Frame_, bg=Frame_colour, fg='white', font=("Bahnschrift", 12))
    Username.place(relx=0.38, rely=0.5, relheight=0.05, relwidth=0.5)

    Label(Frame_, text="Password :", font=("Bahnschrift", 15), fg="white", bg=Frame_colour).place(relx=0.1, rely=0.59)
    Password = Entry(Frame_, bg=Frame_colour, fg='white', font=("Bahnschrift", 12), show="*")
    Password.place(relx=0.4, rely=0.6, relheight=0.05, relwidth=0.5)

    Button(Frame_, text='Login', bg=Frame_colour, fg='white', font=("Bahnschrift Semibold", 20), command=Login).place(relx=0.2, rely=0.8)

    admin_var = IntVar()

    Checkbutton(Frame_, text="Register as Admin", variable=admin_var, bg=Frame_colour, fg='white',
                font=("Bahnschrift Light", 10)).place(relx=0.5, rely=0.75)

    Button(Frame_, text='Register', bg=Frame_colour, fg='white', font=("Bahnschrift Semibold", 20),
           command=Register).place(relx=0.5, rely=0.8)

    Login_win.mainloop()

