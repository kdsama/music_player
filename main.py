from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QAction, QFileDialog, QListWidget, QPushButton, QVBoxLayout, QWidget, QSlider, QLabel, QTextEdit
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt
from UI.MusicPlayer import MusicPlayerApp

from service.song import SongService
from jobs.seeder import seeder
from db.song import Load


if __name__ == '__main__':
    seeder()
    # Load the cursor for the db 
    Load()
    app = QApplication([])
    window = MusicPlayerApp()
    window.show()
    app.exec_()    
    # song = SongService("test_music/Westlife - Nothing's Gonna Change My Love For You.mp3")
    # song.play()
    # song.wait(5)
    # song.pause()
    # song.wait(5)
    # song.resume()

