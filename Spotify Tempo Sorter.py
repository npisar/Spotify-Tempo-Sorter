##################################################
# This program will NOT WORK without your own client ID and client secret!
# Please reference the readme and this video. https://www.youtube.com/watch?v=MBo_uSkI2pM
# You need to install Spotipy, as well as pass the client id and client secret
##################################################

# Copy-pasted from the readme
# In short, this program is made up of three main functions.
# The first function searches with a query on Spotify, returning some specified number of results
    # Each result is stored in a dictionary, where the key is the song name, and the value is a list of dictionaries
        # Since I'm using dictionaries, duplicate song names were an issue. I had to add a function that adds "-Duplicate"
        # to the end if encounters a duplicate result. And then I ran that function call 5 times or so to account for
        # a LOT of duplicates.
    # The list of dictionaries contains the tempo of the song in Beats Per Minute (BPM) as well as the track's ID
    # Basically, it returns a huge dictionary with the song title and relevant tempo and ID information about it

# The second function takes a range of tempos and chooses a specified random number of those results from the first function
    # It uses the random module to choose randomly
    # If the user asks for more songs than are in the list of results, or if there aren't enough songs in the
        # desired tempo range, then the program can handle that
    # When checking if the song is in the tempo range, it takes the listed tempo as well as the doubled tempo.
        # This is because you can feel songs in double time or halftime. Tempo isn't necessarily always felt the same way
        # for every song
    # This returns another dictionary with the specified random number of songs

# The third and final function outputs the Spotify URLs of the songs.
    # These are formatted differently than the IDs. So I couldn't just print the IDs
    # This is a pretty short function that stores each URL in a list, and prints each item of the list
    # Then, you can copy the links from the terminal, and paste into a Spotify playlist on the desktop app!
###

#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
  #####                                     
 #     # #####   ####  ##### # ###### #   # 
 #       #    # #    #   #   # #       # #  
  #####  #    # #    #   #   # #####    #   
       # #####  #    #   #   # #        #   
 #     # #      #    #   #   # #        #   
  #####  #       ####    #   # #        #   
                                            
 #######                                    
    #    ###### #    # #####   ####         
    #    #      ##  ## #    # #    #        
    #    #####  # ## # #    # #    #        
    #    #      #    # #####  #    #        
    #    #      #    # #      #    #        
    #    ###### #    # #       ####         
                                            
  #####                                     
 #     #  ####  #####  ##### ###### #####   
 #       #    # #    #   #   #      #    #  
  #####  #    # #    #   #   #####  #    #  
       # #    # #####    #   #      #####   
 #     # #    # #   #    #   #      #   #   
  #####   ####  #    #   #   ###### #    #
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

# Once you've passed the client and secret ID's, as well as the user ID, just press run!

#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||







# import all the necessary modules
from __future__ import print_function    # (at top of module)
from spotipy.oauth2 import SpotifyClientCredentials
import json
import spotipy
import random

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace = False
############################################################################################

# functions to process data
def duplicate_name_checker(input_dictionary, iterator):
    if iterator['name'] in input_dictionary:
        iterator['name'] += "-Duplicate"
def song_features_processor(features_json_string, delimiters_list):
    for delimiter in delimiters_list:
        features_json_string = " ".join(features_json_string.split(delimiter))
    
    return features_json_string.split()
def feature_numeric_value(processed_features, feature_name):
    feature_value_index = (processed_features.index(feature_name)) + 1
    return float(processed_features[feature_value_index])

# functions that actually get the songs and information about the
def track_and_tempo_dict(query, number_of_songs):
    # search code taken from the Spotipy GitHub example
    tids = []
    songs_dictionary = {}
    search_results = sp.search(q = query, limit = number_of_songs)
    
    for i, t in enumerate(search_results['tracks']['items']):
        print(' ', i+1, t['name'])
        for i in range(number_of_songs+1):
            # check for duplicate names so the counting doesn't get messed up
            duplicate_name_checker(songs_dictionary, t)
        songs_dictionary[t['name']] = ""
        tids.append(t['uri'])
    list_songs_dictionary = list(songs_dictionary)
    
    # store the features of all the songs and process them
    features = sp.audio_features(tids)
    tid_and_song_count = 0
    for feature in features:
        song_features = json.dumps(feature, indent=4)
        split_json_string = song_features_processor(song_features, [":", ","])
        
        song_info = []
        
        # process the song tempo to append
        song_tempo = {}
        tempo = feature_numeric_value(split_json_string, '"tempo"')
        song_tempo["Tempo (BPM)"] = tempo
        song_info.append(song_tempo)

        # process the song ID to append
        song_id = {}
        song_id["ID"] = tids[tid_and_song_count]
        song_info.append(song_id)

        songs_dictionary[list_songs_dictionary[tid_and_song_count]] = song_info
        tid_and_song_count += 1

    # printing and formatting
    print(f"\n\nTop {number_of_songs} results for the query {query} are:\n----------\n")
    print_count = 1
    for song, information in (songs_dictionary).items():
        print(f"{print_count}. {song}: {information}\n")
        print_count += 1
    print(f"----------\n")
    
    # return the dictionary so data can be used
    return songs_dictionary
def get_random_songs_in_range(track_dictionary, number_of_songs, min_tempo, max_tempo):
    songs_in_range = {}
    track_counter = 1

    for track, information in track_dictionary.items():
        # compare tempo to tempo range
        if float(min_tempo) < information[0]["Tempo (BPM)"] < float(max_tempo):
            songs_in_range[track] = information
        # also compare the doubled value to the range since both work. You can feel the doubled valule in halftime.
        if float(min_tempo) < (information[0]["Tempo (BPM)"]) * 2 < float(max_tempo):
            songs_in_range[track] = information
    
    # handle if the desired number is larger than the amount of songs
    if number_of_songs > len(songs_in_range):
        number_of_songs = len(songs_in_range)
        print(f"\nIt looks like the number of results in that tempo range is less than the desired number of songs. Try running the program again with a larger search size!")

    # create a list to append information to using the random function --> needs to be a list
    list_songs_in_range = []
    for song, information in songs_in_range.items():
        list_songs_in_range.append(information)
    
    # use random.sample to get X random items
    random_songs_in_range_list = random.sample(list_songs_in_range, number_of_songs)

    # put the items back in a dictionary so we can have the title along with the track information
    random_songs_in_range = {}
    for random_song_data in random_songs_in_range_list:
        for song, info in songs_in_range.items():
            # if the ID's are the same between the randomly sampled list of features and the original dict, then add it to the dict 
            if random_song_data[1]['ID'] == info[1]['ID']:
                random_songs_in_range[song] = random_song_data

    # printing and formatting stuff so it looks nice for the user
    print(f"\n\nThe {number_of_songs} random songs picked from the given range are:\n----------\n")
    print_counter = 1
    for song, information in (random_songs_in_range).items():
        print(f"{print_counter}. {song}: {information}\n")
        print_counter += 1
    print(f"----------\n")
    # still return the dictionary so data can be used
    return random_songs_in_range
def output_song_urls(dict_of_songs):
    # create a list to store URLs
    url_list = []
    # iterate through dict of songs from the last step
    for song, info in dict_of_songs.items():
        # store the URI in a variable for ease of access, then split the URI into only the ID 
        uri = info[1]['ID']
        id = uri[14:]
        # format into a link with an fstring
        song_link = f"https://open.spotify.com/track/{id}"
        # append to the list of URLs
        url_list.append(song_link)
    
    # print each URl from the list
    for url in url_list:
        print(url)

# functions that check user input
def int_input_checker(input_message):
    while True:
        string_input = input(input_message)
        try:
            int_input = int(string_input)
            break
        except:
            print(f"Please enter an integer number of results!")
    return int_input
def bpm_float_input_checker(input_message):
    while True:
        string_input = input(input_message)
        try:
            float_input = float(string_input)
            break
        except:
            print(f"Please enter a float bpm value!")
    return float_input

############################################################################################
# print / user input block for first function
print(f"\n\n\nEnter an artist name, and track_and_tempo_dict will return a dictionary with the song name, URI, and tempo in BPM.\n----------------------------------------\n")
track_tempo_dict_query = input("What's your search query? Input an artist or song name: ")
input_number_of_songs = int_input_checker("How many results would you like? Please enter an integer: ")
track_tempo_dict = track_and_tempo_dict(track_tempo_dict_query, input_number_of_songs)

# print / user input block for second function
print(f"Now, get_random_songs_in_range will randomly return a dictionary of songs within an inputted tempo range.\n----------------------------------------\n")
number_random_songs = int_input_checker("How many songs do you want to be randomly selected? ")
min_tempo_input = bpm_float_input_checker("What's the lowest BPM you want? ")
max_tempo_input = bpm_float_input_checker("What's the highest BPM you want? ")
random_songs_in_range = get_random_songs_in_range(track_tempo_dict, number_random_songs, min_tempo_input, max_tempo_input)

# print / user input block for last function
print(f"Finally, output_song_urls will take the songs from that random dictionary and print out their URLs to copy and paste into the Spotify App.\n----------------------------------------\n")
output_song_urls(random_songs_in_range)
print(f"\n----------------------------------------\nNow, copy those URLs, create a new playlist, and press Ctrl+V to paste them in. Happy drumming!")