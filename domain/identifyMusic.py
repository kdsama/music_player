import os
import sqlite3
from mutagen.mp3 import MP3


class identifyMusic:
    def __init__(self, music_dir, database_name) -> None:
        self.music_dir = music_dir
        self.database_name = database_name
    
    def loadLocalMusic(self):
        conn = sqlite3.connect(self.database_name)
        for filename in os.listdir(self.music_dir):
            if filename.endswith('.mp3'):
                # Use mutagen module to get MP3 file tag information
                mp3 = MP3(os.path.join(self.music_dir, filename))
                title = mp3.get('TIT2', [''])[0]
                artist = mp3.get('TPE1', [''])[0]
                album = mp3.get('TALB', [''])[0]
                duration = int(mp3.info.length)

                # Insert label information into the database
                conn.execute('INSERT INTO music (filename, title, artist, album, duration) VALUES (?, ?, ?, ?, ?)',
                            (filename, title, artist, album, duration))
                conn.commit()