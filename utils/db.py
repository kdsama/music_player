import sqlite3

def create_music_database():
    conn = sqlite3.connect("music.db")
    c = conn.cursor()

    # Create the music table if the music table doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS music
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, file_path TEXT NOT NULL)''')

    music_files = [
        "music/Westlife - Nothing's Gonna Change My Love For You.mp3",
    ]

    for music_file in music_files:
        c.execute("INSERT INTO music (file_path) VALUES (?)", (music_file,))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_music_database()
