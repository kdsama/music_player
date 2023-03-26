from service.song import SongService




class PlaylistService:
    def __init__(self, songs):
        self.current_song_index = 0 
        # songs =  list of absolute paths, not relative paths 
        self.songs = songs 
        self.loop = False 
        self.songServiceObject  = None
    
    def play(self):
        for song in self.songs : 
            self.songServiceObject = SongService(song)
            song.play()

    def next(self):
        self.current_song_index +=1 
        #If index goes above 
        if self.current_song_index >= len(self.music_files):
            if self.loop:
                self.current_song_index = 0
            else :   
                self.songServiceObject.stop()
        # else : 
        
            
        

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
