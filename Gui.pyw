#-------------------------------------------------------------------------------
# Name:        Gui.py
# Purpose:     Main graphical user interface for SID
#
# Author:      MS Productions
#
# Created:     23 04 2023
# Copyright:   (c)MS Productions
#
# Lead Dev : Meit Sant
#-------------------------------------------------------------------------------
'''
These imports are highly specific. No wildcard imports were made except an exception of sqlite3.
(Wildcard imports are those which import everything into the script.
Eg: 'from pandas import *' or just 'import pandas')
'''

from os import listdir
from sys import exit
from tkinter import Tk,ttk,Frame,Button,Label,END,BROWSE,W,YES,NO,INSERT,simpledialog
from tkinter.filedialog import askopenfilename
import tkinter.messagebox as mb
import tkinter.scrolledtext as st
from threading import Thread,enumerate
from random import choice
from PIL import ImageTk, Image
from Account_login_GUI import Login_UI
import sqlite3,ED

# This will open the Login UI where the user must either register a new account or login with an existing account.
Login_UI()
try:
    # Trying to fetch Username and Account type if successfully logged in.
    from Account_login_GUI import UName,AccType
    UName,AccType = UName,AccType
except:
    # Will exit if login window closed or couldn't fetch Username and Account type.
    exit()

db_path = 'Image_database.db'

# Connect to the database
connector = sqlite3.connect(db_path)
cursor = connector.cursor()

# Creates a table if it doesn't already exist
connector.execute("""
CREATE TABLE IF NOT EXISTS img_database
(Img_ID INTEGER PRIMARY KEY,
ImageNAME TEXT,
DATA LONGTEXT,
UserName VARCHAR(10),
Status VARCHAR(10)
);
""")
connector.commit()

'''
FUNCTIONS :
'''

def Choose_File():
    '''
    Get the file path from user by opening an Explorer window
    '''

    # This gets the names of the threads currently running. If there is an ongoing encode, this will prevent another from starting.
    for thread in enumerate():
        if "Enc_cmd" in str(thread.name):
            log_widget.insert(INSERT,f"\n{ED.Give_time_and_date()} >> An encode is ongoing please wait.")
            return
    global filename
    while True:
        # Open a Explorer window to choose a file
        filename = askopenfilename()
        if filename == '': return # If the user closes the window without choosing a file, then do nothing.
        elif 'png' not in filename.lower() and 'jpg' not in filename.lower():
            # Shows an error if the file type is not supported
            mb.showerror("ERROR","The file type is invalid. Only JPG and PNG images are supported")
        else: break
    log_widget.delete(1.0,END)
    log_widget.insert(INSERT,f"{ED.Give_time_and_date()} >> File chosen - '{filename}'")

def Display_records(view):
    '''
    Shows the records in the database in a tabular form.
    view :  1. Download
            2. Accounts
    '''
    # Clear the table
    tree.delete(*tree.get_children())

    # Fetch data from database according to view.
    if view == 'Download':
        # Fetching data from the db
        curr = connector.execute('SELECT * FROM img_database;')
        data = curr.fetchall()
        i = 0
        for records in data:
            # Skips entry of images not uploaded by the logged on user. [UNLESS ADMIN]
            if AccType != 'Admin' and records[3] != UName: continue
            # Skips deleted entries [UNLESS ADMIN]
            if AccType != 'Admin' and records[4] == 'Deleted': continue
            i+=1
            if AccType == 'Admin':
                # Insert the records into the table with user's name [UNLESS ADMIN]
                if records[4] == None:
                    Status = '-'
                else:
                    Status = 'Image Deleted by User'
                tree.insert('', END, values=(i,records[1],records[3],Status))
            else:
                # Insert the records into the table
                tree.insert('', END, values=(i,records[1]))

    if view == 'Accounts':
        # Fetching data from the db
        curr = connector.execute('SELECT * From Acc_database')
        data = curr.fetchall()
        i = 0
        # Display all the records in the database along with their date of register and account type
        for records in data:
            i+=1
            if records[3] == None:
                Ac_type = ''
            else:
                Ac_type = 'Admin'
            # Insert the records into the table
            tree.insert('', END, values=(i,records[1],Ac_type,records[4]))
        del i,data

def Download_record(Upscale=None):
    '''
    Initiates Decode and save of the image selected.
    Upscale (optional) :
        1. True
        2. None
    When Upscale is True, the image will be decoded along with
    upscaling before saving to the downloads folder
    '''
    # Shows an error if no item is selected
    if not tree.selection():
        mb.showerror('ERROR', 'Please select an item from the database')
        return
    else:
        if Upscale == True: # If user wantes to upscale, then ask the upscale factor.
            newWin = Tk()
            newWin.withdraw()
            scale_factor = simpledialog.askinteger("Upscale Factor", "Enter Upscale factor:\n(Note: Higher values may take more CPU resources to compute)",parent=newWin)
            newWin.destroy()
        else:
            scale_factor = None
        mb.showinfo('Info','The image will be downloaded after decode is performed.')

        # Get the name of the image from the table selection
        current_item = tree.focus()
        values = tree.item(current_item)
        selection = values["values"]
        Img_name = selection[1]

        # Connect to the database
        connector = sqlite3.connect('Image_database.db')
        cursor = connector.cursor()
        curr1 = connector.execute('SELECT DATA FROM img_database WHERE ImageNAME = ?;', (Img_name,))
        Data = curr1.fetchall()
        del selection,connector,cursor,curr1,values,current_item
        try:
            # Decode the data and save the image
            ED.Decode_data(Img_name,Data[0][0],Upscale,scale_factor)
            mb.showinfo('Info', 'Image saved successfully')
            return
        except Exception as e:
            print(f'\n[ERROR] {e}')
            # Shows an error if decoding fails
            mb.showerror('ERROR', 'Error occured while decoding image. Please try again.')
            return

def Delete_Data(UI_Type):
    '''
    Deletes the data selected by the user.
    UI_Type :   1. Dwnld
                2. None
    The UI type corresponds to which data is to be parsed and deleted from the database.
    If None, then Accounts UI will be taken.
    '''
    if not tree.selection():
        # Shows an error if no item is selected
        mb.showerror('ERROR!', 'Please select an item from the database')
        return
    if UI_Type == 'Dwnld':
        if mb.askokcancel('Destructive Action - Delete Data',
            'Do you really want to do this ?\nThe Data will be deleted permanently') is True:   # Confirm with the user before deleting data
            current_item = tree.focus()
            values = tree.item(current_item)
            selection = values["values"]

            # If user is not an admin, the record will not be deleted from the database.
            # To truly delete a record, the user must be an admin.
            if AccType != "Admin":
                connector.execute("""
UPDATE img_database
SET status = 'Deleted'
WHERE ImageName = ? AND UserName = ? """, (selection[1],UName))
                connector.commit()
                Display_records('Download')
                return

            # Delete the selected record from the database
            connector.execute('DELETE FROM img_database WHERE ImageName = ?', (selection[1],))
            connector.commit()

            mb.showinfo('Info', 'The Specified data has succesfully been deleted.')
            Display_records('Download')
        else:
            return
    else:
        if mb.askokcancel('Destructive Action - Delete Account',
            'Do you really want to do this ?\nThe Account will be deleted permanently') is True:   # Confirm with the user before deleting data

            # Get the data from the table
            current_item = tree.focus()
            values = tree.item(current_item)
            selection = values["values"]

            # Execute SQL to delete account from db
            connector.execute('DELETE FROM Acc_database WHERE AccNAME = ?', (selection[1],))
            connector.commit()

            # Refresh the Accounts UI table
            Display_records('Accounts')
            return
        else: # If user selects "no" for confirmation, then do nothing.
            return

def Clear_all():
    '''
    Clears all the images in the database. (ONLY FOR ADMINS)
    '''
    # Confirm with the user before clearing all data
    if mb.askokcancel('Destructive Action - Clear All',
        'Do you really want to do this ?\nThe Data will be deleted permanently') is True:

        # Delete all records from the database
        connector.execute('DELETE FROM img_database;')
        connector.commit()
        mb.showinfo('Info', 'All the data has been erased.')

        # Refresh the Download UI table
        Display_records('Download')
    else: return #  # If user selects "no" for confirmation, then do nothing.

def Enc_cmd():
    '''
    Function for execution of Encode of the image file chosen.
    '''
    log_widget.delete(2.0,END)
    if not 'filename' in globals():
        # Shows an error if no file has been chosen
        mb.showerror("ERROR","You have not yet entered the file path.")
        return # Do nothing.
    log_widget.insert(INSERT,f"\n{ED.Give_time_and_date()} >> Loading image...")

    try:
        # Load the chosen image
        ED.Loading_image(filename)
        log_widget.insert(INSERT,f"\n{ED.Give_time_and_date()} >> Encoding image...")

        try:
            # Encode the image
            tme,Img_name,Img_data = ED.Encode_img()

            log_widget.insert(INSERT,f"\n{ED.Give_time_and_date()} >> Image Encoded")
            log_widget.insert(INSERT,f"\n{ED.Give_time_and_date()} >>{tme}") # Time utilised by CPU to encode the image (Time of Execution)
            log_widget.insert(INSERT,f"\n{ED.Give_time_and_date()} >> Saving data to database...")

            try:
                # Connect to the database
                connector = sqlite3.connect(db_path)
                cursor = connector.cursor()
                cursor.execute("select * from Img_database")
                results = cursor.fetchall()

                # Setting the ID of the image.
                if len(results) == 0:
                    ID = 1
                else:
                    ID = results[len(results)-1][0]+1 # Adds 1 to whatever the last ID is of the record.
                connector.execute(f"INSERT INTO Img_database (Img_ID, ImageNAME, DATA, UserName) VALUES ({ID},'{Img_name}','{Img_data}','{UName}')")
                connector.commit()

                log_widget.insert(INSERT,f"\n{ED.Give_time_and_date()} >> Saved successfully.")
            except Exception as e:
                print(f"[ERROR] {e}")
                # Shows an error if saving fails
                log_widget.insert(INSERT,f"\n{ED.Give_time_and_date()} >> [ERROR] Save Failed.")

        except Exception as e:
            print(f"[ERROR] {e}")
            # Shows an error if encoding fails
            log_widget.insert(INSERT,f"\n{ED.Give_time_and_date()} >> [ERROR] Encoding failed.")
    except Exception as e:
        print(f"[ERROR] {e}")
        # Shows an error if the image path is invalid
        log_widget.insert(INSERT,f"\n{ED.Give_time_and_date()} >> [ERROR] Image was not found.")

    return

def Upload_gui_load():
    global mode
    # Check if the current mode is already set to 'Upload'. If yes, return and do nothing.
    if mode == 'Upload': return

    # Set the mode to 'Upload' to indicate that the user is in the upload section.
    mode = "Upload"

    # Define the insight text that provides an explanation of this section.
    Insight_text = """
    The program will automatically encode the image chosen with a special encoding
    algorithem. With which all your images will be secure.
    """

    # Hider frame for Insight text
    Frame(Idea_panel,
            bg=Main_window_colour).place(relx=0,
                                        rely=0.45,
                                        relheight=1,
                                        relwidth=1)

    # Places Insight text
    Label(Idea_panel,
        text=Insight_text,
        font=("Bahnschrift Light",12),
        fg="white",bg=Main_window_colour).place(relx=0.05,rely=0.3)

    # Places text 'Insight'
    Label(Idea_panel,
        text="Insight",
        font=("Bahnschrift Bold",20),
        fg="white",
        bg=Main_window_colour).place(relx=0.05,rely=0.1)

    # Hides previous UI
    Frame(Main_win,
        background=Main_window_colour).place(relx=0.23,rely=0.34,relheight=1,relwidth=1)
    global Output_box,log_widget,Log_text

    Output_box = Frame(Main_win,background="#7476A7")
    Output_box.place(relx=0.3, rely=0.57, relheight=0.35, relwidth=0.5)

    log_widget = st.ScrolledText(Output_box,font=Font,background="black",fg="White")
    log_widget.place(relx=0, rely=0.2, relheight=0.8, relwidth=1.04)

    # If there is some log text of the previous log widget, then insert into the new one for a fluid transition.
    try:
        log_widget.insert(INSERT,Log_text)
        del Log_text
    except: pass

    # Places text "Console Ouput"
    Label(Output_box,text= 'Console Output',font=Font,background="#7476A7").place(relx=0,rely=0)

    # Choose Image Button
    Button(Main_win, text='Choose Image',
                font=Font,fg="white",
                bg=Main_window_colour,
                command = Choose_File).place(relx=0.3, rely=0.41,relheight = 0.08,relwidth=0.4)

    # Upload Button
    Button(Main_win, text='Upload',
                font=Font,fg="white",
                bg=Main_window_colour,
                command = lambda : Thread(target=Enc_cmd).start()).place(relx=0.8, rely=0.41,relheight = 0.08,relwidth=0.15)

def Download_gui_load():
    global mode
    # Check if the current mode is already set to 'Download'. If yes, return and do nothing.
    if mode == 'Download': return

    # Set the mode to 'Download' to indicate that the user is in the download section.
    mode = "Download"

    # Define the insight text that provides an explanation of this section.
    Insight_text = """
    Please select the name of your desired image. Upon selecting your
    image, it will decode your image and save it in your local downloads folder
    """
    # Hider frame for Insight text
    Frame(Idea_panel,
            bg=Main_window_colour).place(relx=0,
                                        rely=0.45,
                                        relheight=1,
                                        relwidth=1)

    # Places Insight text
    Label(Idea_panel,text=Insight_text,font=("Bahnschrift Light",12),fg="white",bg=Main_window_colour).place(relx=0.1,rely=0.3)

    # Places text 'Insight'
    Label(Idea_panel,
        text="Insight",
        font=("Bahnschrift Bold",20),
        fg="white",
        bg=Main_window_colour).place(relx=0.05,rely=0.1)

    # Hides previous UI
    Frame(Main_win,background=Main_window_colour).place(relx=0.23,rely=0.34,relheight=1,relwidth=1)

    # Download Image Button
    Button(Main_win,
            text='Download Image',
            font= Font,fg="white",
            bg= Main_window_colour,
            command= lambda : Thread(target=Download_record).start()).place(relx=0.62,rely = 0.89,relheight=0.1,relwidth=0.15)

    # Download + Upscale Image Button
    Button(Main_win,
            text='Download + Upscale Image',
            font= Font,fg="white",
            bg= Main_window_colour,
            command= lambda : Thread(target= lambda:Download_record(True)).start()).place(relx=0.78,rely = 0.89,relheight=0.1,relwidth=0.21)

    Label(Main_win, text="-NEW-", font=("Gotham", 12), fg="white", bg=Main_window_colour).place(relx=0.93, rely=0.866)

    # Delete Record Button
    Button(Main_win,
            text='Delete Record',
            font=Font,fg="white",
            bg=Main_window_colour,
            command= lambda : Delete_Data('Dwnld')).place(relx=0.46,rely = 0.89,relheight=0.1,relwidth=0.15)

    # Clear All Button [ADMIN ONLY]
    if AccType == 'Admin':
        Button(Main_win,
                text='Clear All',
                font=Font,fg="white",
                bg=Main_window_colour,
                command= Clear_all).place(relx=0.3,rely = 0.89,relheight=0.1,relwidth=0.15)

    global tree,Log_text

    # If user is Admin, then also show status and the username of the record saved by.
    if AccType == 'Admin':
        tree = ttk.Treeview(Main_win,height = 100,selectmode=BROWSE,columns=('Sr_No','Name','UserName','Status'))
        tree.heading('UserName', text='UserName',anchor=W)
        tree.column('#2', width = 40,stretch = YES)

        tree.heading('Status', text='Status',anchor=W)
        tree.column('#3', width = 40,stretch = YES)


    else: tree = ttk.Treeview(Main_win,height = 100,selectmode=BROWSE,columns=('Sr_No','Name'))

    tree.heading('Sr_No', text='Sr_No', anchor=W)
    tree.heading('Name', text='Name', anchor=W)

    tree.column('#0', width = 0,stretch = NO)
    tree.column('#1', width = 40,stretch = YES)

    # Place the Treeview widget on the main window
    tree.place(relx = 0.26,y = 280,relheight = 0.37,relwidth = 0.6)

    Display_records('Download')

    # Gets the log text of the Upload UI so that later it can be inserted back for a fluid transition.
    try:Log_text= log_widget.get("1.0",END)
    except: pass

def Accounts_UI():
    '''
    Separate UI to show accounts. [ONLY ADMINS]
    '''
    global mode

    # Check if the current mode is already set to 'Accounts'. If yes, return and do nothing.
    if mode == 'Accounts':
        return

    # Set the mode to 'Accounts' to indicate that the user is in the accounts management section.
    mode = "Accounts"

    # Define the insight text that provides an explanation of this section.
    Insight_text = """
    From here, the admin can view or delete the accounts present in
    the database.
    """

    # Hider frame for Insight text
    Frame(Idea_panel,
          bg=Main_window_colour).place(relx=0, rely=0.45, relheight=1, relwidth=1)

    # Places Insight text on the Idea_panel
    Label(Idea_panel,
          text=Insight_text,
          font=("Bahnschrift Light", 12),
          fg="white",
          bg=Main_window_colour).place(relx=0.1, rely=0.3)

    # Places the text 'Insight'
    Label(Idea_panel,
          text="Insight",
          font=("Bahnschrift Bold", 20),
          fg="white",
          bg=Main_window_colour).place(relx=0.05, rely=0.1)

    # Hides previous UI
    Frame(Main_win, background=Main_window_colour).place(relx=0.23, rely=0.34, relheight=1, relwidth=1)

    global tree
    # Create a Treeview widget for displaying data with specified columns
    tree = ttk.Treeview(Main_win, height=100, selectmode=BROWSE, columns=('Sr_No', 'Name', 'Acc type', 'Date created'))

    # Set column headings and their alignment
    tree.heading('Sr_No', text='Sr_No', anchor=W)
    tree.column('#0', width=0, stretch=NO)

    tree.heading('Name', text='Name', anchor=W)
    tree.column('#1', width=40, stretch=YES)

    tree.heading('Acc type', text='Acc type', anchor=W)
    tree.column('#2', width=40, stretch=YES)

    tree.heading('Date created', text='Date created', anchor=W)
    tree.column('#3', width=40, stretch=YES)

    # Place the Treeview widget on the main window
    tree.place(relx=0.26, y=280, relheight=0.37, relwidth=0.6)

    # Display records of 'Accounts' in the Treeview
    Display_records('Accounts')

    # Delete Account Button
    Button(Main_win,
           text='Delete Account',
           font=Font,
           fg="white",
           bg=Main_window_colour,
           command=lambda: Delete_Data(None)).place(relx=0.8, rely=0.89, relheight=0.1, relwidth=0.18)


Main_win = Tk()

Main_window_colour = '#28293F'
Side_panel_colour ='#1C2028'
Font = ("Bahnschrift Bold",12)

Main_win.title("Secure Imaging Database")
Main_win.geometry('1020x600+350+200')
Main_win.configure(bg = Main_window_colour)

# Side Panel
Side_panel = Frame(Main_win,background = Side_panel_colour)
Side_panel.place(x = 0,
                 y = 0,
                 relheight = 1,
                 relwidth = 0.23)

# Shadow of Idea Panel
Shadow = Frame(Main_win,background=Side_panel_colour)
Shadow.place(relx = 0.257,
             rely = 0.117,
             relheight = 0.21,
             relwidth = 0.675)

# Position of the GUI based on screen resolution
X_disp = 840-(len(UName)*10)

# Welcome text for the user
Label(Main_win,
            text='Welcome {0}'.format(UName),
            font=("Bahnschrift Bold",16),
            fg="white",
            bg = Main_window_colour).place(x = X_disp,rely = 0.04)

if AccType == 'Admin':
    # Sets user img as Admin user
    Acc_image = Image.open(r"./Assets/Admin_acc.png")
else:
    # Sets user img as Regular user
    Acc_image = Image.open(r"./Assets/Acc_img.png")

Acc_image1  = Acc_image.resize((50 ,50),Image.LANCZOS)
Acc_photo = ImageTk.PhotoImage(Acc_image1)
image_label = Label(Main_win,image = Acc_photo,borderwidth = 0,highlightthickness = 0)

# Places user img on the top right hand corner
image_label.place(relx = 0.93,rely = 0.02)

# Randomizes the Home Screen image
dir_list = listdir(r"./Assets/HomeScr_photos")
image1 = Image.open(f"./Assets/HomeScr_photos/{choice(dir_list)}")

# Displays the Home screen image
image1=image1.resize((600 ,350),Image.LANCZOS)
photo1 = ImageTk.PhotoImage(image1)
image_label1 = Label(Main_win,image = photo1,borderwidth = 0,highlightthickness = 0)
image_label1.place(relx = 0.3,rely = 0.35)

# Defines variable for the Idea_panel frame
Idea_panel = Frame(Main_win,background=Main_window_colour)
Idea_panel.place(relx = 0.264,rely = 0.125,relheight = 0.19,relwidth = 0.66)

# Places Insight text
Insight_text = """
Secure Imaging database is a project inspired by Google Photos.
It uses a custom encoding and decoding algorithem to secure your image files.
"""
Label(Idea_panel,text=Insight_text,font=("Bahnschrift Light",12),fg="white",bg=Main_window_colour).place(relx=0.1,rely=0.3)

# Loading Insight Image
image = Image.open(r"./Assets/Insight.png")
image=image.resize((40 ,40),Image.LANCZOS)
Insight = ImageTk.PhotoImage(image)
image_label2 = Label(Idea_panel,image = Insight,borderwidth = 0,highlightthickness = 0)

# Places Insight Image near the Insight text
image_label2.place(relx = 0,rely = 0.1)

# Places text "Insight" next to the Insight Image
Label(Idea_panel,
        text="Insight",
        font=("Bahnschrift Bold",20),
        fg="white",
        bg=Main_window_colour).place(relx=0.05,rely=0.1)

# Logo Image
image = Image.open(r"./Assets/DBImg.png")
image=image.resize((150 ,150),Image.LANCZOS)
Logo = ImageTk.PhotoImage(image)
image_label3 = Label(Side_panel,image = Logo,borderwidth = 0,highlightthickness = 0)

# Places logo on the top left hand corner
image_label3.place(relx = 0.18,rely = 0.1)

# Logo
Label(Side_panel,
        text="Secure Imaging Database",
        font=("Bahnschrift Light",12),
        fg="white",
        bg=Side_panel_colour).place(relx=0.08,rely=0.05)

# Upload Image Button
Button(Side_panel,
        text='Upload Image',
        font=Font,fg="white",
        bg=Side_panel_colour,
        command = Upload_gui_load).place(relx=0.15,
                                        rely=0.4,
                                        relheight=0.1,
                                        relwidth=0.7)

# Download Image Button
Button(Side_panel,
        text='Download Image',
        font=Font,fg="white",
        bg=Side_panel_colour,
        command = Download_gui_load).place(relx=0.15,
                                        rely=0.6,
                                        relheight=0.1,
                                        relwidth=0.7)

# Accounts table
if AccType == 'Admin':
    Button(Side_panel,
            text='Accounts',
            font=Font,fg="white",
            bg=Side_panel_colour,
            command = Accounts_UI).place(relx=0.15,
                                            rely=0.8,
                                            relheight=0.1,
                                            relwidth=0.7)

# Set the mode to 'Home' to indicate that the user is in the home section.
mode = 'Home'
Main_win.mainloop()