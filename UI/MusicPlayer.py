from PyQt5.QtWidgets import QApplication,QDockWidget, QMainWindow,QHBoxLayout, QMenuBar, QMenu, QAction, QFileDialog, QListWidget, QPushButton, QVBoxLayout, QWidget, QSlider, QLabel, QTextEdit
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt,QSize, QTimer
from UI.play import MusicPlayer
from service.playlist import PlaylistService
from db import song

START = "Start"
PAUSE = "Pause"


def GetPlayisSongPausedText(isSongPaused):
        if isSongPaused :
            return START
        return PAUSE



class MusicPlayerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        
        self.is_song_paused = False

        self.LastOpenedSong = True 
        # Create window title
        self.setWindowTitle("Minimal Music Player")
        
        # Create menu bar
        menu_bar = self.menuBar()
        file_menu = QMenu("File", self)
        menu_bar.addMenu(file_menu)

        self.start_volume = 0.5
        self.volume_change = 0.1
        # Add actions to menu
        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_music_file)
        file_menu.addAction(open_action)


        # Create play control buttons
        self.toggle_button = QPushButton("TogglePlay", self)        
        self.toggle_button.clicked.connect(self.toggle_music)
        self.toggle_button.setText(START)

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
        position_label = QLabel("Position:", self)
        self.position_slider = QSlider(Qt.Horizontal, self)
        self.position_slider.setMinimum(0)
        
        
        self.position_slider.valueChanged.connect(self.update_song_position)
        timer = QTimer()
        timer.timeout.connect(self.update_slider)
        timer.start(1000)


        # # # Create lyrics area
        # # lyrics_label = QLabel("Lyrics:", self)
        # # self.lyrics_area = QTextEdit(self)
        # # self.lyrics_area.setReadOnly(True)
        # # Create music player list
        # self.music_list = QListWidget(self)
        # self.music_list.setWordWrap(True)
      # Create Playlist dock
        self.dock = QDockWidget('PlayLists',self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock)

        # Create music player list
        self.music_list = QListWidget(self)
        self.music_list.setWordWrap(True)

        
        
        self.dock.setWidget(self.music_list)

        #layouts
        Mainlayout = QVBoxLayout()
        ButtonLayout = QHBoxLayout()
        #sets the minsize of the mainwindow
        self.setMinimumSize(QSize(50, 50))

        # Update widget to pannel

        Mainlayout.addWidget(position_label)
        Mainlayout.addWidget(self.position_slider)
        Mainlayout.addLayout(ButtonLayout)
        #Mainlayout.addWidget(lyrics_label)
        #Mainlayout.addWidget(self.lyrics_area)
        ButtonLayout.addWidget(self.toggle_button)  
        #ButtonLayout.addWidget(stop_button)  
        ButtonLayout.addWidget(next_button)
        ButtonLayout.addWidget(prev_button)
        ButtonLayout.addWidget(fast_button)
        ButtonLayout.addWidget(rewind_button)
        ButtonLayout.addWidget(reduce_volume_button)
        ButtonLayout.addWidget(add_volume_button)
        

        container = QWidget()
        container.setLayout(Mainlayout)
        self.setCentralWidget(container)

        # Initialize media player
        self.playlist = PlaylistService([])
        last_song = self.playlist.last_played_song() 
        if last_song != "":
            self.playlist.addToPlaylist(last_song)


        self.set_volume()
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
        self.position_slider.setMaximum(self.playlist.songServiceObject.duration)
        
        
    def update_slider(self):
        print(self.playlist.songServiceObject.get_song_position())
        self.position_slider.setValue(self.playlist.songServiceObject.get_song_position())

    def update_song_position(self):
        self.position_slider.setSliderPosition(self.position_slider.value())

    def play_music(self):
        self.playlist.play()

# Depending on the nature pause and play the song . 
    def toggle_music(self):
        
        if not self.is_song_paused:
            if not self.LastOpenedSong :
                print("We should come here now ")
                self.playlist.songServiceObject.pause()
                self.is_song_paused = True 
                self.toggle_button.setText(START)
            else:
                print("but we are xoming hee")
                self.LastOpenedSong = False
                self.play_music()
                self.toggle_button.setText(PAUSE)
        else:
            self.playlist.songServiceObject.resume()
            self.is_song_paused = False
            self.toggle_button.setText(PAUSE)

            
    def toggleLoop(self):
        self.playlist.toggleLoop()
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
    
    def set_volume(self):
        self.start_volume = self.playlist.songServiceObject.increase_and_return_new_volume(self.start_volume,0.0)

    def reduce_volume(self):
        
        self.start_volume = self.playlist.songServiceObject.decrease_and_return_new_volume(self.start_volume,self.volume_change)
        # self.music_player.volume_down()

    def add_volume(self):
        
        self.start_volume = self.playlist.songServiceObject.increase_and_return_new_volume(self.start_volume,self.volume_change)
        # self.music_player.volume_up()

    def change_speed(self):
        pass





    