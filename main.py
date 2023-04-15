from PyQt5.QtWidgets import QApplication
from UI.MusicPlayer import MusicPlayerApp
from jobs.seeder import seeder
from db.song import Load
from pathlib import Path


if __name__ == '__main__':
    seeder()
    # Load the cursor for the db 
    Load()
    app = QApplication([])
    app.setStyleSheet(Path('UI/stylesheet.qss').read_text())
    window = MusicPlayerApp()
    window.show()
    app.exec_()    
    # song = SongService("test_music/Westlife - Nothing's Gonna Change My Love For You.mp3")
    # song.play()
    # song.wait(5)
    # song.pause()
    # song.wait(5)
    # song.resume()

