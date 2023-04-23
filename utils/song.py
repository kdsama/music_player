from mutagen.mp3 import MP3
import pygame
import json

#Used for fast-forward and back-off
change_time = 0

#Sleep time
sleep_time = 0

#sleep time switch: 0 is off, 1 is on
sleep_time_switch = 0

metadata = {}

def metaData(song_path):
    audio = MP3(song_path)
    global metadata
    ps = song_path.split("/")
    potential_song_item = ps[len(ps)-1]
    potential_song_name = potential_song_item
    metadata['title'] = audio['TIT2'].text[0] if 'TIT2' in audio else potential_song_name.split(".")[0]
    metadata['artist'] = audio['TPE1'].text[0] if 'TPE1' in audio else ''
    metadata['album'] = audio['TALB'].text[0] if 'TALB' in audio else ''
    metadata['duration'] = audio.info.length
    metadata["path"] = song_path
    return metadata


def get_song_position():
    
    pos = pygame.mixer.music.get_pos() / 1000
    return pos


def setVolume(volume):
    pygame.mixer.music.set_volume(volume)

def increase_and_return_new_volume(from_volume,diff):
    from_volume = min(from_volume+ diff,1.0)
    setVolume(from_volume)
    return from_volume

def decrease_and_return_new_volume(from_volume,diff):
    from_volume = max(from_volume- diff,0.0)
    setVolume(from_volume)
    return from_volume


def load(song_path):
    audio = MP3(song_path)
    pygame.mixer.music.load(song_path)
    return audio

def play(song_path):
    # pygame.mixer.init()
    load(song_path)
    print("Song path loaded now is ",song_path)
    save_current_music(song_path)  
    pygame.mixer.music.play()
    #The audio will not play without the wait below 

    # wait(int(audio.info.length * 1000))


def wait(n):
    # wait for n seconds before doing anything 
    pygame.time.wait(n*1000)

def stop():
    pygame.mixer.music.stop()

def waitAndKill(n):
    #wait for n seconds and stop the song , or whatever song that is being played. 
    wait(n)
    pygame.mixer.music.stop()

def the_song_is_playing():
    return pygame.mixer.music.get_busy()

def pause():
    pygame.mixer.music.pause()

def resume():
    pygame.mixer.music.unpause()

def fast_forward(current_time=0):

    
    new_time = pygame.mixer.music.get_pos()/1000 +  current_time 
    pygame.mixer.music.set_pos(new_time)
    

def wait_for_music_to_end():
        while pygame.mixer.music.get_busy():
            pygame.event.pump()
            pygame.time.wait(10)   


    


def speed_up(rate):
    pygame.mixer.music.set_rate(rate * pygame.mixer.music.get_rate())

#Get the index of the song
def get_music_index(song_name):
    global metadata
    for i in range(0, len(metadata)):
        if metadata[i] == song_name:
            return i
    else:
        return 0

# Previous Song
def previous_music(current_music_name):
    stop()
    previous_music_index = (get_music_index(current_music_name) - 1) % len(metadata)
    previous_music = metadata['title'][previous_music_index]
    pygame.mixer.music.play(previous_music)


# Next Song
def next_music(current_music_name):
    stop()
    previous_music_index = (get_music_index(current_music_name) + 1) % len(metadata)
    previous_music = metadata['title'][previous_music_index]
    pygame.mixer.music.play(previous_music)

# quit
def quit():
    stop()
    pygame.quit()
    exit()

# Sleep timer
def set_sleep_time(seconds):
    global sleep_time
    global sleep_time_switch
    sleep_time = sleep_time + seconds
    sleep_time_switch = 1

# check the sleep time
def check_sleep_time():
    global sleep_time
    if (sleep_time > 0):
        sleep_time = sleep_time - 1
    if (sleep_time <= 0 and sleep_time_switch == 1):
        quit()

# Saves the name of the current music
def save_current_music(current_music):
    music_name = {"current_music": current_music}
    with open("./current_music.json", "w") as f:
        json.dump(music_name, f)


# Show the last song playedwhen you left
def get_last_music():
    with open("./current_music.json", "r", encoding="utf-8") as f:
        content = json.load(f)
        last_music_name = content["current_music"]
        play(last_music_name)

# Display the album image
def display_image(current_music_name):
    global metadata
    current_music_index = get_music_index(current_music_name)
    current_music_image = metadata['album'][current_music_index]
    image = pygame.image.load(current_music_image)
    # Set the new width and height
    new_width = 100
    new_height = 100
    # Scale the image
    resized_image = pygame.transform.scale(image, (new_width, new_height))
    return resized_image

# Advanced search (not only by the song name or artist but also by mood,genre,remixes, etc.)
def search(query):
    global metadata
    matching_items = []

    for title in metadata['title']:
        if query.lower() in title.lower():
            matching_items.append(title)

    for artist in metadata['artist']:
        if query.lower() in artist.lower():
            matching_items.append(artist)

    for mood in metadata['mood']:
        if query.lower() in mood.lower():
            matching_items.append(mood)

    for genre in metadata['genre']:
        if query.lower() in genre.lower():
            matching_items.append(genre)

    for remixes in metadata['remixes']:
        if query.lower() in remixes.lower():
            matching_items.append(remixes)

    return set(matching_items)

# Update the query results displayed by the UI
def on_search_text_changed(text):
    results = search(text)
    # list_widget.clear()
    # list_widget.addItems(results)