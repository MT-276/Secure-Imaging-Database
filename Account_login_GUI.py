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
import os, sys, time, sqlite3
from ED import Encrypt_Pwd
global Username, Password,UName,Pwd,AccType

Allow_Bypass = False

connector = sqlite3.connect('Image_database.db')
connector.execute("""
CREATE TABLE IF NOT EXISTS Acc_database (
Acc_ID INTEGER PRIMARY KEY AUTOINCREMENT,
AccNAME VARCHAR(10) UNIQUE,
Pwd VARCHAR(100),
AccType Varchar(5) )
""")

def Login():
    global Username, Password,UName,Pwd,AccType,Allow_Bypass
    if Allow_Bypass == True:
        UName ='Meit'
        AccType ='Admin'
        Login_win.destroy()
        return
    UName = Username.get()
    Pwd = Password.get()

    result = connector.execute("SELECT * FROM Acc_database WHERE AccNAME = ?;",(UName,)).fetchone()
    if result:
        if result[2] != Encrypt_Pwd(Pwd):
            mb.showerror("Error", "Invalid Password")
            return
        else:
            AccType = result[3]
            Login_win.destroy()
    else:
        mb.showerror("Error", "Invalid Username")

def Back_To_Login():
    Register_win.destroy()
    Login_UI()
def Register():

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
                connector.execute("INSERT INTO Acc_database (AccNAME, Pwd, AccType) VALUES (?,?,'Admin')",(UName,Encrypt_Pwd(Pwd)))
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
            connector.execute("INSERT INTO Acc_database (AccNAME, Pwd) VALUES (?,?)",(UName,Encrypt_Pwd(Pwd)))
            connector.commit()
        except:
            mb.showerror("Error", "The username already exists")
            return
        mb.showinfo("Success", "Registration successful")
        Username.delete(0, END)
        Password.delete(0, END)

    Back_To_Login()

def Login_UI():
    global Login_win, Username, Password, admin_var,Allow_Bypass

    Login_win = Tk()

    Login_window_colour = '#28293F'
    Frame_colour = '#1C2028'
    Font = ("Bahnschrift Bold", 12)

    Login_win.title("Secure Imaging Database - LOGIN")
    Login_win.geometry('400x500+700+300')
    Login_win.configure(bg=Login_window_colour)

    Frame_ = Frame(Login_win, background=Frame_colour)
    Frame_.place(x=30, y=25, relheight=0.9, relwidth=0.85)

    # Load the image
    image_path = "./Assets/Acc_img_Login.png"
    image = Image.open(image_path)
    new_size = (100, 100)
    image = image.resize(new_size, Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)

    # Create a label to display the image
    image_label = Label(Frame_, image=photo, borderwidth=0, highlightthickness=0)

    image_label.image = photo
    image_label.place(relx=0.35, rely=0.08)

    Label(Frame_, text="Username :", font=("Bahnschrift Light", 12), fg="white", bg=Frame_colour).place(relx=0.05, rely=0.39)
    Username = Entry(Frame_, bg=Frame_colour, fg='white', font=("Bahnschrift", 15))
    Username.place(relx=0.4, rely=0.38, relheight=0.07, relwidth=0.5)

    Label(Frame_, text="Password :", font=("Bahnschrift Light", 12), fg="white", bg=Frame_colour).place(relx=0.06, rely=0.49)
    Password = Entry(Frame_, bg=Frame_colour, fg='white', font=("Bahnschrift", 15), show="*")
    Password.place(relx=0.4, rely=0.48, relheight=0.07, relwidth=0.5)

    Button(Frame_, text='LOGIN', bg=Frame_colour, fg='white', font=("Arial bold", 20), command=Login).place(relx=0.32, rely=0.65)

    Label(Frame_, text="Don't have an account ?",font=("Bahnschrift Light", 10),fg="white", bg=Frame_colour).place(relx=0.1, rely=0.8)
    Button(Frame_, text='REGISTER', bg=Frame_colour, fg='white', font=("Bahnschrift Light", 10), command=Register_UI).place(relx=0.55, rely=0.8)

    Login_win.mainloop()

def Register_UI():
    try:
        Login_win.destroy()
    except:pass

    global Register_win, Username, Password, admin_var

    Register_win = Tk()

    Register_window_colour = '#28293F'
    Frame_colour = '#1C2028'
    Font = ("Bahnschrift Bold", 12)

    Register_win.title("Secure Imaging Database - REGISTER")
    Register_win.geometry('400x500+700+300')
    Register_win.configure(bg=Register_window_colour)

    Frame_ = Frame(Register_win, background=Frame_colour)
    Frame_.place(x=30, y=25, relheight=0.9, relwidth=0.85)

    # Load the image
    image_path = "./Assets/Acc_img_Register.png"
    image = Image.open(image_path)
    new_size = (100, 100)
    image = image.resize(new_size, Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)

    # Create a label to display the image
    image_label = Label(Frame_, image=photo, borderwidth=0, highlightthickness=0)

    image_label.image = photo
    image_label.place(relx=0.35, rely=0.08)

    Label(Frame_, text="Username :", font=("Bahnschrift Light", 12), fg="white", bg=Frame_colour).place(relx=0.05, rely=0.39)
    Username = Entry(Frame_, bg=Frame_colour, fg='white', font=("Bahnschrift", 15))
    Username.place(relx=0.4, rely=0.38, relheight=0.07, relwidth=0.5)

    Label(Frame_, text="Password :", font=("Bahnschrift Light", 12), fg="white", bg=Frame_colour).place(relx=0.06, rely=0.49)
    Password = Entry(Frame_, bg=Frame_colour, fg='white', font=("Bahnschrift", 15), show="*")
    Password.place(relx=0.4, rely=0.48, relheight=0.07, relwidth=0.5)

    Button(Frame_, text='Register', bg=Frame_colour, fg='white', font=("Arial bold", 20), command=Register).place(relx=0.32, rely=0.65)
    admin_var = IntVar()

    Label(Frame_, text="Already have an account ?",font=("Bahnschrift Light", 10),fg="white", bg=Frame_colour).place(relx=0.2, rely=0.91)
    Button(Frame_, text='LOGIN', bg=Frame_colour, fg='white', font=("Bahnschrift Light", 10), command=Back_To_Login).place(relx=0.66, rely=0.9)


    Checkbutton(Frame_, text="Register as Admin", variable=admin_var, bg=Frame_colour, fg='grey',onvalue = 1, offvalue = 0,
                font=("Bahnschrift Light", 10)).place(relx=0.3, rely=0.8)

    Register_win.mainloop()
