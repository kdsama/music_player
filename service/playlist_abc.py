
from abc import ABC, abstractmethod

class PlaylistServiceABC(ABC):
    @abstractmethod
    def addToPlaylist(self, song):
        pass
    
    @abstractmethod
    def play_song_by_pathurl(self, path_url):
        pass
    
    @abstractmethod
    def showCurrentPlaylist(self):
        pass
    
    @abstractmethod
    def get_playlist_length(self):
        pass
    
    @abstractmethod
    def play(self, index=-2):
        pass
    
    @abstractmethod
    def next(self):
        pass
    
    @abstractmethod
    def emptyCurrentPlaylist(self):
        pass
    
    @abstractmethod
    def previous(self):
        pass
    
    @abstractmethod
    def toggleLoop(self):
        pass
    
    @abstractmethod
    def last_played_song(self):
        pass