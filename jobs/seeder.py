import sqlite3
from utils import hash
conn = sqlite3.connect('./db/music_db') 
c = conn.cursor()


def seeder():
    user()
    songs()
    playlists()
    albums()
    

def user():
    c.execute('''
          CREATE TABLE IF NOT EXISTS user
          ([id] TEXT PRIMARY KEY, [email] TEXT UNIQUE)
          ''')    
    c.execute("""INSERT INTO user (id, email)VALUES(?,?)""",(hash.GenerateID(),"kd1@gmail.com"))
    

def albums():
    c.execute('''
          CREATE TABLE IF NOT EXISTS albums
          ([id] TEXT PRIMARY KEY, [name] TEXT, [artist_name] TEXT, [createdAt] INTEGER,
          [image_url] TEXT)
          ''')
    

def playlists():
    c.execute('''
      CREATE TABLE IF NOT EXISTS playlists
      ([id] TEXT PRIMARY KEY, [song_ids] TEXT, [user_id] TEXT, [createdAt] INTEGER,[updatedAt] INTEGER,[deleted] BOOLEAN
      [image_url] TEXT)
      ''')
    


def songs():
    c.execute('''
          CREATE TABLE IF NOT EXISTS songs
          ([id] TEXT PRIMARY KEY, [name] TEXT, [album_id] TEXT, [createdAt] INTEGER,
          [location] TEXT)
          ''')

    

