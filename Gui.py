#-------------------------------------------------------------------------------
# Name:        GUI-main.py
#
# Author:      MS Productions
#
# Created:     09 04 2023
# Copyright:   (c)MS Productions
#
# Lead Dev : Meit Sant
#-------------------------------------------------------------------------------

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import tkinter.messagebox as mb
import tkinter.scrolledtext as st
from threading import Thread
import ED,os,sys,time,sqlite3,Account_login_GUI,random
from PIL import ImageTk, Image

Account_login_GUI.Login_UI()
try: UName,AccType = Account_login_GUI.UName,Account_login_GUI.AccType
except: sys.exit()

#UName,AccType = 'Meit','Admin'  # Set the username and account type (Temp)
global mode

# Connect to the database
connector = sqlite3.connect('Image_database.db')
cursor = connector.cursor()
connector.execute("CREATE TABLE IF NOT EXISTS img_database (Img_ID INTEGER AUTO_INCREMENT PRIMARY KEY NOT NULL, ImageNAME TEXT, DATA LONGTEXT, UserName VARCHAR(10))")   # Create a table if it doesn't already exist
connector.commit()

def Choose_File():
    global filename
    while True:
        # Open a file dialog to choose a file
        filename = askopenfilename()
        if filename == '': return
        elif 'png' not in filename and 'jpg' not in filename:
            # Shows an error if the file type is not supported
            mb.showerror("ERROR","The file type is invalid. Only jpg and PNG images are supported")
        else: break
    log_widget.delete(1.0,END)
    log_widget.insert(tk.INSERT,f"{ED.Give_time_and_date()} >> File chosen - '{filename}'")

def Display_records():
    # Clear the treeview
    tree.delete(*tree.get_children())
    # Select all records from the database
    curr = connector.execute('SELECT * FROM img_database;')
    data = curr.fetchall()
    i = 0
    for records in data:
        if AccType != 'Admin' and records[3] != UName: continue
        i+=1
        if AccType == 'Admin':
            # Insert the records into the treeview
            tree.insert('', END, values=(i,records[1],records[3]))
        else: tree.insert('', END, values=(i,records[1]))
    del i,data

def Download_record():
    # Shows an error if no item is selected
    if not tree.selection(): mb.showerror('ERROR', 'Please select an item from the database')
    else:
        #Thread(target=lambda : mb.showinfo('Info','The image will be downloaded after decode is performed.')).start()
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
            ED.Decode_data(Img_name,Data[0][0])
            mb.showinfo('Info', 'Image saved successfully')
        except:
            # Shows an error if decoding fails
            mb.showerror('ERROR', 'Error occured while decoding image. Please try again.')

def Delete_Data():
    if not tree.selection():
        # Shows an error if no item is selected
        mb.showerror('ERROR!', 'Please select an item from the database')
    else:
        if mb.askokcancel('Destructive Action - Delete Data','Do you really want to do this ?\nThe Data will be deleted permanently') == True:   # Confirm with the user before deleting data
            current_item = tree.focus()
            values = tree.item(current_item)
            selection = values["values"]
            num = selection[0]

            # Delete the selected record from the database
            connector.execute('DELETE FROM img_database WHERE Img_ID=%d' % selection[0])
            connector.commit()

            cursor.execute("select * from Img_database")
            # Fetches All data
            results = cursor.fetchall()

            # Gets the total Number of rows
            total_num = len(results)
            print(total_num)
            mb.showinfo('Info', 'The Specified data has succesfully been deleted.')
            Display_records()
        else:
            pass

def Clear_all():
    # Confirm with the user before clearing all data
    if mb.askokcancel('Destructive Action - Clear All','Do you really want to do this ?\nThe Data will be deleted permanently') == True:
        # Delete all records from the database
        connector.execute('DELETE FROM img_database;')
        connector.commit()
        mb.showinfo('Info', 'All the data has been erased.')
        Display_records()
    else:
        pass

def Upload_gui_load():
    Insight_text = """
    The program will automatically encode the image chosen with a special encoding
    algorithem. With which all your images will be secure.
    """
    Label(Idea_panel, text=Insight_text, font=("Bahnschrift Light",12),fg="white",bg=Main_window_colour).place(relx=0.015, rely=0.2,relwidth=1)
    Label(Idea_panel, text="Insight", font=("Bahnschrift Bold",14),fg="white",bg=Main_window_colour).place(relx=0.04, y=0.13)

    Frame(Main_win,background=Main_window_colour).place(relx=0.23,rely=0.34,relheight=1,relwidth=1)
    global Output_box,log_widget,Log_text

    Output_box = Frame(Main_win,background="#7476A7")
    Output_box.place(relx=0.3, rely=0.57, relheight=0.35, relwidth=0.5)

    log_widget = st.ScrolledText(Output_box,font=Font,background="black",fg="White")
    log_widget.place(relx=0, rely=0.2, relheight=0.8, relwidth=1.04)

    try:
        log_widget.insert(tk.INSERT,Log_text)
        del Log_text
    except:pass

    Label(Output_box,text= 'Console Output',font=Font,background="#7476A7").place(relx=0,rely=0)

    Button(Main_win, text='Choose Image', font=Font,fg="white",bg=Main_window_colour,command = Choose_File).place(relx=0.3, rely=0.41,relheight = 0.08,relwidth=0.4)
    Button(Main_win, text='Encode!',font=Font,fg="white",bg=Main_window_colour,command = lambda : Thread(target=Enc_cmd).start()).place(relx=0.8, rely=0.41,relheight = 0.08,relwidth=0.15)

def Enc_cmd():
    log_widget.delete(2.0,END)
    if not 'filename' in globals():
        mb.showerror("ERROR","You have not yet entered the file path.")                     # Shows an error if no file has been chosen
        return None
    dte = ED.Give_time_and_date()
    Tmp_str ="\n"+dte+" >> Loading image..."
    log_widget.insert(tk.INSERT,Tmp_str)

    try:
        ED.Loading_image(filename)                                                          # Load the chosen image

        dte = ED.Give_time_and_date()
        Tmp_str ="\n"+dte+" >> Encoding image..."
        log_widget.insert(tk.INSERT,Tmp_str)
        try:
            tme,Img_name,Img_data = ED.Encode_img()                                         # Encode the image

            dte = ED.Give_time_and_date()
            Tmp_str ="\n"+dte+" >> Image Encoded"
            log_widget.insert(tk.INSERT,Tmp_str)

            dte = ED.Give_time_and_date()
            Extra_ = " >>"+tme
            Tmp_str ="\n"+dte+Extra_
            log_widget.insert(tk.INSERT,Tmp_str)

            dte = ED.Give_time_and_date()
            Tmp_str ="\n"+dte+" >> Saving data to database..."
            log_widget.insert(tk.INSERT,Tmp_str)

            try:
                connector = sqlite3.connect('Image_database.db')
                cursor = connector.cursor()
                cursor.execute("select * from Img_database")
                results = cursor.fetchall()

                if len(results) == 0: ID = 1
                else: ID = results[len(results)-1][0]+1
                connector.execute('INSERT INTO Img_database (Img_ID, ImageNAME, DATA, UserName) VALUES (?,?,?,?)', (ID,Img_name,Img_data,UName))
                connector.commit()

                dte = ED.Give_time_and_date()
                Tmp_str ="\n"+dte+" >> Saved successfully"
                log_widget.insert(tk.INSERT,Tmp_str)
            except:
                dte = ED.Give_time_and_date()
                Tmp_str ="\n"+dte+" >> [ERROR] Save Failed"
                log_widget.insert(tk.INSERT,Tmp_str)                                        # Shows an error if saving fails
        except:
            dte = ED.Give_time_and_date()
            Tmp_str ="\n"+dte+" >> [ERROR] Encoding failed"
            log_widget.insert(tk.INSERT,Tmp_str)                                            # Shows an error if encoding fails
    except:
        dte = ED.Give_time_and_date()
        Tmp_str ="\n"+dte+" >> [ERROR] The path of the image is invalid."
        log_widget.insert(tk.INSERT,Tmp_str)                                                # Shows an error if the image path is invalid


    del Tmp_str,dte
    return

def Download_gui_load():

    Insight_text = """
    Please select the name of your desired image. Upon selecting your
    image, it will decode your image and save it in your local downloads folder.
    """
    Label(Idea_panel, text=Insight_text, font=("Bahnschrift Light",12),fg="white",bg=Main_window_colour).place(relx=0.015, rely=0.2,relwidth=1 )
    Label(Idea_panel, text="Insight", font=("Bahnschrift Bold",14),fg="white",bg=Main_window_colour).place(relx=0.04, y=0.13)

    Frame(Main_win,background=Main_window_colour).place(relx=0.23,rely=0.34,relheight=1,relwidth=1)

    ''' Search Function (Incomplete)
    Button(Main_win, text='Search', font=Font,fg="white",bg=Main_window_colour,command = Display_records).place(relx=0.8,y=230,relheight=0.06,relwidth=0.1)

    Key_word = ""
    Entry(Main_win, textvariable=Key_word, font=("Bahnschrift Light",18)).place(relx=0.26,y=230,relheight=0.06,relwidth=0.4)
    '''

    Button(Main_win, text='Download Image', font=Font,fg="white",bg=Main_window_colour,command= Thread(target=Download_record).start).place(relx=0.8,rely = 0.89,relheight=0.1,relwidth=0.18)


    if AccType == 'Admin':Button(Main_win, text='Delete Record', font=Font,fg="white",bg=Main_window_colour,command= Delete_Data).place(relx=0.6,rely = 0.89,relheight=0.1,relwidth=0.18)
    if AccType == 'Admin':Button(Main_win, text='Clear All', font=Font,fg="white",bg=Main_window_colour,command= Clear_all).place(relx=0.4,rely = 0.89,relheight=0.1,relwidth=0.18)

    global tree,Log_text

    if AccType == 'Admin':
        tree = ttk.Treeview(Main_win,height = 100,selectmode=BROWSE,columns=('Sr_No','Name','UserName'))
        tree.heading('UserName', text='UserName',anchor=W)
        tree.column('#2', width = 40,stretch = YES)

    else: tree = ttk.Treeview(Main_win,height = 100,selectmode=BROWSE,columns=('Sr_No','Name'))

    tree.heading('Sr_No', text='Sr_No', anchor=W)
    tree.heading('Name', text='Name', anchor=W)

    tree.column('#0', width = 0,stretch = NO)
    tree.column('#1', width = 40,stretch = YES)

    tree.place(relx = 0.26,y = 280,relheight = 0.37,relwidth = 0.6)
    Display_records()
    try:Log_text= log_widget.get("1.0",END)
    except:pass

Insight_text = """
Secure Imaging database is a project inspired by Google Photos.
It uses a custom encoding and decoding algorithem to secure your image files.
"""

Main_win = Tk()

Main_window_colour = '#28293F'
Side_panel_colour ='#1C2028'
Font = ("Bahnschrift Bold",12)

Main_win.title("Secure Imaging Database")
Main_win.geometry('1020x600+350+200')
Main_win.configure(bg = Main_window_colour)

Side_panel = Frame(Main_win,background = Side_panel_colour)
Side_panel.place(x = 0,
                 y = 0,
                 relheight = 1,
                 relwidth = 0.23)

Shadow = Frame(Main_win,background=Side_panel_colour)
Shadow.place(relx = 0.257,
             rely = 0.117,
             relheight = 0.21,
             relwidth = 0.675)

X_disp = 840-(len(UName)*10)

Label(Main_win,text='Welcome {0}'.format(UName),font=("Bahnschrift Bold",16),fg="white",bg = Main_window_colour).place(x = X_disp,rely = 0.04)

if AccType == 'Admin':
    image = Image.open(r"./Assets/Admin_acc.png")                                           # Sets user img as Admin user
else:
    image = Image.open(r"./Assets/Acc_img.png")                                             # Sets user img as Regular user

image=image.resize((50 ,50),Image.LANCZOS)
Acc_photo = ImageTk.PhotoImage(image)
image_label = Label(Main_win,image = Acc_photo,borderwidth = 0,highlightthickness = 0)
image_label.place(relx = 0.93,rely = 0.02)                                                  # Places user img on the top right hand corner

dir_list = os.listdir(r"./Assets/HomeScr_photos")
image1 = Image.open(f"./Assets/HomeScr_photos/{random.choice(dir_list)}")                   # Randomizes the Home Screen image

image1=image1.resize((600 ,350),Image.LANCZOS)                                            # Displays the Home screen image
photo1 = ImageTk.PhotoImage(image1)
image_label1 = Label(Main_win,image = photo1,borderwidth = 0,highlightthickness = 0)
image_label1.place(relx = 0.3,rely = 0.35)

Idea_panel = Frame(Main_win,background=Main_window_colour)
Idea_panel.place(relx = 0.264,rely = 0.125,relheight = 0.19,relwidth = 0.66)

Label(Idea_panel,text=Insight_text,font=("Bahnschrift Light",12),fg="white",bg=Main_window_colour).place(relx=0.02,rely=0.2)

Label(Idea_panel,text="Insight",font=("Bahnschrift Bold",14),fg="white",bg=Main_window_colour).place(relx=0.04,y=0.13)

Label(Side_panel,text="Secure Imaging Database",font=("Bahnschrift Light",12),fg="white",bg=Side_panel_colour).place(relx=0.04,rely=0.02)

Button(Side_panel,text='Upload Image',font=Font,fg="white",bg=Side_panel_colour,command = Upload_gui_load).place(relx=0.15,rely=0.3,relheight=0.1,relwidth=0.7)

Button(Side_panel,text='Download Image',font=Font,fg="white",bg=Side_panel_colour,command = Download_gui_load).place(relx=0.15,rely=0.5,relheight=0.1,relwidth=0.7)

Main_win.mainloop()
