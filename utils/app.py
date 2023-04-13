from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QAction, QFileDialog, QListWidget, QPushButton, QVBoxLayout, QWidget, QSlider, QLabel, QTextEdit
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt
from play import MusicPlayer

class MusicPlayerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create window title
        self.setWindowTitle("Minimal Music Player")

        # Create menu bar
        menu_bar = self.menuBar()
        file_menu = QMenu("File", self)
        menu_bar.addMenu(file_menu)

        # Add actions to menu
        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_music_file)
        file_menu.addAction(open_action)

        # Create music player list
        self.music_list = QListWidget(self)

        # Create play control buttons
        play_button = QPushButton("Load Library", self)
        play_button.clicked.connect(self.play_music)
        pause_button = QPushButton("Pause", self)
        pause_button.clicked.connect(self.pause_music)
        stop_button = QPushButton("Stop", self)
        stop_button.clicked.connect(self.stop_music)

        # Create next and previous buttons
        next_button = QPushButton("Next", self)
        next_button.clicked.connect(self.next_music)
        prev_button = QPushButton("Previous", self)
        prev_button.clicked.connect(self.prev_music)

        # Create fast forward and rewind buttons
        fast_button = QPushButton("fast forward", self)
        fast_button.clicked.connect(self.fast_forward)
        rewind_button = QPushButton("rewind", self)
        rewind_button.clicked.connect(self.rewind)

        # Create reduce volume and add volume buttons
        reduce_volume_button = QPushButton("reduce volume", self)
        reduce_volume_button.clicked.connect(self.reduce_volume)
        add_volume_button = QPushButton("add volume", self)
        add_volume_button.clicked.connect(self.add_volume)

        # Create speed control slider
        speed_label = QLabel("Speed:", self)
        speed_slider = QSlider(Qt.Horizontal, self)
        speed_slider.setMinimum(50)
        speed_slider.setMaximum(200)
        speed_slider.setValue(100)
        speed_slider.valueChanged.connect(self.change_speed)

        # Create lyrics area
        lyrics_label = QLabel("Lyrics:", self)
        self.lyrics_area = QTextEdit(self)
        self.lyrics_area.setReadOnly(True)

        # Update widget to pannel
        layout = QVBoxLayout()
        layout.addWidget(self.music_list)
        layout.addWidget(play_button)  
        layout.addWidget(pause_button) 
        layout.addWidget(stop_button)  
        layout.addWidget(next_button)
        layout.addWidget(prev_button)
        layout.addWidget(fast_button)
        layout.addWidget(rewind_button)
        layout.addWidget(reduce_volume_button)
        layout.addWidget(add_volume_button)
        layout.addWidget(speed_label)
        layout.addWidget(speed_slider)
        layout.addWidget(lyrics_label)
        layout.addWidget(self.lyrics_area)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Initialize media player
        self.music_player = MusicPlayer()
        self.music_player.get_music_list()

        for music_path in self.music_player.get_music_list():
            self.music_list.addItem(music_path)


    def open_music_file(self):
        music_path, _ = QFileDialog.getOpenFileName(self, "Open the Music File", "", "MP3 (*.mp3);;All Files (*)")
        if music_path:
            self.music_list.addItem(music_path)
            self.music_player.setMedia(QMediaContent(QUrl.fromLocalFile(music_path)))

    def play_music(self):
        pass

    def pause_music(self):
        self.music_player.pause()

    def stop_music(self):
        self.music_player.quit()

    def update_lyrics(self, lyrics):
        pass

    def next_music(self):
        self.music_player.next_song()

    def prev_music(self):
        self.music_player.previous_song()

    def fast_forward(self):
        self.music_player.fast_forward()

    def rewind(self):
        self.music_player.rewind()
    
    def reduce_volume(self):
        self.music_player.volume_down()

    def add_volume(self):
        self.music_player.volume_up()

    def change_speed(self):
        pass

if __name__ == "__main__":
    app = QApplication([])
    window = MusicPlayerApp()
    window.show()
    app.exec_()