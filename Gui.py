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
from tkinter import ttk
from tkinter import *
from tkinter.filedialog import askopenfilename
import tkinter.messagebox as mb
import tkinter.scrolledtext as st
import ED,os,sys,time,sqlite3

global mode

connector = sqlite3.connect('Image_database.db')
cursor = connector.cursor()
connector.execute(
"CREATE TABLE IF NOT EXISTS img_database (Img_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, ImageNAME TEXT, DATA TEXT)"
)

def choose_file():
    global filename
    Loaded = False
    while Loaded != True:
        filename = askopenfilename()
        if 'png' not in filename and 'jpg' not in filename:
            mb.showerror("ERROR","The file type is invalid. Only jpg and PNG images are supported")
        else:
            Loaded = True
##    filename = r"C:/Users/meitv/OneDrive/Desktop/tmp.png"
    log_widget.delete(1.0,END)
    dte = ED.Give_time_and_date()
    Tmp_str =dte+" >> File chosen - '" + filename+"'"
    log_widget.insert(tk.INSERT,Tmp_str)

    del Tmp_str

def display_records():
   tree.delete(*tree.get_children())
   curr = connector.execute('SELECT * FROM img_database')
   data = curr.fetchall()
   for records in data:
       tree.insert('', END, values=records)

def Download_record():
   if not tree.selection():
       mb.showerror('ERROR', 'Please select an item from the database')
   else:
       current_item = tree.focus()
       values = tree.item(current_item)
       selection = values["values"]
       Data = selection[2]
       Img_name = selection[1]
       del selection
       ED.Decode_data(Img_name,Data)
       try:
        print('placeholder')
        mb.showerror('SUCCESS', 'Image saved successfully')
       except:
        mb.showerror('ERROR', 'Error occured while decoding image. Please try again')

def Delete_Record():
    #Todo Add this feature [Delete_Record]
    """
    Currently not in use
    """
    mb.showinfo("Delete Record","Feature still under development !")

def Clear_all():
    #Todo Add this feature [Clear_all]
    """
    Currently not in use
    """
    mb.showinfo("Clear all","Feature still under development !")

def Upload_gui_load():

    Insight_text = """
    The program will automatically encode the image chosen with a special encoding
    algorithem. If the database file is compromised, the image data will still be encoded,
    hence making it harder to penetrate.
    """
    #Ins_txt.destroy()
    #Ins.destroy()

    Frame(Main_win,background=Main_window_colour).place(relx=0.23,rely=0.34,relheight=1,relwidth=1)
    global Output_box,log_widget

    Output_box = Frame(Main_win,background="#7476A7")
    Output_box.place(x=300, y=375, relheight=0.308, relwidth=0.5)

    log_widget = st.ScrolledText(Output_box,height=7.5, width=56,font=Font,background="black",fg="White")
    log_widget.place(x=0,y=30)

    Label(Output_box,text= 'Console Output',font=Font,background="#7476A7").place(x=0,y=0)

    Label(Idea_panel, text=Insight_text, font=("Bahnschrift Light",12),fg="white",bg="#282A39").place(x=20, y=20,width=620)
    Label(Idea_panel, text="Insight", font=("Bahnschrift Bold",14),fg="white",bg="#282A39").place(x=20, y=10)

    Button(Main_win, text='Choose Image', font=Font,fg="white",bg=Main_window_colour, height = 2,width=40,command = choose_file).place(x=300, y=250)
    Button(Main_win, text='Encode!',font=Font,fg="white",bg=Main_window_colour,command = Enc_cmd, height = 2,width=15).place(x=800, y=250)

def Enc_cmd():
    log_widget.delete(2.0,END)
    if not 'filename' in globals():
        mb.showerror("ERROR","You have not yet entered the file path.")
        return None
    dte = ED.Give_time_and_date()
    Tmp_str ="\n"+dte+" >> Loading image..."
    log_widget.insert(tk.INSERT,Tmp_str)

    try:
        ED.Loading_image(filename)

        dte = ED.Give_time_and_date()
        Tmp_str ="\n"+dte+" >> Encoding image..."
        log_widget.insert(tk.INSERT,Tmp_str)
        try:
            tme,Img_name,Img_data = ED.Encode_img()

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
                connector.execute(
               'INSERT INTO Img_database (ImageNAME, DATA) VALUES (?,?)', (Img_name,Img_data)
               )
                connector.commit()

                dte = ED.Give_time_and_date()
                Tmp_str ="\n"+dte+" >> Saved successfully"
                log_widget.insert(tk.INSERT,Tmp_str)
            except:
                dte = ED.Give_time_and_date()
                Tmp_str ="\n"+dte+" >> [ERROR] Save Failed"
                log_widget.insert(tk.INSERT,Tmp_str)
        except:
            dte = ED.Give_time_and_date()
            Tmp_str ="\n"+dte+" >> [ERROR] Encoding failed"
            log_widget.insert(tk.INSERT,Tmp_str)


    except:
        dte = ED.Give_time_and_date()
        Tmp_str ="\n"+dte+" >> [ERROR] The path of the image is invalid."
        log_widget.insert(tk.INSERT,Tmp_str)

    del Tmp_str,dte

    #Button(Main_win, text='Open File Location', font=Font,fg="white",bg=Main_window_colour, height = 2,width=15,command = lambda: os.startfile(filename)).place(x=810, y=500)


    #Todo2 Solve the issue where it hangs if it is a big image


    #log_widget.configure(state ='disabled')

def Download_gui_load():

    Insight_text = """
    Please select the name of your desired image. Upon selecting your
    image, it will decode your image and save it in your local downloads folder.
    """
    Ins_txt = Label(Idea_panel, text=Insight_text, font=("Bahnschrift Light",12),fg="white",bg="#282A39").place(x=20, y=20,width=620)
    Ins = Label(Idea_panel, text="Insight", font=("Bahnschrift Bold",14),fg="white",bg="#282A39").place(x=20, y=10)

    Frame(Main_win,background=Main_window_colour).place(relx=0.23,rely=0.34,relheight=1,relwidth=1)

    ''' Search Function (Incomplete)
    Button(Main_win, text='Search', font=Font,fg="white",bg=Main_window_colour,command = display_records).place(relx=0.8,y=230,relheight=0.06,relwidth=0.1)

    Key_word = ""
    Entry(Main_win, textvariable=Key_word, font=("Bahnschrift Light",18)).place(relx=0.26,y=230,relheight=0.06,relwidth=0.4)
    '''
    Button(Main_win, text='Download Image', font=Font,fg="white",bg=Main_window_colour,command= Download_record).place(relx=0.8,rely = 0.89,relheight=0.1,relwidth=0.18)
    Button(Main_win, text='Delete Record', font=Font,fg="white",bg=Main_window_colour,command= Delete_Record).place(relx=0.6,rely = 0.89,relheight=0.1,relwidth=0.18)
    Button(Main_win, text='Clear All', font=Font,fg="white",bg=Main_window_colour,command= Clear_all).place(relx=0.4,rely = 0.89,relheight=0.1,relwidth=0.18)


    global tree
    tree = ttk.Treeview(Main_win, height=100, selectmode=BROWSE,
                   columns=('Sr_No',"Name"))
    X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
    X_scroller.pack(side=BOTTOM, fill=X)
    tree.config(xscrollcommand=X_scroller.set)
    tree.heading('Sr_No', text='Sr_No', anchor=W)
    tree.heading('Name', text='Name', anchor=CENTER)
    tree.column('#0', width=0, stretch=NO)
    tree.column('#1', width=40, stretch=NO)
    tree.place(relx=0.26,y=280,relheight=0.37,relwidth=0.6)
    display_records()

    #Todo Make everything scalable
Insight_text = """
    Secure Imaging database is a project inspired by Google Photos. It uses a custom
    encoding and decoding algorithem to secure your image files.
    """

Main_win = Tk()                                                                 #Creating Main window

Main_window_colour = '#28293F'
Side_panel_colour ='#1C2028'
Font = ("Bahnschrift Bold",12)

Main_win.title("Secure Imaging Database")                                       # Main window config
Main_win.geometry('1010x600')
Main_win.configure(bg=Main_window_colour)

Side_panel = Frame(Main_win, background=Side_panel_colour)                      # Side panel config
Side_panel.place(x=0, y=0, relheight=1, relwidth=0.23)

Shadow = Frame(Main_win,background="#1C2028")
Shadow.place(x=257, y=70, relheight=0.21, relwidth=0.675)

#Todo Figure out how to delete the frames
Idea_panel = Frame(Main_win,background="#282A39")
Idea_panel.place(x=264, y=75, relheight=0.19, relwidth=0.66)


Label(Idea_panel, text=Insight_text, font=("Bahnschrift Light",12),fg="white",bg="#282A39").place(x=20, y=20,width=620)
Label(Idea_panel, text="Insight", font=("Bahnschrift Bold",14),fg="white",bg="#282A39").place(x=20, y=10)

Label(Side_panel, text="Secure Imaging Database", font=("Bahnschrift Light",12),fg="white",bg=Side_panel_colour).place(x=12, y=20)
                                                                                #^ Logo

Button(Side_panel, text='Upload Image', font=Font,fg="white",bg=Side_panel_colour, height = 2,width=15,command = Upload_gui_load).place(x=40, rely=0.23)
Button(Side_panel, text='Download Image', font=Font,fg="white",bg=Side_panel_colour, height = 2,width=15,command = Download_gui_load).place(x=40, rely=0.40)
                                                                                #^ Upload and Download options



Main_win.mainloop()