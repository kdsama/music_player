from service.song import SongService
from db.song import get_last_played_song




class PlaylistService:
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
        print(self.songs)
        if len(self.songs) == 1 :
            self.songServiceObject = SongService(self.songs[0])

    def play_song_by_pathurl(self,path_url):
        for index in range(0,len(self.songs)) :
            if self.songs[index] == path_url :
                self.songServiceObject = SongService(self.songs[index])
                song_id = self.songServiceObject.play()     

    def play_song_by_pathurl(self,path_url):
        for index in range(0,len(self.songs)) :
            if self.songs[index] == path_url :
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
            return 
        
        for song in self.songs :             
            self.songServiceObject = SongService(song)            
            song_id = self.songServiceObject.play()

    def next(self):
        
        self.current_song_index +=1 
        
        if self.current_song_index >= len(self.songs):
            if self.loop:
                self.current_song_index = 0                
            else :   
                self.current_song_index = len(self.songs) -1 
                self.songServiceObject.stop()
                return 
                   
        self.play(self.current_song_index)
 
    def emptyCurrentPlaylist(self):
        self.songs = []
        return 
 
    def previous(self):
        
        self.current_song_index -=1 
        print(self.current_song_index,self.songs)
        #If index goes above 
        if self.current_song_index < 0:
            if self.loop:
                self.current_song_index = len(self.songs) - 1
                self.play(self.current_song_index)
            else :   
                self.current_song_index = 0 
                self.songServiceObject.stop()
                return


        self.play(self.current_song_index)

        # else :         
        
    #  To toggle loop button . 
    def toggleLoop(self):
        self.loop = not self.loop  
        print("Value of loop is ",self.loop)
        print(self.loop)   

    def last_played_song(self):
        song =  get_last_played_song()
        if song is None : 
            return ""
        return song["path"]
        

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
            # pygame.time.wait(10)
