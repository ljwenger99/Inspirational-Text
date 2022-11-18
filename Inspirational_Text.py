#Lucas Wenger
#Project 3 - Inspirational Text
#Due Nov. 9, 2018
#Accepts a text from the user and can perform a variety of functions on it

import sys
import random

#Starter code from https://medium.freecodecamp.org/send-emails-using-code-4fcea9df63f
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendEmail(sender, sendee, header, body, password):
    s = smtplib.SMTP(host='smtp.office365.com', port=587)
    s.starttls()
    s.login(sender, password)
    msg = MIMEMultipart()
    msg['From']= sender
    msg['To']= sendee
    msg['Subject']= header
    msg.attach(MIMEText(body, 'plain'))
    s.send_message(msg)
    del msg
    s.quit()

#DUMMY ACCOUNT ADDRESS + PASSWORD
'''
email - note2self2018@hotmail.com
password - inspiration4u
'''

def find(key, text, number=0): 
    key = key.lower()
    tlistlower = text.lower().split()
    tlist = text.split()
    if key in tlistlower:
        for i in range(0,number):
                tlistlower[tlistlower.index(key)] += "("+str(i+1)+")"
                if key not in tlistlower:
                    return "\nI'm sorry, it seems that word does not appear any more in the file."
        if tlistlower.index(key) < 15:
            return " ".join(tlist[:tlistlower.index(key)+15])
        elif tlistlower.index(key) >= 50:
            return " ".join(tlist[tlistlower.index(key)-15:tlistlower.index(key)+15])
    else:
        return "\nI'm sorry, it seems that word is not in the file."

def GoodnessCaesarDecoder(ctext):
   letterGoodness = [0.0817, 0.0149, 0.0278, 0.0425, 0.127, 0.0223, 0.0202, 0.0609, 0.0697, 0.0015, 0.0077, 0.0402, 0.0241, 0.0675, 0.0751, 0.0193, 0.0009, 0.0599, 0.0633, 0.0906, 0.0276, 0.0098, 0.0236, 0.0015, 0.0197, 0.0007]
   alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0'
   goodnessval = []
   for S in range(0,27):
      tempvar = 0
      for i in "".join(ctext.upper().split()):
         tempvar += letterGoodness[((ord(i)-65)-S) % 25]
      goodnessval.append(tempvar)
   tempstr = ''
   for i in ctext.upper():
      if i not in alphabet:
         tempstr += i
      else:
         tempstr += alphabet[(alphabet.index(i) - goodnessval.index(max(goodnessval))) % 26]
   return tempstr

def caesar(text,shift):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    codedstr = ''
    for i in text.upper():
        if i in alphabet:
            codedstr += alphabet[(alphabet.index(i) + shift) % 26]
        else:
            codedstr += i
    return codedstr

def checker(text,shift):
    print (caesar(text,shift))
    user = input("\nDo you recognize the sample as English?\nIf so, please enter 'y' to continue. If not, enter any other key.\n")
    if user == 'y':
        return True
    else:
        return False
    
def decode(text):
    for i in range(26):
        isenglish = checker(text,i)
        if isenglish == True:
            return caesar(text,i)
        if isenglish == False:
            continue
        
#Greet the user and ask them to input the name of a textfile 
filename = input("Greetings master! My name is Jeeves, and I am here to assist you with all your textfile needs.\nIf you would be so kind, please input the name of file you would like assistance with or 'q' to quit:\n")
while True:
    try:
        with open(filename, 'r+') as f:
            text = f.read()
        break
    except FileNotFoundError:
        if filename == 'q':
            sys.exit()
        filename = input("I'm sorry, it seems I could not find your file. \nPlease input another file name (ex: filename.txt) or 'q' to quit:\n")
        continue
while True:    
    #Generate a menu 
    print("\nWhat would you like me to do with the file?\n\n")
    print("1. Count how many times a sequence of characters occurs")
    print("2. Find a word")
    print("3. Search and replace (CASE SENSITIVE - creates a new file)")
    print("4. Encode text (creates a new file)")
    print("5. Decode text (can create new file)")
    print("6. Send an email with either random text or a keyword or keyphrase")
    user = ''
    while user not in ['1','2','3','4','5','6','q']:
        user = input("\nenter an integer 1 through 6; press 'q' to quit\n")

    #1 - Search for word or phrase and count times it occurs - Searches for sequence of characters
    if user == '1':
        key = input("What sequence of characters would you like to count?\n").lower() 
        num = text.lower().count(key)
        print("\"" + key + "\" appears " + str(num) + " times in the text.")

    #2 - Search for word and print out ~100 characters around the word - Searches for EXACT WORD
    #  - Cycle through places where the word occurs and let user either go to next occurance or main menu
    elif user == '2':
        key = input("What word would you like to find?\n")
        cont = 'c'
        number = 0
        while cont == 'c':
            print(find(key,text,number))
            if find(key,text,number) == "\nI'm sorry, it seems that word is not in the file." or find(key,text,number) == "\nI'm sorry, it seems that word does not appear any more in the file.":
                break
            number += 1
            cont = input("\nFind the next occurance? Press 'c' to continue or any other key to return to the main menu.\n")
    #3 - Do a search and replace - Searches for sequence of characters
    elif user == '3':
        search = input("What would you like to search for?\n")
        replace = input("What would you like to replace it with?\n")
        newfilename = input("What would you like to name the new file? (leave out '.txt')\n")
        textcopy = text.replace(search,replace)
        with open(newfilename+'.txt', 'w+') as f:
            f.write(textcopy)
        print("\nNew file \""+newfilename+".txt\" created. If you desire assistance with the new file, please exit and relaunch the program.\n") 

    #4 - Encode text and save as new file 
    elif user == '4':
        s = input("Enter a shift value between 1 and 25 or anything else for a random shift value\n")
        if s not in range(1,26):
            s = random.randint(1,25)
        newfilename = input("What would you like to name the new file? (leave out '.txt')\n")
        codedtext = caesar(text,s)
        with open(newfilename+'.txt', 'w+') as f:
            f.write(codedtext)
        print("\nEncoded file \""+newfilename+".txt\" created. If you desire assistance with the new file, please exit and relaunch the program.\n")

    #5 - Decode file
    elif user == '5':
        method = input("Attempt to auto-decode? Press 'y' to do so or any other key to brute force it.\n")
        if method == 'y':
            decodedtext = GoodnessCaesarDecoder(text)
            print(decodedtext)
            save = input("\nWould you like to save decoded text as a file? Press 's' to save as a file or any other key to return to main menu.\n")
            if save == 's':
                newfilename = input("What would you like to name the new file? (leave out '.txt')\n")
                with open(newfilename+'.txt', 'w+') as f:
                    f.write(decodedtext)
                print("\nDecoded file \""+newfilename+".txt\" created. If you desire assistance with the new file, please exit and relaunch the program.\n")
        else:
            decodedtext = decode(text)
            save = input("Would you like to save decoded text as a file? Press 's' to save as a file or any other key to return to main menu.\n")
            if save == 's':
                newfilename = input("What would you like to name the new file? (leave out '.txt')\n")
                with open(newfilename+'.txt', 'w+') as f:
                    f.write(decodedtext)
                print("\nDecoded file \""+newfilename+".txt\" created. If you desire assistance with the new file, please exit and relaunch the program.\n")

    #6 - Send an email with either a chunk of text with keyword or random chunk of text - keyword is by EXACT WORD
    elif user == '6':
        try:
            useremail = input("Please enter your email address:\n")
            chunktype = input("Would you like to send a random chunk of text or text around a certain keyword? Press 'k' to enter a keyword or anything else for a random chunk.\n")
            if chunktype == 'k':
                tryagain = 'y'
                while tryagain == 'y':
                    key = input("What would you like the keyword to be?\n")
                    if key in text:
                        body = find(key,text,random.randint(0,(text.lower().split().count(key.lower())-1)))
                        break
                    else:
                        tryagain = input("It seems that word is not in the text. Input another keyword? Press 'y' to try again or any other key to return to the main menu.\n")
                header = "Inspirational Theme: "+key
            else:
                randcharintext = random.randint(0,len(text)-1)
                if randcharintext < 50:
                    body = text[0:randcharintext+50]
                else:
                    body = text[randcharintext-50:randcharintext+50]
                header = "Random Inspiration"
            sendEmail("note2self2018@hotmail.com", useremail, header, body, "inspiration4u")
            print("\nYour email has been sent!\n")
        except:
            print("\nFailed to send email. Returning to main menu.\n")
    #q - Quit
    elif user == 'q':
        print("Farewell master! I'll be awaiting your command.")
        sys.exit()

