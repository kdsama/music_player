
class Album:
    def __init__(self, id, artist, name, image_url):
        self.id = id
        self.artist = artist
        self.name = name
        self.image_url = image_url
    
    def getAlbumName(self):
        return self.name
    
    def getAlbumCover(self):
        return self.image_url
