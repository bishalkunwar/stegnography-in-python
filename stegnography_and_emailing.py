# Python program implementing Image Steganography
 
# PIL module is used to extract
# pixels of image and modify it
import smtplib, ssl
from PIL import Image
 
# Convert encoding data into 8-bit binary
# form using ASCII value of characters
def genData(data):
 
        # list of binary codes
        # of given data
        newd = []
 
        for i in data:
            newd.append(format(ord(i), '08b'))
        return newd
 
# Pixels are modified according to the
# 8-bit binary data and finally returned
def modPix(pix, data):
 
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)
 
    for i in range(lendata):
 
        # Extracting 3 pixels at a time
        pix = [value for value in imdata.__next__()[:3] +
                                imdata.__next__()[:3] +
                                imdata.__next__()[:3]]
 
        # Pixel value should be made
        # odd for 1 and even for 0
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j]% 2 != 0):
                pix[j] -= 1
 
            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if(pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1
                # pix[j] -= 1
 
        # Eighth pixel of every set tells
        # whether to stop ot read further.
        # 0 means keep reading; 1 means thec
        # message is over.
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if(pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1
 
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1
 
        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]
 
def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)
 
    for pixel in modPix(newimg.getdata(), data):
 
        # Putting modified pixels in the new image
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1
 
# Encode data into image
def encode():
    img = input("Enter image name(with extension) : ")
    image = Image.open(img, 'r')
 
    data = input("Enter data to be encoded : ")
    if (len(data) == 0):
        raise ValueError('Data is empty')
 
    newimg = image.copy()
    encode_enc(newimg, data)
 
    new_img_name = input("Enter the name of new image(with extension) : ")
    print("Data encrypted successfully")
    #newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))
    return newimg.save(new_img_name)
 
# Decode the data in the image
def decode():
    img = input("Enter image name(with extension) : ")
    image = Image.open(img, 'r')
 
    data = ''
    imgdata = iter(image.getdata())
 
    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                                imgdata.__next__()[:3] +
                                imgdata.__next__()[:3]]
 
        # string of binary data
        binstr = ''
 
        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'
 
        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data

def mails():

    port = 587  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = input("Enter the sender email address:") #"beesalsk@gmail.com"  Enter your address
    password =  input("Enter the sender email password: ")
    receiver_email = input("Enter the receiver email address:") #"bishal.kunwar487@gmail.com" Enter receiver address
    ''' message = """\
    Subject: Hi there

    This message is sent from Python."""
    '''
    #encode()
    message = encode()
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
    
# Main Function
def main():
    a = int(input("***Welcome to Steganography***\n"
                        "1. Encode\n2. Decode\n"))
    if (a == 1):
        mails()
 
    elif (a == 2):
        print("Decoded Word: \n")
        decode()
    else:
        raise Exception("Enter correct input")
 
# Driver Code
if __name__ == '__main__' :
 
    # Calling main function
    main()


'''Output sample:

***Welcome to Steganography***
1. Encode
2. Decode
1
Enter the sender email address:beesalsk@gmail.com
Enter the sender email password: my email password.
Enter the receiver email address:bishal.kunwar487@gmail.com
Enter image name(with extension) : bishal.jpg
Enter data to be encoded : hello, bishal.
Enter the name of new image(with extension) : bishal1.jpg
Data encrypted successfull

error thrown == nonlength of emails at line number 144.
i.e: object of type 'NoneType' has no len()

decodings:

***Welcome to Steganography***
1. Encode
2. Decode
2
Decoded Word: 

Enter image name(with extension) : bishal1.jpg


but here, no data is decoded, can't find what is the error. '''



