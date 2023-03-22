from mutagen.mp3 import MP3
import pygame




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

def waitAndKill(n):
    #wait for n seconds and stop the song , or whatever song that is being played. 
    pygame.time.wait(n*1000)
    pygame.mixer.music.stop()

def pause():
    pygame.mixer.music.pause()

def resume():
    pygame.mixer.music.unpause()

def fast_forward(seconds):
    current_time = pygame.mixer.music.get_pos() / 1000
    new_time = current_time + seconds
    pygame.mixer.music.set_pos(new_time * 1000)

def wait_for_music_to_end():
        while pygame.mixer.music.get_busy():
            pygame.event.pump()
            
            pygame.time.wait(10)   

def fast_backward(seconds):
    current_position = pygame.mixer.music.get_pos() // 1000
    new_position = current_position - seconds
    if new_position < 0:
        new_position = 0
    pygame.mixer.music.set_pos(new_position)
    


def speed_up(rate):
    pygame.mixer.music.set_rate(rate * pygame.mixer.music.get_rate())


