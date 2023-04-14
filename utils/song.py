from mutagen.mp3 import MP3
import pygame

#Used for fast-forward and back-off
change_time = 0

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


    

def load(song_path):
    audio = MP3(song_path)
    pygame.mixer.music.load(song_path)
    return audio

def play(song_path):
    # pygame.mixer.init()
    audio = load(song_path)    
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
    pygame.time.wait(n*1000)
    pygame.mixer.music.stop()

def the_song_is_playing():
    return pygame.mixer.music.get_busy()

def pause():
    pygame.mixer.music.pause()

def resume():
    pygame.mixer.music.unpause()

def fast_forward(seconds):
    global change_time
    change_time += seconds
    current_time = pygame.mixer.music.get_pos() / 1000
    new_time = current_time + change_time
    pygame.mixer.music.set_pos(new_time * 1000)

def wait_for_music_to_end():
        while pygame.mixer.music.get_busy():
            pygame.event.pump()
            
            pygame.time.wait(10)   

def back_off(seconds):
    global change_time
    change_time -= seconds
    current_time = pygame.mixer.music.get_pos() / 1000
    new_time = current_time + change_time
    if new_time < 0:
        new_time = 0
    pygame.mixer.music.set_pos(new_time * 1000)
    


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