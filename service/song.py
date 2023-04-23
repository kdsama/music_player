from utils import song as SongFunction
from db.song import CheckOrInsertSong,get_all_songs
from db.song import CheckOrInsertSong,get_all_songs
import utils.song
import pygame 

pygame.mixer.init()
# For now we will use this as a service layer. 
# service layer is the one that usually interacts to the api/gui or CLI . 
# we will fetch the information about the song once it has been selected from the music player. 
# the path can be anyone. 
path_name_metadata = {}
path_name_metadata = {}

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
        self.current_time = 0 
        # self.initialize =     
        self.set_existing_song_metadata()
         
        

    
    def set_existing_song_metadata(self):
        songs_list = get_all_songs()
        for songs in songs_list:
            path_name_metadata[songs.path] = songs 
        

    @staticmethod
    def get_song_names_from_pathurls(paths): 
        name_list = []
        for path in paths : 
            try :

                name_list.append(SongService.get_song_names_from_pathurl(path))
            except Exception as e : 
                name_list.append("Name Not Found")
        return name_list

    @staticmethod
    def get_song_names_from_pathurl(path):
        name = "Name Not Found"
        try :
            name = path_name_metadata[path]["title"]
            
        except Exception as e : 
            name =  SongFunction.metaData(path)["title"]

        return name 

    
    def set_existing_song_metadata(self):
        songs_list = get_all_songs()
        for songs in songs_list:
            path_name_metadata[songs.path] = songs 
        

    @staticmethod
    def get_song_names_from_pathurls(paths): 
        name_list = []
        for path in paths : 
            try :

                name_list.append(SongService.get_song_names_from_pathurl(path))
            except Exception as e : 
                name_list.append("Name Not Found")
        return name_list

    @staticmethod
    def get_song_names_from_pathurl(path):
        name = "Name Not Found"
        try :
            name = path_name_metadata[path]["title"]
            
        except Exception as e : 
            name =  SongFunction.metaData(path)["title"]

        return name 

    def play(self): 
        # You may need to add more values to the constructor to run this. 
        # SongFunction.play(self.path)
        SongFunction.play(self.path)
        try :

            song_id = CheckOrInsertSong(self.metadata)
            path_name_metadata[self.path] = self.metadata
            path_name_metadata[self.path] = self.metadata
            return song_id 
        except Exception as e : 
            print(e)
            return -1 
        
        
     
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
        self.current_time -= n 
        SongFunction.fast_forward(self.current_time)
        
    def stop(self):
        SongFunction.stop()
    
    def go_front(self, n):
        # go forward n seconds in the song
        self.current_time += n 
        SongFunction.fast_forward(self.current_time)
    
    def get_song_position(self):
        return SongFunction.get_song_position()
    @staticmethod
    def increase_and_return_new_volume(from_vol,diff):
        return SongFunction.increase_and_return_new_volume(from_vol,diff)
    @staticmethod
    def decrease_and_return_new_volume(from_vol,diff):
        return SongFunction.decrease_and_return_new_volume(from_vol,diff)

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