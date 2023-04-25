from abc import ABC, abstractmethod

class SongServiceBase(ABC):
    @abstractmethod
    def __init__(self, path):
        pass
    
    @abstractmethod
    def play(self):
        pass
    
    @abstractmethod
    def wait(self, n):
        pass
    
    @abstractmethod
    def pause(self):
        pass
    
    @abstractmethod
    def resume(self):
        pass
    
    @abstractmethod
    def go_back(self, n):
        pass
    
    @abstractmethod
    def stop(self):
        pass
    
    @abstractmethod
    def go_front(self, n):
        pass
    
    @abstractmethod
    def get_song_position(self):
        pass
    @abstractmethod
    def move_song_to_position(self,position):
        pass
    @staticmethod
    @abstractmethod
    def increase_and_return_new_volume(from_vol, diff):
        pass
    
    @staticmethod
    @abstractmethod
    def decrease_and_return_new_volume(from_vol, diff):
        pass
    
    @staticmethod
    @abstractmethod
    def get_songs_from_names(names): 
        pass
    
    @staticmethod    
    @abstractmethod
    def get_song_path_by_name(title):
        pass
        
     
    @staticmethod
    @abstractmethod
    def the_song_is_playing(self):
        pass
    
    