import pygame
import json
import sqlite3
import os
from mutagen.mp3 import MP3
from time import sleep


class Song:
    def __init__(self, id, name, album_id, created_at, location, album):
        self.id = id
        self.name = name
        self.album_id = album_id
        self.created_at = created_at
        self.location = location
        self.album = album
    
    def play(self):
        # The object of the song will already would have been initiated . 
        # This function will play the song. Its better if it calls a service which plays the song. 
        # You may need to add more values to the constructor to run this. 
        pass
    
    def load(self):
        # Happens before playing it
        pygame.init()
        pass
    
    def pause(self):
        # pause the song
        pass
    
    def go_back(self, n):
        # go back n seconds in the song
        pass
    
    def go_front(self, n): 
        # go forward n seconds in the song
        pass
