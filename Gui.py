#-------------------------------------------------------------------------------
# Name:        Gui.py
#
# Author:      MS Productions
#
# Created:     09 04 2023
# Copyright:   (c)MS Productions
#
# Lead Dev : Meit Sant
#-------------------------------------------------------------------------------

from tkinter import *
from tkinter.filedialog import askopenfilename
import tkinter.messagebox as mb
from tkinter.scrolledtext import ScrolledText
import ED

global mode




def dummy_cmd():
    if not 'filename' in globals():
        mb.showerror("ERROR","You have not yet entered the file path.")
        return None
    ED.Encode_image(filename)



def choose_file():
    global filename
    filename = askopenfilename()


def Upload_gui_load():

    Insight_text = """
    The program will automatically encode the image chosen with a special encoding
    algorithem. If the database file is compromised, the image data will still be encoded,
    hence making it harder to penetrate.
    """
    #Ins_txt.destroy()
    #Ins.destroy()

    Frame(Main_win,background=Main_window_colour,height=500,width=800).place(x=270,y=210)

    Output_box = Frame(Main_win,background="#7476A7")
    Output_box.place(x=300, y=375, relheight=0.3, relwidth=0.5)

    Label(Output_box,text= 'Console Output',font=Font,background="#7476A7").place(x=0,y=0)

    global log_widget

    log_widget = ScrolledText(Output_box, height=10, width=80, font=("consolas", "8", "normal")).place(x=0,y=30)


    Label(Idea_panel, text=Insight_text, font=("Bahnschrift Light",12),fg="white",bg="#282A39").place(x=20, y=20,width=620)
    Label(Idea_panel, text="Insight", font=("Bahnschrift Bold",14),fg="white",bg="#282A39").place(x=20, y=10)

    Button(Main_win, text='Choose Image', font=Font,fg="white",bg=Main_window_colour, height = 2,width=40,command = choose_file).place(x=300, y=250)
    Button(Main_win, text='Encode!',font=Font,fg="white",bg=Main_window_colour,command = dummy_cmd, height = 2,width=15).place(x=800, y=250)


def Download_gui_load():

    Insight_text = """
    Please enter the name of your desired image. Upon selecting your
    image, it will decode your image and save it in your local downloads folder.
    """
    Ins_txt = Label(Idea_panel, text=Insight_text, font=("Bahnschrift Light",12),fg="white",bg="#282A39").place(x=20, y=20,width=620)
    Ins = Label(Idea_panel, text="Insight", font=("Bahnschrift Bold",14),fg="white",bg="#282A39").place(x=20, y=10)

    Frame(Main_win,background=Main_window_colour,height=500,width=800).place(x=270,y=210)

    Button(Main_win, text='Download Image', font=Font,fg="white",bg=Main_window_colour, height = 2,width=40).place(x=600, y=500)

    Key_word = ""
    Entry(Main_win, width=30, textvariable=Key_word, font=("Bahnschrift Light",18)).place(x=270, y=250)
    Button(Main_win, text='Search', font=("Bahnschrift Bold",15),fg="white",bg=Main_window_colour, height = 1,width=10).place(x=800, y=250)


Insight_text = """
    Secure Imaging database is a project inspired by Google Photos. It uses a custom
    encoding and decoding algorithem to secure your image files.
    """

Main_win = Tk()                                                                 #Creating Main window

Main_window_colour = '#28293F'
Side_panel_colour ='#1C2028'
Font = ("Bahnschrift Bold",12)

Main_win.title("Secure Imaging Database")                                       # Main window config
Main_win.geometry('1000x600')
Main_win.configure(bg=Main_window_colour)

Side_panel = Frame(Main_win, background=Side_panel_colour)                      # Side panel config
Side_panel.place(x=0, y=0, relheight=1, relwidth=0.25)

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