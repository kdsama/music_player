from PyQt5.QtWidgets import QApplication,QDockWidget, QMainWindow,QHBoxLayout,QGridLayout, QMenuBar, QMenu, QAction, QFileDialog, QListWidget, QPushButton, QVBoxLayout, QWidget, QSlider, QLabel, QTextEdit
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt,QSize, QTimer
from PyQt5.QtGui import QPixmap, QIcon
from UI.play import MusicPlayer
from service.playlist import PlaylistService
from service.song import SongService
from db import song

START = "Start"
PAUSE = "Pause"


def GetPlayisSongPausedText(isSongPaused):
        if isSongPaused :
            return START
        return PAUSE

class SliderWindow(QWidget):
    def __init__(self,parent=None):
        super(SliderWindow,self).__init__(parent)

        layout = QVBoxLayout()
        self.slider = QSlider(Qt.Horizontal)
        layout.addWidget(self.slider)
        self.setLayout(layout)

class Volume(QPushButton):
    def __init__(self,parent=None):
        super(Volume,self).__init__(parent)

class MusicPlayerApp(QMainWindow):
    def __init__(self):
        super(MusicPlayerApp,self).__init__()

        self.slider = None
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
        open_action = QAction("Open New Song", self)
        open_action.triggered.connect(self.open_music_file)
        file_menu.addAction(open_action)
        open_action = QAction("Add New Songs to Queue", self)
        open_action.triggered.connect(self.queue_music_file)
        file_menu.addAction(open_action)

         # Create label for song name
        self.song_name = QLabel("Song Name")

        # Create play control buttons
        self.toggle_button = QPushButton("")        
        self.toggle_button.clicked.connect(self.toggle_music)
        self.toggle_button.setIcon(QIcon('UI/images/Play.png'))
        self.toggle_button.setToolTip("Play song")

        # Create next and previous buttons
        next_button = QPushButton("", self)
        next_button.setIcon(QIcon('UI/images/next.png'))
        next_button.setToolTip("Play next song")
        next_button.clicked.connect(self.next_music)

        prev_button = QPushButton("", self)
        prev_button.setIcon(QIcon('UI/images/previous.png'))
        prev_button.setToolTip("Play previous song")
        prev_button.clicked.connect(self.prev_music)

        # Create fast forward and rewind buttons
        fast_button = QPushButton("", self)
        fast_button.setIcon(QIcon('UI/images/fast_forward.png'))
        fast_button.setToolTip("Fast forward")
        fast_button.clicked.connect(self.fast_forward)
        rewind_button = QPushButton("", self)
        rewind_button.setIcon(QIcon('UI/images/rewind.png'))
        rewind_button.setToolTip("Rewind")
        rewind_button.clicked.connect(self.rewind)

        # Create reduce volume and add volume buttons
        reduce_volume_button = Volume(self)
        reduce_volume_button.setIcon(QIcon('UI/images/volume_down.png'))
        reduce_volume_button.setToolTip("Reduce volume")
        reduce_volume_button.clicked.connect(self.reduce_volume)

        add_volume_button = QPushButton("", self)
        add_volume_button.setIcon(QIcon('UI/images/volume_high.png'))
        add_volume_button.setToolTip("Increase volume")
        add_volume_button.clicked.connect(self.add_volume)

        # Create loop button
        self.loop_button = QPushButton("")
        self.loop_button.setIcon(QIcon('UI/images/repeat.png'))
        self.loop_button.setToolTip("Loop playlist")
        self.loop_button.setCheckable(True)
        self.loop_button.clicked.connect(self.call_loop_function)



        # Create position control slider
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


      # Create Playlist dock
        self.dock = QDockWidget('PlayLists',self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock)

        # Create music player list
        self.music_list = QListWidget(self)
        self.music_list.setWordWrap(True)
        self.music_list.itemClicked.connect(self.play_song_and_set_song_name)
        

        self.dock.setWidget(self.music_list)

        #layouts
        self.Mainlayout = QGridLayout()
        self.Mainlayout.addWidget(self.song_name, 0, 0,1,8)
        self.Mainlayout.addWidget(position_label, 1, 0,1,8)
        self.Mainlayout.addWidget(self.position_slider, 2, 0,1,8)
        self.Mainlayout.addWidget(QWidget(), 3, 0,1,8)
        self.Mainlayout.addWidget(self.toggle_button, 4, 0)
        self.Mainlayout.addWidget(next_button, 4, 1)
        self.Mainlayout.addWidget(prev_button, 4, 2)
        self.Mainlayout.addWidget(fast_button, 4, 3)
        self.Mainlayout.addWidget(rewind_button, 4, 4)
        self.Mainlayout.addWidget(reduce_volume_button, 4, 5)
        self.Mainlayout.addWidget(add_volume_button, 4, 6)
        self.Mainlayout.addWidget(self.loop_button, 4, 7)


        #sets the minsize of the mainwindow
        self.setMinimumSize(QSize(100, 100))
        

        container = QWidget()
        container.setLayout(self.Mainlayout)
        self.setCentralWidget(container)

        # Initialize media player
        self.playlist = PlaylistService([])
        last_song = self.playlist.last_played_song() 
        if last_song != "":
            self.playlist.addToPlaylist(last_song)
            self.refresh_playlist()


        self.set_volume()
        # self.music_player.get_music_list()

        # for music_path in self.music_player.get_music_list():
        #     self.music_list.addItem(music_path)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.toggle_music()
        elif event.key() == Qt.Key_Left and event.modifiers() == Qt.ControlModifier:
            self.reduce_volume()
        elif event.key() == Qt.Key_Right and event.modifiers() == Qt.ControlModifier:
            self.add_volume()
        elif event.key() == Qt.Key_Left or event.key() == Qt.Key_A:
            self.rewind()
        elif event.key() == Qt.Key_Right or event.key() == Qt.Key_D:
            self.fast_forward()
        elif event.key() == Qt.Key_Up or event.key() == Qt.Key_W:
            self.prev_music()
        elif event.key() == Qt.Key_Down or event.key() == Qt.Key_S:
            self.next_music()


    def open_music_file(self):
        music_path, _ = QFileDialog.getOpenFileName(self, "Open the Music File", "", "MP3 (*.mp3);;All Files (*)")
        
        if music_path:
            self.playlist.emptyCurrentPlaylist()
            self.playlist.addToPlaylist(music_path)

            # clear dock element-list
            #self.music_list.clear()
            #self.music_list.addItems(self.playlist.songs)

            self.play_music()
            self.refresh_playlist() 
        # self.position_slider.setMaximum(self.playlist.songServiceObject.duration)
    
    def queue_music_file(self):
        music_path, _ = QFileDialog.getOpenFileName(self, "Open the Music File", "", "MP3 (*.mp3);;All Files (*)")
        
        if music_path:
            self.playlist.addToPlaylist(music_path)
            #self.music_list.clear()
            #self.music_list.addItems(self.playlist.songs)
        if len(self.playlist.songs) == 1 :
            self.playlist.play(0)
            #self.toggle_button.setText(PAUSE)
            self.toggle_button.setIcon(QIcon('UI/images/Pause.png'))
            self.toggle_button.setToolTip("Pause song")
        self.refresh_playlist()
        # self.position_slider.setMaximum(self.playlist.songServiceObject.duration)

        
    def update_slider(self):
        print(self.playlist.songServiceObject.get_song_position())
        self.position_slider.setValue(self.playlist.songServiceObject.get_song_position())

    def update_song_position(self):
        self.position_slider.setSliderPosition(self.position_slider.value())

    def play_music(self):

        self.playlist.play()
        #self.toggle_button.setText(PAUSE)
        self.toggle_button.setIcon(QIcon('UI/images/Pause.png'))
        self.toggle_button.setToolTip("Pause song")

# Depending on the nature pause and play the song . 
    def toggle_music(self):

        #self.music_list.clear()
        #self.music_list.addItems(self.playlist.songs)

        if self.playlist.get_playlist_length() == 0 :
            print("We coming here ?")
            return 
        if not self.is_song_paused:
            if not self.LastOpenedSong :
                self.playlist.songServiceObject.pause()
                self.is_song_paused = True 
                #self.toggle_button.setText(START)
                self.toggle_button.setIcon(QIcon('UI/images/Play.png'))
                self.toggle_button.setToolTip("Play song")
            else:
                print("but we are xoming hee")
                self.LastOpenedSong = False
                self.play_music()
                
        else:
            self.playlist.songServiceObject.resume()
            self.is_song_paused = False
            #self.toggle_button.setText(PAUSE)
            self.toggle_button.setIcon(QIcon('UI/images/Pause.png'))
            self.toggle_button.setToolTip("Pause song")
            
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
        print("we coming here or not for fastforward ???")
        self.playlist.songServiceObject.go_front(10)

    def rewind(self):
        self.playlist.songServiceObject.go_back(10)
    
    def set_volume(self):
        self.start_volume = SongService.increase_and_return_new_volume(self.start_volume,0.0)

    def reduce_volume(self):
        
        self.start_volume = SongService.decrease_and_return_new_volume(self.start_volume,self.volume_change)
        # self.music_player.volume_down()

    def add_volume(self):
        
        self.start_volume = self.playlist.songServiceObject.increase_and_return_new_volume(self.start_volume,self.volume_change)
        # self.music_player.volume_up()

    def change_speed(self):
        pass

    def call_loop_function(self):
        if self.loop_button.isChecked():
            self.loop_button.setStyleSheet("background-color: white;border: 3px solid black;")
            self.toggleLoop()
        else:
            self.loop_button.setStyleSheet("background-color: white;color: black;font-weight: 600;border-radius: 4px;border: 1px solid #070707;padding: 5px 15px;margin-top: 10px;outline: 20px;")
    
    # Function to add slider to volume button
    #def slider_window(self):
    #    if self.slider is None:
    #        self.slider = SliderWindow(self) 
    #        #self.slider.setGeometry(100,200,640,480)
    #        self.Mainlayout.addWidget(self.slider,3,5,1,3)
    #        self.slider.show()
    #    else:
    #        self.slider.close()
    #        self.slider = None

    #Function to play the selected song and set song name label
    def play_song_and_set_song_name(self):

        #play song

        #sets Qlabel with selected song
        name = self.music_list.currentItem().text()
        print(name)
        self.song_name.setText(name)

        self.playlist.play_song_by_pathurl(name)

    def refresh_playlist(self):
        self.music_list.clear()
        print("Are we going to add to the playlist ???")
        try :
            song_name_list = SongService.get_song_names_from_pathurls(self.playlist.songs)
            print(song_name_list)
            self.music_list.addItems(song_name_list)
        except Exception as e : 
            self.music_list.addItems(self.playlist.songs)
    