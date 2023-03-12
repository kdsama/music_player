class Song:
    def __init__(self, id, name, album_id, created_at, location, album):
        self.id = id
        self.name = name
        self.album_id = album_id
        self.created_at = created_at
        self.location = location
        self.album = album
    
    def play(self):
        # play the song
        pass
    
    def load(self):
        # load the song
        pass
    
    def pause(self):
        # pause the song
        pass
    
    def go_back(self, n):
        # go back n seconds in the song
        pass
    
    def go_front(self, n):
        # go forward n seconds in the song
        pass
