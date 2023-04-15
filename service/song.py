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
        self.metadata = SongFunction.metaData(path)        
        self.title = self.metadata["title"]
        self.album = self.metadata["album"]
        self.artist = self.metadata["artist"]
        self.duration = self.metadata["duration"]
        self.path = path
        self.pauseSong = False 
        # self.initialize =      
        


    
    def play(self): 
        # You may need to add more values to the constructor to run this. 
        # SongFunction.play(self.path)
        utils.song.play(self.path)
        try :

            CheckOrInsertSong(self.metadata)
        except Exception as e : 
            print(e)
        
        
     
    def wait(self,n):
        # This is a testing function 
        
        SongFunction.wait(n)

    def pause(self):
        # pause the song
        SongFunction.pause()
        self.pauseSong = True 
    
    def resume(self):
        # resume the song 
        SongFunction.resume()
        self.pauseSong = False 

    def go_back(self, n):
        # go back n seconds in the song
        SongFunction.fast_forward(-n)
        
    def stop(self):
        SongFunction.stop()
    
    def go_front(self, n):
        # go forward n seconds in the song
        SongFunction.fast_forward(n)
    
    def get_song_position(self):
        return SongFunction.get_song_position()
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
