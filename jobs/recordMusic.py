import os
import sqlite3
from mutagen.mp3 import MP3

# The directory path where the music files are located
music_dir = '../test_music'

# Connect to SQLite database
conn = sqlite3.connect('music_database.db')

# Create a table called "music"
conn.execute('''
CREATE TABLE IF NOT EXISTS music
(id INTEGER PRIMARY KEY AUTOINCREMENT,
filename TEXT,
title TEXT,
artist TEXT,
album TEXT,
duration INTEGER)
''')

# Loop through all MP3 files in the music folder
for filename in os.listdir(music_dir):
    if filename.endswith('.mp3'):
        # Use the mutagen module to get MP3 file tag information
        mp3 = MP3(os.path.join(music_dir, filename))
        title = mp3.get('TIT2', [''])[0]
        artist = mp3.get('TPE1', [''])[0]
        album = mp3.get('TALB', [''])[0]
        duration = int(mp3.info.length)

        # Insert label information into the database
        conn.execute('INSERT INTO music (filename, title, artist, album, duration) VALUES (?, ?, ?, ?, ?)',
                     (filename, title, artist, album, duration))
        conn.commit()

cursor = conn.cursor()
cursor.execute('SELECT * FROM music')
results = cursor.fetchall()
for row in results:
    print(row)
conn.close()
