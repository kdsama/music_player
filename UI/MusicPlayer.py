from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QAction, QFileDialog, QListWidget, QPushButton, QVBoxLayout, QWidget, QSlider, QLabel, QTextEdit
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt
from UI.play import MusicPlayer
from service.playlist import PlaylistService


START = "Start"
PAUSE = "Pause"


def GetPlayisSongPausedText(isSongPaused):
        if isSongPaused :
            return START
        return PAUSE



class MusicPlayerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create window title
        self.setWindowTitle("Minimal Music Player")

        # Create menu bar
        menu_bar = self.menuBar()
        file_menu = QMenu("File", self)
        menu_bar.addMenu(file_menu)
        self.is_song_paused = False
        # Add actions to menu
        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_music_file)
        file_menu.addAction(open_action)

        # Create music player list
        self.music_list = QListWidget(self)

        # Create play control buttons
        # play_button = QPushButton("Load Library", self)
        # play_button.clicked.connect(self.play_music)

        self.toggle_button = QPushButton("TogglePlay", self)
        
        self.is_song_paused = False
        self.toggle_button.clicked.connect(self.toggle_music)
        self.toggle_button.setText(START)
        
        # stop_button = QPushButton("Stop", self)
        # stop_button.clicked.connect(self.stop)

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
        # layout.addWidget(play_button)  
        layout.addWidget(self.toggle_button) 
        # layout.addWidget(stop_button)  
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
        self.playlist = PlaylistService([])
        # self.music_player.get_music_list()

        # for music_path in self.music_player.get_music_list():
        #     self.music_list.addItem(music_path)


    def open_music_file(self):
        music_path, _ = QFileDialog.getOpenFileName(self, "Open the Music File", "", "MP3 (*.mp3);;All Files (*)")
        
        if music_path:
            self.playlist.addToPlaylist(music_path)
        if len(self.playlist.songs) == 1 :
            self.playlist.play(0)
            self.toggle_button.setText(PAUSE)
        


    def play_music(self):
        pass

# Depending on the nature pause and play the song . 
    def toggle_music(self):
        
        if not self.is_song_paused:
            self.playlist.songServiceObject.pause()
            self.is_song_paused = True 
            self.toggle_button.setText(START)
        else:
            self.playlist.songServiceObject.resume()
            self.is_song_paused = False
            self.toggle_button.setText(PAUSE)

            

    # def stop_music(self):
    #     self.music_player.quit()

    def update_lyrics(self, lyrics):
        pass

    def next_music(self):
        self.playlist.next()

    def prev_music(self):
        self.playlist.previous()

    def fast_forward(self):
        self.playlist.songServiceObject.go_front(10)

    def rewind(self):
        self.playlist.songServiceObject.go_back(10)
    
    def reduce_volume(self):
        pass
        # self.music_player.volume_down()

    def add_volume(self):
        pass
        # self.music_player.volume_up()

    def change_speed(self):
        pass





    