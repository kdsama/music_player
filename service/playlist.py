from service.song import SongService
from utils import song as SongFunction
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
        print(song)
        pos = -1 
        for i in range(0,len(self.songs)):
            if self.songs[i] == song :
                pos = i
        if pos != -1 :
            del self.songs[i]
            self.songs.append(song)
        else:
            # Added to playlist. 
            self.songs.append(song)
        if len(self.songs) == 1 :
            self.songServiceObject = SongService(self.songs[0])


    def showCurrentPlaylist(self):
        # This is incorrect . Here We have to fetch the names of the songs and just dislpay them , alongside how much time 
        # What is returned is a array of object . each Object is {"name":"NameOfTheSong","duration":"12:30"}

        return self.songs
        
        
    def play(self,index=-1):
        if index != -1 :
            self.songServiceObject = SongService(self.songs[index])
        for song in self.songs : 
            self.songServiceObject = SongService(song)            
            self.songServiceObject.play()

    def next(self):
        self.current_song_index +=1 
        
        if self.current_song_index >= len(self.songs):
            if self.loop:
                self.current_song_index = 0                
            else :   
                self.songServiceObject.stop()
                return 
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
            else :   
                self.songServiceObject.stop()
        # else :         
        
    #  To toggle loop button . 
    def toggleLoop(self):
        self.loop = not self.loop     

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
