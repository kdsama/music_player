import sqlite3
import time

# Connect to the database
conn = ""
c = ""
def ReturnConnection():
    global conn,c
    conn = sqlite3.connect('./music_db')
    c = conn.cursor()
    return conn 

def Load():
    print("To load the database")

def song_exists(title, artist):
    query = "SELECT id FROM song WHERE title=? AND artist=?"
    c.execute(query, (title, artist))
    result = c.fetchone()
    conn.commit()
    return result is not None


def add_song(title, album, artist, duration, path):
    print(title,album,artist,duration,path)
    query = "INSERT INTO song (title, album, artist, duration, path) VALUES (?, ?, ?, ?, ?)"
    c.execute(query, (title, album, artist, duration, path))
    conn.commit()
    return c.lastrowid


def add_activity(song_id, position):
    print("Adding activity")
    query = "INSERT INTO activity (last_song_id, last_song_position) VALUES (?, ?)"
    c.execute(query, (song_id, position))
    conn.commit()

def CheckOrInsertSong(metadata):
    SongExists = song_exists(metadata["title"],metadata["artist"])
    print("Song exists",SongExists)
    if not SongExists : 
        song_id = add_song(metadata["title"], metadata["album"], metadata["artist"], metadata["duration"], metadata["path"])
        add_activity(song_id, 0)  
    else:
        song_id = SongExists[0]      
        add_activity(song_id, 0)
    conn.commit()

def get_last_played_song():
    # Query to join the song and activity tables on song id
    query = "SELECT song.*, activity.last_song_position FROM song JOIN activity ON song.id = activity.last_song_id ORDER BY activity.id DESC LIMIT 1"
    c.execute(query)
    result = c.fetchone()
    conn.commit()
    if result is None:
        # No song has been played yet, return None
        return None
    else:
        # Return a dictionary with song information and last song position
        return {
            'title': result[1],
            'album': result[2],
            'artist': result[3],
            'duration': result[4],
            'path': result[5],
            'last_position': result[6]
            
        }   

def get_last_n_played_songs(n, skip):
    # Query to join the song and activity tables on song id
    query = "SELECT song.*, activity.last_song_position FROM song JOIN activity ON song.id = activity.last_song_id ORDER BY activity.id DESC LIMIT ? OFFSET ?"
    c.execute(query, (n, skip))
    results = c.fetchall()
    conn.commit()
    if results is None:
        # No songs have been played yet, return an empty list
        return []
    else:
        # Return a list of dictionaries with song information and last song position
        songs = []
        for result in results:
            song = {
                'title': result[1],
                'album': result[2],
                'artist': result[3],
                'duration': result[4],
                'path': result[5],
                'last_position': result[6]
            }
            songs.append(song)
        return songs
    
# Get n songs for a particular artist
def get_n_songs_for_artist(artist, n):
    # Query to select n songs for a particular artist
    query = "SELECT * FROM song WHERE artist=? LIMIT ?"
    c.execute(query, (artist, n))
    results = c.fetchall()
    conn.commit()
    if results is None:
        # No songs found for the given artist, return an empty list
        return []
    else:
        # Return a list of dictionaries with song information
        songs = []
        for result in results:
            song = {
                'title': result[1],
                'album': result[2],
                'artist': result[3],
                'duration': result[4],
                'path': result[5],
                'last_position': None,
                'timestamp': int(time.time())
            }
            songs.append(song)
        return songs

# Get n songs for a particular album
def get_n_songs_for_album(album, n):
    # Query to select n songs for a particular album
    query = "SELECT * FROM song WHERE album=? LIMIT ?"
    c.execute(query, (album, n))
    results = c.fetchall()
    conn.commit()
    if results is None:
        # No songs found for the given album, return an empty list
        return []
    else:
        # Return a list of dictionaries with song information
        songs = []
        for result in results:
            song = {
                'title': result[1],
                'album': result[2],
                'artist': result[3],
                'duration': result[4],
                'path': result[5],
                'last_position': None,
                'timestamp': int(time.time())
            }
            songs.append(song)
        return songs

# Get n songs for a particular artist where the song is played less than 5 times
def get_n_songs_for_artist_played_less_than(artist, n, times_played):
    # Query to select n songs for a particular artist where the song is played less than times_played
    query = "SELECT song.*, activity.last_song_position, COUNT(activity.last_song_id) as play_count FROM song LEFT JOIN activity ON song.id = activity.last_song_id WHERE song.artist=? GROUP BY song.id HAVING play_count < ? ORDER BY play_count ASC LIMIT ?"
    c.execute(query, (artist, times_played, n))
    results = c.fetchall()
    conn.commit()
    if results is None:
        # No songs found for the given artist, return an empty list
        return []
    else:
        # Return a list of dictionaries with song information and play count
        songs = []
        for result in results:
            song = {
                'title': result[1],
                'album': result[2],
                'artist': result[3],
                'duration': result[4],
                'path': result[5],
                'last_position': result[6],
                'timestamp': int(time.time())
            }
            songs.append(song)
        return songs
    
def get_n_songs_played_the_most(n):
    
    
    c.execute("""
        SELECT song.title, song.album, song.artist, COUNT(activity.song_id) as plays
        FROM song
        JOIN (
            SELECT song_id FROM activity
            ORDER BY created_at DESC
            LIMIT ?
        ) AS activity_sub ON song.id = activity_sub.song_id
        GROUP BY activity_sub.song_id
        ORDER BY plays DESC
    """, (n,))
    results = c.fetchall()
    conn.commit()
    if results is None:
        # No songs found for the given artist, return an empty list
        return []
    else:
        # Return a list of dictionaries with song information and play count
        songs = []
        for result in results:
            song = {
                'title': result[1],
                'album': result[2],
                'artist': result[3],
                'duration': result[4],
                'path': result[5],
                'last_position': result[6],
                'timestamp': int(time.time())
            }
            songs.append(song)
        return songs








# Commit the changes and close the connection


