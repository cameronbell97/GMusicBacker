# GMusicBacker
Google Play Music playlist backup tool
Created by Cameron Bell
Using gmusicapi by Simon Weber

A program for exporting your playlists on Google Play Music as .csv files for backup records. You must have a Google Play Music Unlimited account for this to work.

Only use this program on trusted computers, as your login details are stored as plaintext.
If you have two-factor-authentication enabled on your Google account, you will need to create an app password for your account and use that to log in.
This program uses an unreliable way of determining the DeviceID used to query the Google Play Music service.
As such, once attempting to log in, the login will likely fail in which case you must visit https://accounts.google.com/b/0/DisplayUnlockCaptcha to allow login for 10 to 20 minutes.

This program requires Python3 and gmusicapi to be installed to run properly.
