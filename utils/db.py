import sqlite3
import os
from mutagen.mp3 import MP3


class identifyMusic:
    def __init__(self, music_dir, database_name) -> None:
        self.music_dir = music_dir
        self.database_name = database_name
    
    def create_music_database(self):
        conn = sqlite3.connect(self.database_name)
        c = conn.cursor()

        # Create the music table if the music table doesn't exist
        c.execute('''
        CREATE TABLE IF NOT EXISTS music
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        title TEXT,
        artist TEXT,
        album TEXT,
        duration INTEGER)
        ''')
    
    def load_local_music(self):
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
        # 展示目前music表中的数据
        # cursor = conn.cursor()
        # cursor.execute('SELECT * FROM music')
        # results = cursor.fetchall()
        # for row in results:
        #     print(row)       
        conn.commit()
        conn.close()

if __name__ == "__main__":
    identify = identifyMusic(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../music'), 'music.db')
    identify.create_music_database()
    identify.load_local_music()
