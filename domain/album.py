
class Album:
    def __init__(self, id, artist, name, image_url):
    # It might seem tricky when the object of this will be initiated. 
    # So it will go like - a db query - object initiated. 
    # 
        self.id = id
        self.artist = artist
        self.name = name
        self.image_url = image_url
    def SaveAlbum(self):
        # We already have most of the information , we just need to pass it to the db layer for the insertion part. 
        pass
    def getAlbumName(self):
        return self.name
    
    def getAlbumCover(self):
        return self.image_url
    
