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

Debug_mode,Loaded,c = True,False,0
while Loaded != True:
    try:
        from PIL import Image                                       #Importing third-party libraries
        import os,sys,time,random
        Loaded = True
    except:
        print("\n[ERROR] An error occured while loading libraries\nAttempting to download libraries...")
        from os import system
        system("pip install Pillow --user")                         #Attempting to download libraries if not found
    if c == 2:
        print("[ERROR] An error occured while loading libraries. Please Re-run the program")
        sys.exit()
    c+=1

def Encode(Nums):
    Nums = str(Nums)

    if len(Nums) != 3:                                              # Checks if the provided data is a 3 digit no. or not
        p = 3-len(Nums)
        for v in range(p):
            Nums+="N"                                               # If not then it adds 'N' which just signifies "none"

    Computed_nums_lst = []
    Computed_nums = ""

    #      0   1   2   3   4   5   6   7   8   9   N
    l1 = ["a","b","c","d","e","f","g","h","i","j","x"]              # Key,Value table
    l2 = ["K","L","M","N","O","P","Q","R","S","T","Y"]
    l3 = ["!","@","#","$","%","^","&","*","-","~","="]

    Key = random.randint(0,9)                                       # Selects a random Key

    for i in Nums:
        if i != "N":
            pointer = int(i)+Key                                    # Adds the key to the numeric value of the colour
            if pointer >= 10:
                pointer = pointer - 10                              # If it is greater than 10, it loops around.

            Hash = random.randint(1,3)                              # Selecting one of the char lists

            if Hash == 1:
                Computed_nums_lst.append(l1[pointer])
            if Hash == 2:
                Computed_nums_lst.append(l2[pointer])
            if Hash == 3:
                Computed_nums_lst.append(l3[pointer])
        else:                                                       # Else condition where value of 'i' is "none"
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

    return Key,Computed_nums                                        # Returns Key and Encoded colour data

def Decode(Hashed_str):

    decoded = ""

    #      0   1   2   3   4   5   6   7   8   9   N
    l1 = ["a","b","c","d","e","f","g","h","i","j","x"]              # Key-Value table
    l2 = ["K","L","M","N","O","P","Q","R","S","T","Y"]
    l3 = ["!","@","#","$","%","^","&","*","-","~","="]

    Key = int(Hashed_str[0])                                        # Obtains the Key
    Value = Hashed_str[1:4]                                         # Obtains the Value

    for i in Value:                                                 # Checks index of the number in value
        if i in l1:
            pointer = l1.index(i)
        if i in l2:
            pointer = l2.index(i)
        if i in l3:
            pointer = l3.index(i)

        pointer -= Key                                              # Subtracts using key to get real number

        if pointer<0:
            pointer+=10

        if i != "x" and i != "Y" and i != "=":                      # Checks for 'x','Y','=' which signify "none"
            decoded+=str(pointer)

    del Key,Value,pointer,l1,l2,l3                                  # Deleting un-used variables to save RAM

    return decoded                                                  # Returns decoded colour value

def Convert_to_JPG(path):
    F = "muk\muk"
    F = F.replace("muk","")
    F = path.split(F)
    F = F[-1]
    F = F.split(".")
    F = F[0]
    new_path = F+".jpg"
    im = Image.open(path)
    im4 = im.convert('RGB')                                         # Converting to jpg format
    im4.save(new_path)                                              # Saving temp jpg image

    del im4                                                         # Deleting un-used variables to save RAM
    return new_path

def Loading_image(Image_path):
    #---------------------- Loading Image ----------------------
    global Delete,pix,im,m,n,Encoded,start_time,NIP

    if '"' in Image_path:
        Image_path = Image_path.replace('"','')
    if "/" in Image_path:
        F="muk\muk"
        F=F.replace('muk','')
        Image_path = Image_path.replace("/",F)
    try:

        F = "muk\muk"
        F = F.replace("muk","")
        F = Image_path.split(F)
        F = F[-1]
        F = F.split(".")
        F = F[1]
        Delete = False
        if F != "jpg":
            Image_path = Convert_to_JPG(Image_path)                 # This program works only on jpg files and hence
            Delete = True                                           # will convert any non-jpg files to a temp jpg
        im = Image.open(Image_path)                                 # and will delete the temp jpg after execution
        start_time = time.perf_counter ()

    except:
        print("The path of the image is invalid, please try again!")
        if Debug_mode == True:
            print("\n",Image_path)
        sys.exit()

    pix = im.load()                                                 # Loading the image
    m,n=im.size                                                     # Obtaining size of image
    Encoded =""
    NIP = Image_path

    del F

def Encode_img():
    global Delete,pix,im,m,n,Encoded,start_time,NIP

    #---------------------- Encoding ----------------------         # Start of Encoding process

    print("\nEncoding image...")
    F = "muk\muk"
    F = F.replace("muk","")
    F = NIP.split(F)
    F = F[-1]
    F = F.split(".")
    F = F[0]
    Img_name = F
    Img_data = ''

    try:
        for i in range(m):                                          # m = no. of rows
            for j in range(n):                                      # n = no. of columns
                tup = pix[i,j]                                      # pix[i,j] --> Gets the RGB data of the pixel
                for k in tup:
                    E,C = Encode(k)                                 # RGB value encoded via Encode() function
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

    if Delete == True:                                              # Checks if there was a temp JPG image created
          os.remove(NIP)                                            # in case the image was of a different format
    del Delete,F,Encoded                                            # and deletes it.
    return Tell_time(start_time),Img_name,Img_data

def Decode_data(Img_name,Encoded_inp):

    start_time = time.perf_counter ()
    #---------------------- Decode Loading ----------------------
    Decoded_lst = []
    Decoded_lst1 = []
    pixel_data = []
    Encoded_str = ''

    #---------------------- Decoding ----------------------
    print("\nDecoding...")

    c=1
    try:
        pixel_encoding = Encoded_inp.split(".")                     # The encoding has two parts:


        for Char in pixel_encoding[0]:                              # Seperates chunks of encoded pixel data
            Encoded_str+=Char
            if c % 4 == 0:
                Decoded_lst.append(Decode(Encoded_str))             # Decodes encoded pixel data
                Encoded_str=''
            c+=1


        c=1

        for Char in Decoded_lst:
            Decoded_lst1.append(Char)
            if c % 3 == 0:
                R = int(Decoded_lst1[0])
                G = int(Decoded_lst1[1])
                B = int(Decoded_lst1[2])
                #A = int(Decoded_lst1[3])
                #print("(",R,",",G,",",B,",",A,")")
                pixel_data.append((R,G,B))                          # Joins all the un-organised pixel data
                Decoded_lst1 = []
            c+=1

        del Decoded_lst,Encoded_str                                 # Deleting un-used variables to save RAM

        Dimension_lst = Encoded_inp.split(".")[1]
        Dimension_lst = Dimension_lst.split("?")
        m,n = int(Dimension_lst[0]),int(Dimension_lst[1])           # Gets dimension data from Encoded_inp
    except:
        print("\n[ERROR] Decryption Failed. Please verify file contents")
        sys.exit()

    del Encoded_inp                                                 # Deleting un-used variables to save RAM

    #---------------------- Converting into an image ----------------------
    x,y=0,0
    print("File Decoded\n\nInitializing image generation...")

    try:
        image = Image.new('RGB', (m, n))                            # Creates a new image

        index = -1
        for x in range(m):
            for y in range(n):
                index += 1

                color = pixel_data[index]
                image.putpixel((x, y), color)                       # Assigns colour to pixel using xy co-ordinate data
        print("Image Generated succesfully")
    except:
        print("\n[ERROR] Image Generation Failed")
        if Debug_mode == True:
            print("\n",m,"x",n,"\n",index,"\n",Encoded_file_name)
        sys.exit()


    #---------------------- Saving Image ----------------------
    print("\nSaving Image...")
    try:
        path = './Pictures'
        os.mkdir(path)
    except:
        pass
    try:
        image.save('Pictures/{}.png'.format(Img_name))                           # Saves the generated image in the downloads
    except:
        print("[ERROR] Image was not saved.")
        sys.exit()
    print("Image saved succesfully")
    os.startfile('Pictures/{}.png'.format(Img_name))                             # Opens the saved image
    Tell_time(start_time)
    #Todo Return function with all the necesary things for console

def Tell_time(start_time):
    end_time = time.perf_counter ()
    ao = (end_time - start_time)//1
    if ao>=60:
        ao = str(ao//60) +" Min " + str(ao%60)
    return (" Time for execution : "+str(int(ao))+ " Sec")          # Calculates and prints the time taken for execution of the program

def Give_time_and_date():
    from datetime import date
    from datetime import datetime
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    today = date.today()
    dte = today.strftime("%b-%d-%Y")
    DT = dte+" "+current_time
    return DT
