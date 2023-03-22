from mutagen.mp3 import MP3
import pygame

def load_file(file_path):
    audio = MP3(file_path)
    pygame.mixer.music.load(file_path)
    return audio

def play():
    pygame.mixer.music.play()

def pause():
    pygame.mixer.music.pause()

def resume():
    pygame.mixer.music.unpause()



def playStuff():
    pygame.mixer.init()
    audio = load_file("/home/kshitij/Desktop/music_player/test_music/Westlife - Nothing's Gonna Change My Love For You.mp3")
    
    play()
    pause()
    resume()

    pygame.time.wait(int(audio.info.length * 1000))

playStuff()
