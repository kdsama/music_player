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
        self.wait(int(self.duration))
        
     
    def wait(self,n):
        # This is a testing function 
        
        SongFunction.wait(n)

    def pause(self):
        # pause the song
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
    

# class MusicPlayer:
#     def __init__(self, music_files):
#         pygame.init()
#         pygame.mixer.init()
#         self.music_files = music_files
#         self.current_song_index = 0
#         self.paused = False
#         self.fast_forwarding = False
#         self.rewinding = False

#     def play_music(self):
#         # Load and play the current song
#         pygame.mixer.music.load(self.music_files[self.current_song_index])
#         pygame.mixer.music.play()

#     def play_next_song(self):
#         # Increment the current song index
#         self.current_song_index += 1

#         # Check if we have reached the end of the playlist
#         if self.current_song_index >= len(self.music_files):
#             self.current_song_index = 0

#         # Stop the current song
#         pygame.mixer.music.stop()

#         # Load and play the next song
#         pygame.mixer.music.load(self.music_files[self.current_song_index])
#         pygame.mixer.music.play()

#     # ... other methods ...

#     def wait_for_music_to_end(self):
#         # Wait for the rest of the music to play
#         while pygame.mixer.music.get_busy():
#             pygame.event.pump()
#             if self.paused:
#                 pygame.mixer.music.pause()
#             elif self.fast_forwarding:
#                 self.fast_forwarding = False
#             elif self.rewinding:
#                 self.rewinding = False
#             else:
#                 pygame.mixer.music.unpause()
#             pygame.time.wait(10)

#     def __del__(self):
#         # Quit Pygame
#         pygame.quit()
