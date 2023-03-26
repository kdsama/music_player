import sqlite3
from utils import hash 
conn = sqlite3.connect('./db/music_db') 
c = conn.cursor()


def seeder():
    
    songs()
    playlists()
    activity()
    



def playlists():
    c.execute('''
        CREATE TABLE playlist (
          id INTEGER PRIMARY KEY,
          name TEXT,
          created_at INTEGER,
          updated_at INTEGER
        );
      ''')
    c.execute('''
       CREATE TABLE playlist_song (
          playlist_id INTEGER,
          song_id INTEGER,
          FOREIGN KEY (playlist_id) REFERENCES playlist(id),
          FOREIGN KEY (song_id) REFERENCES song(id),
          PRIMARY KEY (playlist_id, song_id)
        );  
    ''')

def activity():
    c.execute('''
    CREATE TABLE activity (
          id INTEGER PRIMARY KEY,
          last_song_id INTEGER,
          last_song_position INTEGER,
          created_at INTEGER,
          FOREIGN KEY (last_song_id) REFERENCES song(id)
        );    
    ''')


def songs():
    c.execute('''
         CREATE TABLE song (
        id INTEGER PRIMARY KEY,
        title TEXT,
        album TEXT,
        artist TEXT,
        duration INTEGER,
        path TEXT,
        created_at INTEGER,
        updated_at INTEGER
        );
          ''')

    








