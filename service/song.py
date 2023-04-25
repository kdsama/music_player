from utils import song as SongFunction
from db.song import CheckOrInsertSong,get_all_songs
import pygame 

pygame.mixer.init()
# For now we will use this as a service layer. 
# service layer is the one that usually interacts to the api/gui or CLI . 
# we will fetch the information about the song once it has been selected from the music player. 
# the path can be anyone. 
path_name_metadata = {}
song_name_metadata= {}

def set_existing_song_metadata():
        global path_name_metadata
        songs_list = get_all_songs()
        
        for songs in songs_list:
            
            path_name_metadata[songs["path"]] = songs 
            song_name_metadata[songs["title"]] = songs 
        print(songs_list)

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
        set_existing_song_metadata()
        

    


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
            song_name_metadata[self.title] = self.metadata
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
    @staticmethod    
    def get_song_path_by_name(title):
        global song_name_metadata
        
        
        return song_name_metadata[title]["path"]
         
