#-------------------------------------------------------------------------------
# Name:        ED.py
# Purpose:     Encode, Decode and other functions
#
# Author:      MS Productions
#
# Created:     08 04 2023
# Copyright:   (c)MS Productions
#
# Lead Dev : Meit Sant
#-------------------------------------------------------------------------------
'''
These imports are highly specific. No wildcard imports were made.
(Wildcard imports are those which import everything into the script.
Eg: 'from pandas import *' or just 'import pandas')
'''

from os import path,getlogin,mkdir,startfile,remove,system
from sys import exit
from random import randint
from time import perf_counter
from PIL import Image
from functools import cache

Debug_mode = False

def Encrypt_Pwd(Password):
    '''
    Explanation of str(bin(ord(i))[2:]):

    1. ord(i): Obtains the Unicode code point of the character `i`.
    2. bin(ord(i)): Converts the Unicode code point to its binary representation as a string.
    3. [2:]: Removes the first two characters (`"0b"`) from the binary string.
    4. str(): Converts the resulting binary string to a regular string.
    '''
    Encrypted_Password = ''
    for i in Password:
        Encrypted_Password += str(bin(ord(i))[2:]) + ' '
    return Encrypted_Password

@cache
def Decrypt_Pwd(Encrypted_Password):
    '''
    Explanation of chr(int(j, 2)):

    1. int(j, 2): Converts the binary string j to an integer using base 2.
    2. chr(): Converts the integer back to its corresponding Unicode character representation.
    '''
    Password = ''
    for i in Encrypted_Password.split(' '):
        if i == '':
            return Password
        Password += chr(int(i, 2))
    return Password

def Encode(Nums):
    '''
    Encodes specific pixel colour data to
    numeric encrypted data.
    Example : 255 = 3fS-
    '''
    Nums = str(Nums)

    # Checks if the provided data is a 3 digit no. or not
    if len(Nums) != 3:
        p = 3-len(Nums)
        for v in range(p):
            # If not then it adds 'N' which just signifies "none"
            Nums+="N"

    Computed_nums_lst = []
    Computed_nums = ""

    # Key,Value table

    #      0   1   2   3   4   5   6   7   8   9   N
    l1 = ["a","b","c","d","e","f","g","h","i","j","x"]
    l2 = ["K","L","M","N","O","P","Q","R","S","T","Y"]
    l3 = ["!","@","#","$","%","^","&","*","-","~","="]

    # Selects a random Key
    Key = randint(0,9)

    pntr = 0
    for i in Nums:
        if i != "N":
            # Adds the key to the numeric value of the colour
            pntr = int(i)+Key
            if pntr >= 10:
                # If it is greater than 10, it loops around.
                pntr = pntr - 10

            # Selecting one of the char lists
            Hash = randint(1,3)

            if Hash == 1:
                Computed_nums_lst.append(l1[pntr])
            if Hash == 2:
                Computed_nums_lst.append(l2[pntr])
            if Hash == 3:
                Computed_nums_lst.append(l3[pntr])
        # Else condition where value of 'i' is "none"
        else:
            Hash = randint(1,3)
            if Hash == 1:
                Computed_nums_lst.append(l1[10])
            if Hash == 2:
                Computed_nums_lst.append(l2[10])
            if Hash == 3:
                Computed_nums_lst.append(l3[10])

    for j in Computed_nums_lst:
        Computed_nums += j

    del Hash,pntr,Nums,Computed_nums_lst,l1,l2,l3 # type: ignore

    # Returns Key and Encoded colour data
    return Key,Computed_nums

@cache
def Decode(Hashed_str):
    '''
    This function will decode each singular encoded
    bit into different pixel datas, which will
    later be all arranged into a picture, just like
    manually placing a line of dominos.
    '''
    decoded = ""
    # Key-Value table

    #      0   1   2   3   4   5   6   7   8   9   N
    l1 = ["a","b","c","d","e","f","g","h","i","j","x"]
    l2 = ["K","L","M","N","O","P","Q","R","S","T","Y"]
    l3 = ["!","@","#","$","%","^","&","*","-","~","="]

    # Obtains the Key
    Key = int(Hashed_str[0])
    # Checks index of the number in value
    Value = Hashed_str[1:4]
    pntr = 0

    for i in Value:
        if i in l1:
            pntr = l1.index(i)
        if i in l2:
            pntr = l2.index(i)
        if i in l3:
            pntr = l3.index(i)

        # Subtracts using key to get real number
        pntr -= Key

        if pntr<0:
            pntr+=10

        # Checks for 'x','Y','=' which signify "none"
        if i not in ("x","Y","="):
            decoded+=str(pntr)

    # Deleting un-used variables to save RAM
    del Key,Value,pntr,l1,l2,l3
    # Returns decoded colour value
    return decoded

def Convert_to_JPG(path):
    '''
    The program only works with JPG type images.
    Hence, other types of images such as PNG will
    be temporalily converted and then deleted once
    encode is finished. Example:
    Input : D:\\User\\Pictures\\Cat.png
    Output : Cat.jpg
    '''
    new_path = (path.split("\\")[-1].split(".")[0])+".jpg"
    im = Image.open(path)
    # Converting to jpg format
    im4 = im.convert('RGB')
    # Saving temp jpg image
    im4.save(new_path)

    del im4
    return new_path

def Loading_image(Image_path):
    #---------------------- Loading Image ----------------------
    global Delete,pix,im,m,n,Encoded,start_time,NIP

    if '"' in Image_path:
        Image_path = Image_path.replace('"','')
    if "/" in Image_path:
        Image_path = Image_path.replace("/","\\")
    try:
        Delete = False
        if "jpg" not in Image_path:
            '''
            This program works only on jpg files and hence
            will convert any non-jpg files to a temp jpg image
            and will delete the temp jpg after execution.
            '''
            Image_path = Convert_to_JPG(Image_path)
            Delete = True
        im = Image.open(Image_path)
        start_time = perf_counter()

    except Exception as e:
        print(f"[ERROR] {e}")
        if Debug_mode is True:
            print("\n",Image_path)

    NIP = Image_path

def Encode_img():
    global Delete,pix,im,m,n,Encoded,start_time,NIP

    #---------------------- Encoding ----------------------

    Img_name = NIP.split("\\")[-1].split(".")[0]
    Img_data = ''

    '''
    Here,
    m = no. of rows
    n = no. of columns
    pix[i,j] --> Gets the RGB data of the pixel
    '''

    # Loading the image
    pix = im.load()
    # Obtaining size of image
    m,n=im.size
    Encoded =""

    for i in range(m):
        for j in range(n):
            tup = pix[i,j]
            for k in tup:
                # RGB value encoded via Encode() function
                E,C = Encode(k)
                Encoded+=str(E)
                Encoded+=str(C)
                Img_data+=Encoded
                Encoded = ''

    Img_data+=("."+str(m)+"?"+str(n))


    del tup,k,E,C  # type: ignore
    '''
    Checking if there was a temp JPG image created
    in case the image was of a different format
    and delete it.
    '''
    if Delete is True:
        remove(NIP)

    return Tell_time(start_time),Img_name,Img_data

def Decode_data(Img_name,Encoded_inp,Upscale=None,Scale_Factor=None):

    # Starts the timer for processing
    start_time = perf_counter ()
    Decoded_lst = []
    Decoded_lst1 = []
    pixel_data = []
    Encoded_str = ''

    #---------------------- Decoding ----------------------
    print("\nDecoding...")

    c=1
    try:
        pixel_encoding = Encoded_inp.split(".")
        # Seperates chunks of encoded pixel data
        for Char in pixel_encoding[0]:
            Encoded_str+=Char
            if c % 4 == 0:
                # Decodes encoded pixel data
                Decoded_lst.append(Decode(Encoded_str))
                Encoded_str=''
            c+=1
        c=1
        for Char in Decoded_lst:
            Decoded_lst1.append(Char)
            if c % 3 == 0:
                R = int(Decoded_lst1[0])
                G = int(Decoded_lst1[1])
                B = int(Decoded_lst1[2])

                # Joins all the un-organised pixel data
                pixel_data.append((R,G,B))
                Decoded_lst1 = []
            c+=1
        # Deleting un-used variables to save RAM
        del Decoded_lst,Encoded_str

        Dimension_lst = Encoded_inp.split(".")[1]
        Dimension_lst = Dimension_lst.split("?")

        # Gets dimensions data from Encoded_inp
        m,n = int(Dimension_lst[0]),int(Dimension_lst[1])
    except Exception as e:
        print(f"[ERROR] {e}")
        exit()
    del Encoded_inp

    #---------------------- Converting into an image ----------------------
    x,y=0,0
    print("File Decoded\n\nInitializing image generation...")

    # Creates a new image
    image = Image.new('RGB', (m, n))
    index = -1
    try:
        # Time complexity = O(n^2)
        for x in range(m):
            for y in range(n):
                index += 1
                color = pixel_data[index]

                # Assigns colour to pixel using xy co-ordinate data
                image.putpixel((x, y), color)
        print("Image Generated succesfully")
    except Exception as e:
        print(f"[ERROR] {e}")
        print("\n[ERROR] Image Generation Failed")
        if Debug_mode is True:
            print("\n",m,"x",n,"\n",index,"\n",Img_name)
        exit()

    del index,color,m,n  # type: ignore

    #---------------------- Saving Image ----------------------

    Path = f'C:\\Users\\{getlogin()}\\Downloads\\Pictures'

    if not path.exists(Path):
        mkdir(Path)

    try:
        if Upscale == True:
            print("\nUpscaling Image...")
            width, height = image.size
            image = image.resize((width*Scale_Factor, height*Scale_Factor), Image.BICUBIC) # type: ignore
            print("\nSaving Image...")
            # Saves the generated image in the downloads
            image.save(f'{Path}\\{Img_name}_Upscaled.png')
        else:
            print("\nSaving Image...")
            # Saves the generated image in the downloads
            image.save(f'{Path}\\{Img_name}.png')

    except Exception as e:
        print(f"[ERROR] {e}")
        exit()
    print("Image saved succesfully")
    Tell_time(start_time)
    del image,Path
    return

def Tell_time(start_time):
    # Calculates and prints the time taken for execution of the program
    end_time = perf_counter ()
    ao = (end_time - start_time)
    if ao > 60:
        ao = f"{ao//60} mins {ao%60} seconds"
    else:
        ao = f"{int(ao)} secs"

    return f" Time for execution : {ao}"

def Give_time_and_date():
    """
    As name suggests, it returns the current time
    and date for the console output.
    """
    import datetime
    from datetime import date, datetime
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    today = date.today()
    dte = today.strftime("%b-%d-%Y")
    DT = dte+" "+current_time
    del now,current_time,today,dte
    # Format : Month-Date-Year Hour(24hr):Minute:Seconds
    return DT
