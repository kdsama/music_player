from utils import song as SongFunction
from db.song import CheckOrInsertSong
import utils.song
import pygame 

pygame.mixer.init()
# For now we will use this as a service layer. 
# service layer is the one that usually interacts to the api/gui or CLI . 
# we will fetch the information about the song once it has been selected from the music player. 
# the path can be anyone. 


class SongService:
    def __init__(self, path):
        # make sure the path is an absolute path, and not a relative path
        metadata = SongFunction.metaData(path)        
        self.title = metadata["title"]
        self.album = metadata["album"]
        self.artist = metadata["artist"]
        self.duration = metadata["duration"]
        self.location = path
        self.paused = False 
        # self.initialize =      
        


    
    def play(self): 
        # You may need to add more values to the constructor to run this. 
        # SongFunction.play(self.location)
        utils.song.play(self.location)
        
     
    def wait(self,n):
        # This is a testing function 
        print("are we here ???")
        SongFunction.wait(n)

    def pause(self):
        # pause the song
        print("now we need to pause the song ")
        SongFunction.pause()
        self.pause = True 
    
    def resume(self):
        # resume the song 
        SongFunction.resume()
        self.pause = False 

    def go_back(self, n):
        # go back n seconds in the song
        SongFunction.fast_backward(n)
        
    
    def go_front(self, n):
        # go forward n seconds in the song
        SongFunction.fast_backward(n)
    

