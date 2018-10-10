from gmusicapi import Mobileclient
import re
import os

## Define Variables ##
FILENAME = 'user.acc'
api = Mobileclient()

## Define Functions ##
def retrieveLoginDetails():
    print("Please enter your Google Account details")
    print("If your account uses 2-Factor Authentication, you'll need to create an Application Password")

    # input() always gets strings
    print("Enter Username/Email")
    user = input("> ")
    print("Enter Password")
    pasw = input("> ")

    ## Save Login File
    file = open(FILENAME, "w+")
    file.write(user + '\n' + pasw)
    file.close()

    login(user, pasw)

def login(username, password):
    ## Attempt Login
    print("Attempting login with: " + username)
    if api.login(username, password, Mobileclient.FROM_MAC_ADDRESS, 'en_NZ'):
        # On success
        print("Login Successful")
        library = api.get_all_songs()
        # TODO continue code when you figure out how to log in
    else:
        # On fail
        print("Login Unsuccessful")
        answer = 'z'
        while(answer != 'n' and answer != 't' and answer != 'x'):
            print(" Enter n to try a new login")
            print(" Enter t to try again")
            print(" Enter x to exit")
            answer = input("> ")
        # TODO remove the need to press enter
        if answer == 'n': # New Login
            # Remove Login File
            try:
                os.remove(FILENAME)
            except FileNotFoundError:
                pass
            # Create new login
            retrieveLoginDetails()
        elif answer == 't': # Try Again
            login(username, password)
        elif answer == 'x': # Exit
            quit()
        else:
            print("An unexpected error occurred, closing program")
            quit()

## ------------------ MAIN ------------------ ##


## Check File Exists / Open File ##
try:
    file = open(FILENAME)

    # If login file exists, read contents
    fileContents = file.read()
    file.close()

    # Check login file is in correct format
    FormatRe = re.compile(".+\\n.+")
    Match = FormatRe.match(fileContents)
    if Match:
        # Extract Username & Password
        UserPass = Match.group().split('\n')
        login(UserPass[0], UserPass[1])
    else:
        print("ERROR: Login File in Incorrect Format")

        # Remove File
        try:
            os.remove(FILENAME)
        except FileNotFoundError:
            pass
        # Create new login
        retrieveLoginDetails()
except IOError:
    # If login file doesn't exist, create new login
    retrieveLoginDetails()

##### OLDCODE
