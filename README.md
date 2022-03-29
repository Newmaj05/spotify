# spotify
Description
The idea behind this script was to add songs that hadn't been added to a Shazam-Spotify linked playlist and add them in to have the complete list of songs that I had Shazam'd prior to linking the apps. 

# Required
- Python 3.x
- pandas
- spotipy.oauth2

# Instructions

Prior to running the script, the songs were downloaded from the Shazam account in csv format. However any list of files can be used as long as the column names in this source file are "Title" and "Artist". The other option would be to change these values in the scipt.
The script uses a cred.py file for client specific details which are required to source before running the script. This should be created in the same directory. 

