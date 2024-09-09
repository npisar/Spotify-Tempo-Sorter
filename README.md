# Spotify-Tempo-Sorter
A simple Python script written using Spotipy to find the bpm of songs based on a search query. I made this for my final project in my intro Python class during my second semester of college so I could find songs at a specific BPM to drum to. It's been extremely useful for me and might be for you too!


# Setup
For the program to work, you'll need 2 values that you should paste into commands.txt.

First and foremost, however, you will need to install the Spotipy Python library.
Find instructions for that [here](https://spotipy.readthedocs.io/en/2.24.0/#installation)

# Obtaining the Client ID and Client Secret
You'll need to create an app on the Spotify developer site for the Client ID and Client Secret. These values are tied to a dev application and are used to make the library actually work.
Go to [the developer site](https://developer.spotify.com/) and log in with your Spotify account.

Once you log in, go to your [dashboard](https://developer.spotify.com/dashboard) and create an app.

<img width="1512" alt="Create Spotify App" src="https://github.com/user-attachments/assets/3f5dad1a-c2c3-4593-bea3-dd6251f8b0d7">

Once you choose a name and description, copy and paste the Client ID and Client Secret into commands.txt.

# Using the program
With that, you're ready to go! Open the file, and make sure to pass the Client ID, Client Secret, and Redirect URL (already provided in the commands file).
Please click on the video below for a quick demonstration of how to use the script!
[![YouTube video showing how to use script](https://img.youtube.com/vi/MBo_uSkI2pM/0.jpg)](https://www.youtube.com/watch?v=MBo_uSkI2pM)

The program should walk you through everything you need to do. You'll enter a search query (artists or album names work the best), and it will print out a list of every song (if you see "-duplicate", it found something with the same name) with relevant information. Then, you'll be prompted for the range of tempi as well as how many songs you'd like back. It will randomly pick the inputted number of results. If there are less results that fall within that range, it will give you as many as it can.

Please note that the program can typically only handle about 50 results. If someone wants to edit my code and make the number of possible results larger, please do!

# Adding the songs to a playlist
Once you get the links, copy them. Create a new playlist on Spotify, then click on the main area and press Ctrl+V to paste them in. You should have a playlist with the given songs in there!
