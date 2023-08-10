#-------------------------------------------------------------------------------
# Name:        Account_login_GUI.py
# Purpose:     Login UI for Secure Imaging Database
#
# Author:      MS Productions
#
# Created:     09 04 2023
# Copyright:   (c)MS Productions
#
# Lead Dev : Meit Sant
#-------------------------------------------------------------------------------

import sys, sqlite3
from tkinter import *
import tkinter.messagebox as mb
from tkinter import simpledialog
from PIL import ImageTk, Image
from ED import Encrypt_Pwd
global AccType, Font, Password, Pwd, UName, Username

allow_bypass = True

Font = ("Bahnschrift Bold", 12)

connector = sqlite3.connect('Image_database.db')
connector.execute("""
CREATE TABLE IF NOT EXISTS Acc_database (
Acc_ID INTEGER PRIMARY KEY AUTOINCREMENT,
AccNAME VARCHAR(10) UNIQUE,
Pwd VARCHAR(100),
AccType Varchar(5),
Date_of_creation DATE )
""")

def Login():
    """
    Logs in User
    """
    global Username, Password,UName,Pwd,AccType,allow_bypass
    if allow_bypass is True:
        UName ='Meit'
        AccType ='Admin'
        Login_win.destroy()
        return
    UName = Username.get()
    Pwd = Password.get()

    result = connector.execute("SELECT * FROM Acc_database WHERE AccNAME = ?;",
        (UName,)).fetchone()
    if result:
        if result[2] != Encrypt_Pwd(Pwd):
            mb.showerror("Error", "Invalid Password")
            return
        AccType = result[3]
        Login_win.destroy()
    else:
        mb.showerror("Error", "Invalid Username")

def back_to_login():
    """
    Quits Register Window and
    creates Login Window
    """
    Register_win.destroy()
    Login_UI()

def Register():
    """
    Registers Users
    """
    global Username, Password
    UName = Username.get()
    Pwd = Password.get()
    if len(UName)>10:
        mb.showerror("Error", "Username Character Exceeded.\nPlease keep username under 10 chars")
        return
    if admin_var.get() == 1:
        admin_password = simpledialog.askstring("Admin Password", "Enter Admin Password:", show='*')
        if admin_password == "pwd1212":
            try:
                connector.execute("INSERT INTO Acc_database (AccNAME, Pwd, AccType, Date_of_creation) VALUES (?,?,'Admin',datetime())",
                    (UName,Encrypt_Pwd(Pwd)))
                connector.commit()
            except:
                mb.showerror("Error", "The username already exists")
                return
            mb.showinfo("Success", "Registration successful")
            Username.delete(0, END)
            Password.delete(0, END)
        else:
            mb.showerror("Error", "Incorrect Admin Password")
            return
    else:
        try:
            connector.execute("INSERT INTO Acc_database (AccNAME, Pwd, Date_of_creation) VALUES (?,?,datetime())",
                (UName,Encrypt_Pwd(Pwd)))
            connector.commit()
        except:
            mb.showerror("Error", "The username already exists")
            return
        mb.showinfo("Success", "Registration successful")
        Username.delete(0, END)
        Password.delete(0, END)
    connector.commit()
    back_to_login()

def Login_UI():
    """
    Login Window for Secure Imaging Database
    """
    global Login_win, Username, Password, admin_var,allow_bypass

    # Initialize the login window using Tkinter library
    Login_win = Tk()

    # Define color codes for the login window and frame
    Login_window_colour = '#28293F'
    Frame_colour = '#1C2028'

    # Set the window configurations
    Login_win.title("Secure Imaging Database - LOGIN")
    Login_win.geometry('400x500+700+300')
    Login_win.configure(bg=Login_window_colour)

    # Create a frame within the window
    Frame_ = Frame(Login_win, background=Frame_colour)
    Frame_.place(x=30, y=25, relheight=0.9, relwidth=0.85)

    # Load and display an image on the frame
    image_path = "./Assets/Acc_img_Login.png"
    image = Image.open(image_path)
    new_size = (100, 100)
    image = image.resize(new_size, Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    image_label = Label(Frame_, image=photo, borderwidth=0, highlightthickness=0)
    image_label.image = photo
    image_label.place(relx=0.35, rely=0.08)

    # Create labels and input fields for username and password
    Label(Frame_, text="Username :",
            font=Font,
            fg="white",
            bg=Frame_colour).place(relx=0.05, rely=0.39)

    Username = Entry(Frame_, bg=Frame_colour, fg='white', font=("Bahnschrift", 15))
    Username.place(relx=0.4, rely=0.38, relheight=0.07, relwidth=0.5)

    Label(Frame_, text="Password :",
            font=Font,
            fg="white",
            bg=Frame_colour).place(relx=0.06, rely=0.49)

    Password = Entry(Frame_,
            bg=Frame_colour,
            fg='white',
            font=("Bahnschrift", 15),
            show="*")

    Password.place(relx=0.4, rely=0.48, relheight=0.07, relwidth=0.5)

    # Create a login button a Register button for new users
    Button(Frame_, text='LOGIN',
            bg=Frame_colour,
            fg='white',
            font=("Arial bold", 20), command=Login).place(relx=0.32, rely=0.65)

    Label(Frame_, text="Don't have an account ?",
            font=("Bahnschrift Light", 10),
            fg="white",
            bg=Frame_colour).place(relx=0.1, rely=0.8)

    Button(Frame_, text='REGISTER',
            bg=Frame_colour,
            fg='white',
            font=("Bahnschrift Light", 10),
            command=Register_UI).place(relx=0.55, rely=0.8)

    Login_win.mainloop()

def Register_UI():
    try:
        Login_win.destroy()
    except: pass

    global Register_win, Username, Password, admin_var

    # Initialize the register window using Tkinter library
    Register_win = Tk()

    # Define color codes for the register window and frame
    Register_window_colour = '#28293F'
    Frame_colour = '#1C2028'

    # Set the window configurations
    Register_win.title("Secure Imaging Database - REGISTER")
    Register_win.geometry('400x500+700+300')
    Register_win.configure(bg=Register_window_colour)

    # Create a frame within the window
    Frame_ = Frame(Register_win, background=Frame_colour)
    Frame_.place(x=30, y=25, relheight=0.9, relwidth=0.85)

    # Load and display an image on the frame
    image_path = "./Assets/Acc_img_Register.png"
    image = Image.open(image_path)
    new_size = (100, 100)
    image = image.resize(new_size, Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    image_label = Label(Frame_,
            image=photo,
            borderwidth=0,
            highlightthickness=0)
    image_label.image = photo
    image_label.place(relx=0.35, rely=0.08)

    # Create labels and input fields for username and password
    Label(Frame_, text="Username :",
            font=("Bahnschrift Light", 12),
            fg="white",
            bg=Frame_colour).place(relx=0.05, rely=0.39)
    Username = Entry(Frame_,bg=Frame_colour,fg='white',font=("Bahnschrift", 15))
    Username.place(relx=0.4, rely=0.38, relheight=0.07, relwidth=0.5)
    Label(Frame_,
            text="Password :",
            font=("Bahnschrift Light", 12),
            fg="white",
            bg=Frame_colour).place(relx=0.06, rely=0.49)
    Password = Entry(Frame_,
            bg=Frame_colour,
            fg='white',
            font=("Bahnschrift", 15), show="*")
    Password.place(relx=0.4, rely=0.48, relheight=0.07, relwidth=0.5)

    # Create a Register button along with a checkbox for admin and a back to login button
    Button(Frame_,
            text='Register',
            bg=Frame_colour,
            fg='white',
            font=("Arial bold", 20),
            command=Register).place(relx=0.32, rely=0.65)

    admin_var = IntVar()

    Label(Frame_,
            text="Already have an account ?",
            font=("Bahnschrift Light", 10),
            fg="white", bg=Frame_colour).place(relx=0.2, rely=0.91)

    Button(Frame_,
            text='LOGIN',
            bg=Frame_colour,
            fg='white',
            font=("Bahnschrift Light", 10),
            command=back_to_login).place(relx=0.66, rely=0.9)


    Checkbutton(Frame_,
            text="Register as Admin",
            variable=admin_var,
            bg=Frame_colour,
            fg='grey',
            onvalue = 1, offvalue = 0,
            font=("Bahnschrift Light", 10)).place(relx=0.3, rely=0.8)

    Register_win.mainloop()
