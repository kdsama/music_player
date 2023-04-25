from service.song import SongService
from db.song import get_last_played_song
from service.playlist_abc import PlaylistServiceABC




class PlaylistService(PlaylistServiceABC):
    def __init__(self, songs):
        self.current_song_index = 0 
        # songs =  list of absolute paths, not relative paths 
        self.songs = songs 
        self.loop = False 
        self.songServiceObject  = None
        
    
    def addToPlaylist(self,song):
        # If song is already present, remove it from the playlist and queue it.
        pos = -1 
        for i in range(0,len(self.songs)):
            if self.songs[i] == song :
                pos = i
        if pos != -1 :
            del self.songs[pos]
            self.songs.append(song)
        else:
            # Added to playlist. 
            self.songs.append(song)
        
        if len(self.songs) == 1 :
            self.songServiceObject = SongService(self.songs[0])

    def play_song_by_pathurl(self,path_url):
        for index in range(0,len(self.songs)) :
            if self.songs[index] == path_url :
                self.songServiceObject = SongService(self.songs[index])
                song_id = self.songServiceObject.play()    

    def play_song_by_name(self,name):
       path = SongService.get_song_path_by_name(name)

       for index in range(0,len(self.songs)) :
           if path == self.songs[index]:
                self.songServiceObject = SongService(self.songs[index])
                song_id = self.songServiceObject.play()   
               
               
            
    def showCurrentPlaylist(self):
        # This is incorrect . Here We have to fetch the names of the songs and just dislpay them , alongside how much time 
        # What is returned is a array of object . each Object is {"name":"NameOfTheSong","duration":"12:30"}

        return self.songs
        
    def get_playlist_length(self):
        return len(self.songs)
    
    def play(self,index=-2):
        
        if index != -2 :

            self.songServiceObject = SongService(self.songs[index])
            song_id = self.songServiceObject.play()     
        else:
            self.songServiceObject = SongService(self.songs[0])
            song_id = self.songServiceObject.play()     

    def next(self):
        
        self.current_song_index +=1 
        
        if self.current_song_index >= len(self.songs):
            if self.loop:
                self.current_song_index = 0                
            else :   
                self.current_song_index = len(self.songs) -1 
                # self.songServiceObject.stop()
                
                
                   
        self.play(self.current_song_index)
 
    def emptyCurrentPlaylist(self):
        self.songs = []
        return 
 
    def previous(self):
        
        self.current_song_index -=1 
        
        #If index goes above 
        if self.current_song_index < 0:
            if self.loop:
                self.current_song_index = len(self.songs) - 1
                self.play(self.current_song_index)
            else :   
                self.current_song_index = 0 
                # self.play(self.current_song_index)
                # self.songServiceObject.stop()
                # raise  Exception("set slider to 0 ")
                # return


        self.play(self.current_song_index)

        # else :         
        
    #  To toggle loop button . 
    def toggleLoop(self):
        self.loop = not self.loop  
        
        
    def the_song_is_playing(self):
        return SongService.the_song_is_playing()
    
    def last_played_song(self):
        song =  get_last_played_song()
        if song is None : 
            return ""
        return song["path"]
