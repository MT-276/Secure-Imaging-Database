#-------------------------------------------------------------------------------
# Name:        Encode and Decode functions.py
#
# Author:      MS Productions
#
# Created:     08 04 2023
# Copyright:   (c)MS Productions
#
# Lead Dev : Meit Sant
#-------------------------------------------------------------------------------
import sys
Debug_mode = False

try:
    # Importing third-party libraries
    from PIL import Image
    import os,time,random
except ModuleNotFoundError:
    print("\n[ERROR] An error occured while loading libraries\nAttempting to download libraries...")
    from os import system
    try:
        # Attempting to download libraries if not found
        system("pip install Pillow==9.5.0 --user")
        from PIL import Image
    except ImportError:
        print("""
[ERROR] An error occured while downloading libraries.
Please try again or contact dev
              """)
        sys.exit()

def Encrypt_Pwd(Password):
    Encrypted_Password = ''
    for i in Password: Encrypted_Password += str(bin(ord(i))[2:]) + ' '
    return Encrypted_Password
def Decrypt_Pwd(Encrypted_Password):
    Password = ''
    for i in Encrypted_Password.split(' '):
        if i == '': return Password
        else: Password += chr(int(i, 2))
    return Password

def Encode(Nums):
    """
    Encodes specific pixel colour data to
    numeric encrypted data.
    Example : 255 = 3fS-
    """
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
    Key = random.randint(0,9)

    for i in Nums:
        if i != "N":
            # Adds the key to the numeric value of the colour
            pointer = int(i)+Key
            if pointer >= 10:
                # If it is greater than 10, it loops around.
                pointer = pointer - 10


            # Selecting one of the char lists
            Hash = random.randint(1,3)

            if Hash == 1:
                Computed_nums_lst.append(l1[pointer])
            if Hash == 2:
                Computed_nums_lst.append(l2[pointer])
            if Hash == 3:
                Computed_nums_lst.append(l3[pointer])
        # Else condition where value of 'i' is "none"
        else:
            Hash = random.randint(1,3)
            if Hash == 1:
                Computed_nums_lst.append(l1[10])
            if Hash == 2:
                Computed_nums_lst.append(l2[10])
            if Hash == 3:
                Computed_nums_lst.append(l3[10])

    for j in Computed_nums_lst:
        Computed_nums += j

    del Hash,pointer,Nums,Computed_nums_lst,l1,l2,l3

    # Returns Key and Encoded colour data
    return Key,Computed_nums

def Decode(Hashed_str):
    #Todo Add Docstring (Decode)
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

    for i in Value:
        if i in l1:
            pointer = l1.index(i)
        if i in l2:
            pointer = l2.index(i)
        if i in l3:
            pointer = l3.index(i)

        # Subtracts using key to get real number
        pointer -= Key

        if pointer<0:
            pointer+=10

        # Checks for 'x','Y','=' which signify "none"
        if i not in ("x","Y","="):
            decoded+=str(pointer)

    # Deleting un-used variables to save RAM
    del Key,Value,pointer,l1,l2,l3
    # Returns decoded colour value
    return decoded

def Convert_to_JPG(path):
    F = "\\"
    F = path.split(F)
    F = F[-1]
    F = F.split(".")
    F = F[0]
    new_path = F+".jpg"
    im = Image.open(path)
    # Converting to jpg format
    im4 = im.convert('RGB')
    # Saving temp jpg image
    im4.save(new_path)

    del im4,F
    return new_path

def Loading_image(Image_path):
    #---------------------- Loading Image ----------------------
    global Delete,pix,im,m,n,Encoded,start_time,NIP

    if '"' in Image_path:
        Image_path = Image_path.replace('"','')
    if "/" in Image_path:
        Image_path = Image_path.replace("/","\\")
    try:

        F = Image_path.split("\\")
        F = F[-1]
        F = F.split(".")
        F = F[1]
        Delete = False
        if F != "jpg":
            """
            This program works only on jpg files and hence
            will convert any non-jpg files to a temp jpg image
            and will delete the temp jpg after execution.
            """
            Image_path = Convert_to_JPG(Image_path)
            Delete = True
        im = Image.open(Image_path)
        start_time = time.perf_counter ()

    except:
        print("The path of the image is invalid, please try again!")
        if Debug_mode is True:
            print("\n",Image_path)
        sys.exit()

    # Loading the image
    pix = im.load()
    # Obtaining size of image
    m,n=im.size
    Encoded =""
    NIP = Image_path

    del F

def Encode_img():
    global Delete,pix,im,m,n,Encoded,start_time,NIP

    #---------------------- Encoding ----------------------

    print("\nEncoding image...")
    F = NIP.split("\\")
    F = F[-1]
    F = F.split(".")
    F = F[0]
    Img_name = F
    Img_data = ''

    """
    Here,
    m = no. of rows
    n = no. of columns
    pix[i,j] --> Gets the RGB data of the pixel
    """
    try:
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

    except:
        print("[ERROR] Encoding failed")
        sys.exit()
    del m,n,i,j,tup,k,E,C
    print("Image Encoded")

    """
    Checking if there was a temp JPG image created
    in case the image was of a different format
    and delete it.
    """
    if Delete is True:
          os.remove(NIP)
    del Delete,F,Encoded
    return Tell_time(start_time),Img_name,Img_data

def Decode_data(Img_name,Encoded_inp):

    # Starts the timer for processing
    start_time = time.perf_counter ()
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
    except:
        print("\n[ERROR] Decryption Failed. Please verify file contents")
        sys.exit()

    del Encoded_inp

    #---------------------- Converting into an image ----------------------
    x,y=0,0
    print("File Decoded\n\nInitializing image generation...")

    try:
        # Creates a new image
        image = Image.new('RGB', (m, n))
        index = -1
        for x in range(m):
            for y in range(n):
                index += 1
                color = pixel_data[index]

                # Assigns colour to pixel using xy co-ordinate data
                image.putpixel((x, y), color)
        print("Image Generated succesfully")
    except:
        print("\n[ERROR] Image Generation Failed")
        if Debug_mode is True:
            print("\n",m,"x",n,"\n",index,"\n",Img_name)
        sys.exit()

    del index,color,m,n

    #---------------------- Saving Image ----------------------
    print("\nSaving Image...")
    try:
        Windows_user_name = os.getlogin()
        path = f'C:\\Users\\{Windows_user_name}\\Downloads\\Pictures'
        os.mkdir(path)
        sys.exit()
    except:
        pass

    try:
        # Saves the generated image in the downloads
        image.save(f'{Img_name}\\{path}.png')
    except:
        print("[ERROR] Image was not saved.")
        sys.exit()
    print("Image saved succesfully")
    #os.startfile('Pictures/{}.png'.format(Img_name))
    Tell_time(start_time)

def Tell_time(start_time):
    end_time = time.perf_counter ()
    ao = (end_time - start_time)//1
    if ao>=60:
        ao = str(ao//60) +" Min " + str(ao%60)
    # Calculates and prints the time taken for execution of the program
    return (" Time for execution : "+str(int(ao))+ " Sec")

def Give_time_and_date():
    """
    As name suggests, it returns the current time
    and date for the console output.
    """
    from datetime import date
    from datetime import datetime
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    today = date.today()
    dte = today.strftime("%b-%d-%Y")
    DT = dte+" "+current_time
    # Format : Month-Date-Year Hour(24hr):Minute:Seconds
    return DT
