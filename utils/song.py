from mutagen.mp3 import MP3
import pygame
import json




def metaData(song_path):
    audio = MP3(song_path)
    metadata = {}
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
    
    load(song_path)
    pygame.mixer.music.play()

def is_song_finished():
    global song_finished 
    return song_finished

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
    


# quit
def quit():
    stop()
    pygame.quit()
    exit()
