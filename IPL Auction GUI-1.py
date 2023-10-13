#-------------------------------------------------------------------------------
# Name:        IPL Auction Systems 1.1
#
# Created:     10 10 2023
#
# Lead Devs:   Om Kumbhar
#              Divyansh Karn
#              Meit Sant
#-------------------------------------------------------------------------------
'''
1.1 Release Notes :-
- Created 3 new tables for players bought [MI,CSK and UNSOLD]
- Added function that will add players to their respective team tables
- Unsold players have a separate table
- At the end a tkinter GUI table will be displayed

Todo for Ver 1.2 :-
- Do Performance improvements [Agar ata hei tohi karna, nahi toh don't waste extra time.]
- Add more comments [Text that explains the code].
- Clean up the code for presentation to ma'am.
- Learn what each function does in case the examiner asks.

'''
from tkinter import *
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import tkinter.font as tkfont
from io import BytesIO
from decimal import Decimal
import requests,sys,sqlite3,time

Timer_Seconds = 10

# Try Connection to the database
try:
    connector = sqlite3.connect('IPL_database.db')
    cursor = connector.cursor()
    print('Connection to Database Established succesfully')

    connector.execute('DELETE FROM UNSOLD')
    connector.execute('DELETE FROM CSK')
    connector.execute('DELETE FROM MI')
    connector.commit()
except:
    print('Connection failed. Database corrupted or not found')
    sys.exit()
# Syntax for SQL :
#   Read -
#        Query = connector.execute('SQL Query')     <----- This will execute the query
#        Data = Query.fetchall()                    <----- This will fetch the output from the last query
#   Write -
#        connector.execute('SQL Query')             <----- This will execute the query
#        connector.commit()                         <----- This will write the changes to the database


def mi_bid():
    global current_bid, current_price, timer, time_remaining, mi_purse, csk_purse, mi_purse_label

    if current_bid != "MI":
        if current_price + Decimal('0.2') <= mi_purse:
            current_bid = "MI"  # Update the current bidding player
            current_price += Decimal('0.2')  # Increase the current bidding price by 20 lakhs
            update_auction_details()
            reset_timer()
            csk_button.config(state=tk.NORMAL)
        else:
            print("MI: Insufficient funds!")
    else:
        print("MI: You have already bid!")

def csk_bid():
    global current_bid, current_price, timer, time_remaining, mi_purse, csk_purse, csk_purse_label

    if current_bid != "CSK":
        if current_price + Decimal('0.2') <= csk_purse:
            current_bid = "CSK"  # Update the current bidding player
            current_price += Decimal('0.2')  # Increase the current bidding price by 20 lakhs
            update_auction_details()
            reset_timer()
            mi_button.config(state=tk.NORMAL)
        else:
            print("CSK: Insufficient funds!")
    else:
        print("CSK: You have already bid!")

def update_auction_details():
    global bidding_player_label,bidding_price_label
    bidding_player_label.config(text=f"Current Bid: {current_bid}")
    bidding_price_label.config(text=f"Current Price: {current_price:.2f} CR")

def reset_timer():
    window.after_cancel(timer)
    start_timer()

def start_timer():
    global timer, time_remaining
    time_remaining = Timer_Seconds
    timer_label.config(text=f"Time Remaining: {time_remaining} seconds")
    timer = window.after(1000, update_timer)

def update_timer():
    global timer, time_remaining

    time_remaining -= 3
    timer_label.config(text=f"Time Remaining: {time_remaining} seconds")

    if time_remaining <= 0:
        timer_expired()
        start_timer()
    else:
        timer = window.after(1000, update_timer)

def timer_expired():
    global current_bid, time_remaining, current_price, mi_purse, csk_purse, Number, Data
    timer_label.config(text="Time Remaining: 10 seconds")
    if current_bid == "":
        # No bid within the time limit
        messagebox.showinfo("Auction Result", "Player Unsold")
        connector.execute(f'INSERT INTO UNSOLD VALUES("{Data[1]}")')
        connector.commit()
        Number = Update_Player(Number)
    else:
        # Display which team won
        messagebox.showinfo("Auction Result", f"{current_bid} won the bid!")

        if current_bid == "MI":
            mi_purse -= current_price  # Deduct money from MI purse
            connector.execute(f'INSERT INTO MI VALUES("{Data[1]}")')
            connector.commit()
        if current_bid == "CSK":
            csk_purse -= current_price  # Deduct money from CSK purse
            connector.execute(f'INSERT INTO CSK VALUES("{Data[1]}")')
            connector.commit()
        update_purse_labels()
        Number = Update_Player(Number)
    current_bid = ""  # Reset current bid
    current_price = Decimal('2.0')  # Reset bidding price
    update_auction_details()
    return

def update_purse_labels():
    # Check if mi_purse_label exists
    if 'mi_purse_label' in globals():
        mi_purse_label.config(text=f"MI Purse: {mi_purse:.2f} CR")
    # Check if csk_purse_label exists
    if 'csk_purse_label' in globals():
        csk_purse_label.config(text=f"CSK Purse: {csk_purse:.2f} CR")

def Update_Player(Num):
    global player_No_Label, name_Label, position_Label, age_Label, Data

    try:
        player_No_Label.destroy()
        name_Label.destroy()
        position_Label.destroy()
        age_Label.destroy()
    except:
        pass

    Num += 1

    Query = connector.execute(f'SELECT * FROM Player_Data WHERE PlayerNumber = {Num};')
    Data = Query.fetchall()
    if Data == []:
        # Fetching the teams from the database
        Query = connector.execute('SELECT * FROM CSK')
        CSK = Query.fetchall()
        Query = connector.execute('SELECT * FROM MI')
        MI = Query.fetchall()
        Query = connector.execute('SELECT * FROM UNSOLD')
        UNSOLD = Query.fetchall()
        # Formating the data for the table func
        formatted_data = [['MI', 'CSK', 'UNSOLD']]
        no_Of_Entries = max([len(CSK),len(MI),len(UNSOLD)])
        for i in range(no_Of_Entries):
            row = []
            for lst in [MI,CSK,UNSOLD]:
                if i < len(lst):
                    row.append(lst[i][0])
                else:
                    row.append('')
            formatted_data.append(tuple(row))
        rows = no_Of_Entries
        columns = 3
        # Shows the table
        show_Table(formatted_data,rows,columns)
        if messagebox.askyesno('IPL Auction System','Do you want to restart ?') == False:
            window.destroy()
            sys.exit()
        else:
            Num = 1
            Query = connector.execute(f'SELECT * FROM Player_Data WHERE PlayerNumber = {Num};')
            Data = Query.fetchall()
    Data = list(Data[0])

    # Create the labels for player information fields
    fields = [f"Player No: {Data[0]}", f"Name: {Data[1]}", f"Position: {Data[2]}", f"Age: {Data[3]}"]

    player_No_Label = tk.Label(info_frame, text=fields[0], font=("Arial", 14), bg="#ADD8E6")
    player_No_Label.grid(sticky="w", padx=10, pady=5)

    name_Label = tk.Label(info_frame, text=fields[1], font=("Arial", 14), bg="#ADD8E6")
    name_Label.grid(sticky="w", padx=10, pady=5)

    position_Label = tk.Label(info_frame, text=fields[2], font=("Arial", 14), bg="#ADD8E6")
    position_Label.grid(sticky="w", padx=10, pady=5)

    age_Label = tk.Label(info_frame, text=fields[3], font=("Arial", 14), bg="#ADD8E6")
    age_Label.grid(sticky="w", padx=10, pady=5)

    return Num

def transition_to_auction_page():
    global Number, info_frame, purse_frame, mi_player_frame, csk_player_frame

    # Destroy the opening page widgets
    opening_label.destroy()
    image_label.destroy()

    # Create the IPL auction page widgets
    custom_font = tkfont.Font(family="Arial", size=30, weight="bold")
    auction_label = tk.Label(window, text="IPL Auction", font=custom_font, bg="#ADD8E6")
    auction_label.pack(pady=20)

    # Create the frame for purses
    purse_frame = tk.Frame(window, bg="#ADD8E6")
    purse_frame.pack(side=tk.TOP, pady=10, fill="x")

    # Create the MI Team label
    mi_team_label = tk.Label(purse_frame, text="Mumbai Indians!", font=("Arial", 16), padx=10, pady=5, bg="blue", fg="white")
    mi_team_label.pack(side="left", anchor="w")

    # Create the CSK Team label
    csk_team_label = tk.Label(purse_frame, text="Chennai Super Kings!", font=("Arial", 16), padx=10, pady=5, bg="yellow", fg="black")
    csk_team_label.pack(side="right", anchor="e")

    # Create the MI Purse label
    global mi_purse_label
    mi_purse_label = tk.Label(purse_frame, text=f"MI Purse: {mi_purse:.2f} CR", font=("Arial", 16), padx=10, bg="#ADD8E6")
    mi_purse_label.pack(side="left", anchor="w")

    # Create the CSK Purse label
    global csk_purse_label
    csk_purse_label = tk.Label(purse_frame, text=f"CSK Purse: {csk_purse:.2f} CR", font=("Arial", 16), padx=10, bg="#ADD8E6")
    csk_purse_label.pack(side="right", anchor="e")

    # Create the frame for buttons
    button_frame = tk.Frame(window, bg="#ADD8E6")
    button_frame.pack(side=tk.BOTTOM, pady=20)

    # Create the MI Bid button
    global mi_button
    mi_button = tk.Button(button_frame, text="MI Bid", command=mi_bid, font=("Arial", 14), bg="white", fg="black")
    mi_button.pack(side=tk.LEFT, padx=50)

    # Create the CSK Bid button
    global csk_button
    csk_button = tk.Button(button_frame, text="CSK Bid", command=csk_bid, font=("Arial", 14), bg="white", fg="black")
    csk_button.pack(side=tk.RIGHT, padx=50)

    # Create the frame for player information box
    info_frame = tk.Frame(window, padx=20, pady=20, bg="#ADD8E6")
    info_frame.pack()

    Number = Update_Player(Number)

    # Create the label for bidding player
    global bidding_player_label
    bidding_player_label = tk.Label(window, text="Current Bid: ", font=("Arial", 16), padx=10, bg="#ADD8E6")
    bidding_player_label.pack()

    # Create the label for bidding price
    global bidding_price_label
    bidding_price_label = tk.Label(window, text="Current Price: ", font=("Arial", 16), padx=10, bg="#ADD8E6")
    bidding_price_label.pack()

    # Create the label for the timer
    global timer_label
    timer_label = tk.Label(window, text="Time Remaining: 10 seconds", font=("Arial", 16), padx=10, bg="#ADD8E6")
    timer_label.pack()

    # Start the timer
    start_timer()

def show_Table(Data,total_rows,total_columns):
    root=Tk()
    root.title("IPL Auction - Teams")
    for i in range(total_rows+1):
        for j in range(total_columns):
            e = Entry(root, width=20, fg='black',
                font=('Arial',16,'bold'))
            e.grid(row=i, column=j)
            e.insert(END, Data[i][j])
    root.mainloop()
    return
# Create the GUI window
window = Tk()
window.title("IPL Auction")

# Maximize the window to cover most of the screen
window.state('zoomed')

# Configure the window background color to light blue
window.configure(bg="#ADD8E6")

# Initialize the current bid and price
current_bid = ""
current_price = Decimal('2.0')

# Initialize the purses
mi_purse = Decimal('95.0')
csk_purse = Decimal('95.0')

# Download the image from the URL
image_url = "https://www.iplt20.com/assets/img/auctiontop.jpg"  # URL of the image
try:
    response = requests.get(image_url)
except:
    print('The net is off.  -_-')
    sys.exit()
image_data = response.content

# Load the image using PIL
opening_image = Image.open(BytesIO(image_data))

# Convert the image to Tkinter-compatible format
opening_photo = ImageTk.PhotoImage(opening_image)

# Create the label to display the image on the opening page
image_label = tk.Label(window, image=opening_photo, bg="#ADD8E6")
image_label.pack()

# Create the label for the opening page
opening_label = tk.Label(window, text="Welcome to the IPL Auction", font=("Arial", 36), pady=100, bg="#ADD8E6")
opening_label.pack()

Number = 0
# Transition to the IPL auction page after 2 seconds
window.after(2000, lambda: transition_to_auction_page())

# Run the GUI event loop
window.mainloop()
connector.close()