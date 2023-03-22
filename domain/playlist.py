
class Playlist:
    def __init__(self, song_ids, name, user_id, created_at, updated_at, deleted):
        self.song_ids = song_ids
        self.name = name
        self.user_id = user_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted = deleted
    
    def savePlaylist(self):
        # save the playlist
        # db querying . Insert . Validation required for :- 
        # if the entries being passed are correct or not . 

        pass
    
    def getPlaylistByName(self, name):
        # get the playlist by name
        # straight forward db querying
        pass
    
    def getAllPlaylistsOfUser(self, user_id):
        # get all playlists of a user
        # straight forward db querying
        pass

