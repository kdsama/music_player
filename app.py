from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QAction, QFileDialog, QListWidget, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from utils.play import MusicPlayer

class MusicPlayerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title
        self.setWindowTitle("Minimal Music Player")

        # Create menu bar
        menu_bar = self.menuBar()
        file_menu = QMenu("File", self)
        menu_bar.addMenu(file_menu)

        # Add actions to menu
        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_music_file)
        file_menu.addAction(open_action)

        # Create music selection list
        self.music_list = QListWidget(self)

        # Create play control buttons
        play_button = QPushButton("Play", self)
        play_button.clicked.connect(self.play_music)
        pause_button = QPushButton("Pause", self)
        pause_button.clicked.connect(self.pause_music)
        stop_button = QPushButton("Stop", self)
        stop_button.clicked.connect(self.stop_music)

        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(self.music_list)
        layout.addWidget(play_button)
        layout.addWidget(pause_button)
        layout.addWidget(stop_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Initialize media player
        self.music_player = MusicPlayer()

    def open_music_file(self):
        music_path, _ = QFileDialog.getOpenFileName(self, "Open the Music File", "", "MP3 (*.mp3);;All Files (*)")
        if music_path:
            self.music_list.addItem(music_path)
            self.music_player.setMedia(QMediaContent(QUrl.fromLocalFile(music_path)))

    def play_music(self):
        self.music_player.play()

    def pause_music(self):
        self.music_player.pause()

    def stop_music(self):
        self.music_player.stop()

if __name__ == "__main__":
    app = QApplication([])
    window = window = MusicPlayerApp()
    window.show()
    app.exec_()