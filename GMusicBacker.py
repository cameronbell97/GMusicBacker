from gmusicapi import Mobileclient
import re
import os
import io
import datetime

## Define Variables ##
FILENAME = 'user.acc'
EXPORTDIR = "export"
FORMAT = "TYPE1"
    ## TYPE KEY ##
    # Type 1 = [title],[artist],[album]  - Speech Marks around every field, no commas at end of line
    # Type 2 = [artist],[album],[title]  - Speech Marks only around necessary fields
    # Type 3 = [artist],[album],[title]  - Speech Marks around every field
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
        loggedinmenu()
        # TODO continue code when you figure out how to log in
    else:
        # On fail
        print("Login Unsuccessful")
        print("If you get this error a lot, try visiting https://accounts.google.com/b/0/DisplayUnlockCaptcha")
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

def loggedinmenu():
    # Retrieve Playlists #
    print("Retrieving playlists")
    playlists = api.get_all_user_playlist_contents()
    print("Retrieved " + playlists.__len__().__str__() + " playlists")
    library = api.get_all_songs()
    print("Retrieved library of " + library.__len__().__str__() + " songs")

    # Export Playlists #
    answer = 'z'
    while (answer != 'x'):
        print(" Enter e to export all playlists")
        print(" Enter d to display the playlists")
        print(" Enter x to exit")
        answer = input("> ")
        if(answer == 'd'):
            displayPlaylists(playlists)
        if(answer == 'e'):
            exportPlaylists(playlists, library)
    # TODO remove the need to press enter

    if answer == 'x': # Exit
        quit()
    else:
        print("An unexpected error occurred, closing program")
        quit()

def displayPlaylists(playlists):
    print("Playlists:")
    print(" [#] || [Name] || [Length]")
    count = 0
    for playlist in playlists:
        print(" " + count.__str__() + " || " + playlist['name'] + " || " + playlist['tracks'].__len__().__str__() + " songs")
        count+=1

def exportPlaylists(playlists, library):
    # Get Current Filepath
    now = datetime.datetime.now()
    fpath = EXPORTDIR + '\\' + now.strftime("%Y-%m-%d %H.%M")

    # Make Export Directory
    try:
        if not os.path.exists(EXPORTDIR):
            os.makedirs(EXPORTDIR)

        if not os.path.exists(fpath):
            os.makedirs(fpath)
    except IOError:
        # If export directory string is invalid or directory already exists
        print("Error making export directory, exiting")
        quit()

    try:
        # Scrape Songs
        for playlist in playlists:
            # Make File
            pname = cleanName(playlist['name'])
            newfilename = fpath + "\\" + pname + ".csv"
            file = io.open(newfilename, 'w', encoding="utf-8")

            # Write header
            file.write("title,artist,album\n")

            # Write tracks
            for track in playlist['tracks']:
                if track['source'] == '2':
                    trackinfo = track['track']
                    if FORMAT == "TYPE2":
                        file.write(oldifyField(trackinfo['artist']) + ',' + oldifyField(trackinfo['album']) + ',' + oldifyField(trackinfo['title']) + ",\n")
                    elif FORMAT == "TYPE3":
                        file.write("\"" + trackinfo['artist'] + '\",\"' + trackinfo['album'] + '\",\"' + trackinfo['title'] + "\",\n")
                    else:
                        file.write("\"" + trackinfo['title'] + '\",\"' + trackinfo['artist'] + '\",\"' + trackinfo['album'] + "\"\n")
                else:
                    match = False
                    for libtrack in library:
                        if libtrack['id'] == track['trackId']:
                            if FORMAT == "TYPE2":
                                file.write(oldifyField(libtrack['artist']) + ',' + oldifyField(libtrack['album']) + ',' + oldifyField(libtrack['title']) + ",\n")
                            elif FORMAT == "TYPE3":
                                file.write("\"" + libtrack['artist'] + '\",\"' + libtrack['album'] + '\",\"' + libtrack['title'] + "\",\n")
                            else:
                                file.write("\"" + libtrack['title'] + '\",\"' + libtrack['artist'] + '\",\"' + libtrack['album'] + "\"\n")
                            match = True

                    if not match:
                        file.write(track['trackId'] + "\n")

            file.close()
            print("Exported \"" + newfilename + "\"")
        print("Done!")
    except IOError:
        print("Error creating file: \"" + newfilename + "\"")
        print("Closing program")
        quit()

def cleanName(name):
    return re.sub('[/\\:*?"<>|]', '', name).encode('ascii', 'ignore').decode("utf-8")
    # translation_table = dict.fromkeys(map(ord, '!@#$'), None)
    # return name.translate(translation_table)

def oldifyField(field):
    if ',' in field:
        return ('\"' + field.__str__() + '\"')
    else:
        return field

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
