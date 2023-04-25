from PyQt5.QtWidgets import QApplication,QDockWidget, QMainWindow,QHBoxLayout,QGridLayout, QMenuBar, QMenu, QAction, QFileDialog,QLineEdit, QListWidget, QPushButton, QVBoxLayout, QWidget, QSlider, QLabel, QTextEdit
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt,QSize, QTimer, QEvent
from PyQt5.QtGui import QPixmap, QIcon,QPainter,QBrush,QColor
from UI.play import MusicPlayer
from service.playlist import PlaylistService
from service.song import SongService
from UI.components.volume import Volume
from UI.components.help import Help
import random 
from db import song
import os
START = "Start"
PAUSE = "Pause"
ONE_HOUR_IN_MILISECONDS = 3600000
HALF_HOUR_IN_MILISECONDS = 1800000




class MusicPlayerApp(QMainWindow):
    def __init__(self):
        super(MusicPlayerApp,self).__init__()

        self.timer_button_count = 0
        self.slider = None
        self.is_song_paused = False
        self.next_time_check = False
        self.prev_time_check = False
        
        self.sliderPos = 0 
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
        self.open_action = QAction("Open New Song", self)
        self.open_action.triggered.connect(self.open_music_file)
        file_menu.addAction(self.open_action)
        self.open_action = QAction("Add New Songs to Queue", self)
        self.open_action.triggered.connect(self.queue_music_file)
        file_menu.addAction(self.open_action)
        self.help_action = QAction("Shortcuts")
        file_menu.addAction(self.help_action)
        self.help_action.triggered.connect(self.help_menu)
        self.close_action = QAction("Close")
        file_menu.addAction(self.close_action)
        self.close_action.triggered.connect(self.close_fn)

        # Create label for song name
        self.song_name = QLabel()

        # Create song image
        self.Image = QLabel(self)
        self.Image.setFixedSize(QSize(200,200))

        

        # Create play control buttons
        self.toggle_button = QPushButton("")        
        self.toggle_button.clicked.connect(self.toggle_music)
        self.toggle_button.setIcon(QIcon('UI/img/Play.png'))
        self.toggle_button.setToolTip("Play song")
        self.toggle_button.setFixedSize(QSize(60,60))

        # Create next and previous buttons
        next_button = QPushButton("", self)
        next_button.setObjectName('next_button')
        next_button.setIcon(QIcon('UI/img/next.png'))
        next_button.setToolTip("click to play next song / hold to fast forward")
        next_button.pressed.connect(self.next_button_pressed)
        next_button.released.connect(self.next_button_released)
        next_button.setFixedSize(QSize(60,60))

        prev_button = QPushButton("", self)
        prev_button.setIcon(QIcon('UI/img/previous.png'))
        prev_button.setToolTip("Click to play previous song / hold to rewind")
        prev_button.pressed.connect(self.prev_button_pressed)
        prev_button.released.connect(self.prev_button_released)
        prev_button.setFixedSize(QSize(60,60))


        '''
        # Create fast forward and rewind buttons
        fast_button = QPushButton("", self)
        fast_button.setIcon(QIcon('UI/img/images/fast_forward.png'))
        fast_button.setToolTip("Fast forward")
        fast_button.clicked.connect(self.fast_forward)
        fast_button.setFixedSize(QSize(60,60))

        rewind_button = QPushButton("", self)
        rewind_button.setIcon(QIcon('UI/img/images/rewind.png'))
        rewind_button.setToolTip("Rewind")
        rewind_button.clicked.connect(self.rewind)
        rewind_button.setFixedSize(QSize(60,60))
        '''

        # Create reduce volume and add volume buttons
        reduce_volume_button = Volume(self)
        reduce_volume_button.setIcon(QIcon('UI/img/volume_down.png'))
        reduce_volume_button.setToolTip("Reduce volume")
        reduce_volume_button.clicked.connect(self.reduce_volume)
        reduce_volume_button.setFixedSize(QSize(60,60))

        add_volume_button = QPushButton("", self)
        add_volume_button.setIcon(QIcon('UI/img/volume_high.png'))
        add_volume_button.setToolTip("Increase volume")
        add_volume_button.clicked.connect(self.add_volume)
        add_volume_button.setFixedSize(QSize(60,60))

        # Volume Slider
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.sliderReleased.connect(self.VolumeSliderMovement)

        # Create loop button
        self.loop_button = QPushButton("")
        self.loop_button.setIcon(QIcon('UI/img/repeat.png'))
        self.loop_button.setToolTip("Loop playlist")
        self.loop_button.setCheckable(True)
        self.loop_button.clicked.connect(self.call_loop_function)
        self.loop_button.setFixedSize(QSize(60,60))

        # Create Timer button
        self.timer_button = QPushButton("")
        self.timer_button.setIcon(QIcon('UI/img/timer.png'))
        self.timer_button.setText('No Timer')
        self.timer_button.setToolTip("No timer set")
        self.timer_button.setObjectName('timer_button')
        self.timer_button.clicked.connect(self.call_timer_function)
        self.timer_button.setFixedSize(QSize(150,60))

        # Create position control slider
        position_label = QLabel("Position:", self)
        self.position_slider = QSlider(Qt.Horizontal, self)
        self.position_slider.setMinimum(0)
        
        
        self.position_slider.sliderReleased.connect(self.update_song_position)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_slider)

      # Create Playlist dock
        self.dock = QDockWidget('PlayLists',self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock)

        # Create music player list
        self.music_list = QListWidget(self)
        self.music_list.setWordWrap(True)
        self.music_list.itemDoubleClicked.connect(self.play_song_and_set_song_name)


        # Create search bar
        self.SearchBar = QLineEdit()
        self.SearchBar.installEventFilter(self)
        self.SearchBar.textChanged.connect(self.search_playlist)

        #set place holder text for search bar
        self.SearchBar.setPlaceholderText("Search here...")
        
        #self.dock_layout = QVBoxLayout()
        self.dock.setTitleBarWidget(self.SearchBar)
        self.dummy_widget = QWidget()
        self.dock_layout = QVBoxLayout()
        self.dock_layout.addWidget(QLabel('Playlists'))
        self.dock_layout.addWidget(self.music_list)
        self.dummy_widget.setLayout(self.dock_layout)
        self.dock.setWidget(self.dummy_widget)
        
        #self.dock.setLayout(self.dock_layout)

        self.tn = QTimer()
        self.tn.timeout.connect(self.fast_forward)
        self.tp = QTimer()
        self.tp.timeout.connect(self.rewind)

        #layouts
        self.Mainlayout = QGridLayout()
        self.Buttonlayout = QHBoxLayout()
        self.Mainlayout.setHorizontalSpacing(50)
        self.Buttonlayout.setSpacing(4)
        self.Mainlayout.addWidget(self.Image,0,0,2,3,alignment= Qt.AlignmentFlag.AlignHCenter)
        self.Mainlayout.addWidget(self.song_name, 0, 3,1,2)
        self.Mainlayout.addWidget(position_label, 3, 0,1,5)
        self.Mainlayout.addWidget(self.position_slider, 4, 0,1,5)
        self.Mainlayout.addWidget(QWidget(), 2, 0,1,5)
     
        self.Buttonlayout.addWidget(self.toggle_button)
        self.Buttonlayout.addWidget(prev_button)
        self.Buttonlayout.addWidget(next_button)
        #self.Mainlayout.addWidget(fast_button, 1, 7)
        #self.Mainlayout.addWidget(rewind_button, 1, 8)
        self.Buttonlayout.addWidget(reduce_volume_button)
        self.Buttonlayout.addWidget(add_volume_button)
        self.Buttonlayout.addWidget(self.loop_button)
        self.Buttonlayout.addWidget(self.timer_button)
        self.Mainlayout.addLayout(self.Buttonlayout,1,3)


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

        #self.music_list.currentItemChanged.connect(lambda: print("Item Changed Signal"))
        name = self.music_list.item(0)
        #self.music_list.setCurrentItem(name)
        # Fresh installation , there might not be a preloaded song 
        try : 
            self.song_name.setText(name.text())
            self.refresh_image()
        except Exception as e : 
            self.song_name.setText("")

        self.set_volume()
        self.sleep_timer = QTimer()
        self.sleep_timer.timeout.connect(self.closeEvent)
                
    def eventFilter(self, source, event):
        if (event.type() == QEvent.KeyPress and
            source is self.SearchBar):
            return super(MusicPlayerApp, self).eventFilter(source, event)
        return False

    def keyPressEvent(self, event):
        
        if event.key() == Qt.Key_Space or event.key() == Qt.Key_P:
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
            try : 
                self.prev_music()
            except Exception as e : 
                self.reset_controls_on_edge_songs()
        elif event.key() == Qt.Key_Down or event.key() == Qt.Key_S:
            try : 
                self.next_music()
            except Exception as e : 
                self.reset_controls_on_edge_songs()
            


    def open_music_file(self):
        music_path, _ = QFileDialog.getOpenFileName(self, "Open the Music File", "", "MP3 (*.mp3);;All Files (*)")
        
        if music_path:
            self.playlist.emptyCurrentPlaylist()
            self.playlist.addToPlaylist(music_path)


            self.play_music()
            self.refresh_playlist() 
        # self.position_slider.setMaximum(self.playlist.songServiceObject.duration)
    
    def queue_music_file(self):
        music_path, _ = QFileDialog.getOpenFileName(self, "Open the Music File", "", "MP3 (*.mp3);;All Files (*)")
        
        if music_path:
            self.playlist.addToPlaylist(music_path)

        if len(self.playlist.songs) == 1 :
            self.playlist.play(0)
            #self.toggle_button.setText(PAUSE)
            self.toggle_button.setIcon(QIcon('UI/img/Pause.png'))
            self.toggle_button.setToolTip("Pause song")
        self.refresh_playlist()
        # self.position_slider.setMaximum(self.playlist.songServiceObject.duration)



        
    def help_menu(self):
        self.h = Help()
        self.h.setStyleSheet("background-color: #3C4048;;")
        #self.h.setText()
        #self.Mainlayout.addWidget(self.h,5,0)
        self.h.show()

    def close_fn(self):
        pass

    def update_slider(self):
        # Dont do anything if there is no songs 
        if len(self.playlist.songs) == 0 : 
            return 
        
        song_position = self.playlist.songServiceObject.get_song_position()
        self.position_slider.setValue(song_position)
        
        duration = self.playlist.songServiceObject.duration
        if self.sliderPos - duration < 20 and self.sliderPos  >= song_position:
            try :
                self.next_music()
            except Exception as e : 
                # Means no next song probably 
                self.reset_controls_on_edge_songs()
        else : 
            
            self.sliderPos = song_position
        
        # self.change_song_check()        

    def search_playlist(self,text):
        if text == "":
            self.refresh_playlist()
        else : 
            self.music_list.clear()
            self.music_list.addItems(self.playlist.get_song_by_partial_input(text))

    def update_song_position(self):
        self.timer.stop()
        #  get previous song position 
        # subtract it with current Slider position 
        #  and use the fast forward to rewind option accordingly 
        new_pos = self.position_slider.value()
        if self.sliderPos < new_pos : 
            self.fast_forward(int(new_pos-self.sliderPos))
        else : 
            self.rewind(int(self.sliderPos-new_pos))
        self.timer.start(1000)

    def play_music(self):
        self.playlist.play()
        #self.toggle_button.setText(PAUSE)
        self.refresh_slider_info()
        self.toggle_button.setIcon(QIcon('UI/img/Pause.png'))
        self.toggle_button.setToolTip("Pause song")

# Depending on the nature pause and play the song . 
    def toggle_music(self):
        self.timer.start(1000)
        
        
        if self.playlist.get_playlist_length() == 0 :
            

            self.timer.stop()
            return 
        self.refresh_slider_info()
        if not self.is_song_paused:
            if not self.LastOpenedSong :
                self.playlist.songServiceObject.pause()
                self.is_song_paused = True 
                #self.toggle_button.setText(START)
                self.toggle_button.setIcon(QIcon('UI/img/Play.png'))
                self.toggle_button.setToolTip("Play song")
            else:
                
                self.LastOpenedSong = False
                self.play_music()
                
        else:
            self.playlist.songServiceObject.resume()
            self.is_song_paused = False
            #self.toggle_button.setText(PAUSE)
            self.toggle_button.setIcon(QIcon('UI/img/Pause.png'))
            self.toggle_button.setToolTip("Pause song")
            
    def toggleLoop(self):
        self.playlist.toggleLoop()


    # Set the title name of the song. Whenever you select a song , you are shown which current song is being played.
    def set_player_title(self,name=""):
        if name == "":
            name_list = SongService.get_song_names_from_pathurls([self.playlist.songs[self.playlist.current_song_index]])
            self.song_name.setText(name_list[0])
        else : 
            self.song_name.setText(name)

    def refresh_image(self):        
        img = self.playlist.current_song_index % 12 + 1 
        
        pixmap = QPixmap('UI/random_stock_images/'+str(img))
        self.Image.setPixmap(pixmap)
        
        pixmap.scaledToWidth(64)
        pixmap.scaledToHeight(64)

        
    def refresh_slider_info(self):
        self.refresh_image()
        self.sliderPos = 0 
        self.position_slider.setMaximum(self.playlist.songServiceObject.duration)
        self.position_slider.setMinimum(0)
        self.position_slider.setValue(0)


    def next_music(self):
        
        self.playlist.next()
        self.set_player_title()
        self.refresh_slider_info()
        self.refresh_playlist()
        # get song name of the next song and set Name to it 



    def prev_music(self):
        self.playlist.previous()
        self.set_player_title()
        self.refresh_slider_info()
        self.refresh_playlist()

    def move_song_to_position(self,slider_pos):
        self.playlist.songServiceObject.move_song_to_position(slider_pos)

    def fast_forward(self,seconds=10):
        self.next_time_check = True
        self.playlist.songServiceObject.go_front(seconds)

    def rewind(self,seconds=10):
        self.prev_time_check = True
        self.playlist.songServiceObject.go_back(seconds)
    
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
            self.loop_button.setStyleSheet("border: 3px solid #00ABB3;background-color: #EAEAEA;")
            self.toggleLoop()
        else:
            self.loop_button.setStyleSheet("border: 1px solid #070707;background-color: #B2B2B2")
            self.toggleLoop()
    


    #Function to play the selected song and set song name label
    def play_song_and_set_song_name(self):

        #play song
        name = self.music_list.currentItem().text()
        self.set_player_title(name)        
        self.playlist.play_song_by_name(name)

        self.is_song_paused = False
        self.LastOpenedSong = False
        self.toggle_button.setIcon(QIcon('UI/img/Pause.png'))
        self.toggle_button.setToolTip("Pause song")
        print("WTFFFFFFFFFFFFFFFFFFFFFFFF")
        self.refresh_slider_info()


    def refresh_playlist(self):
        self.SearchBar.clear()
        self.music_list.clear()
        try :
            song_name_list = SongService.get_song_names_from_pathurls(self.playlist.songs)
            self.music_list.addItems(song_name_list)
        except Exception as e : 
            self.music_list.addItems(self.playlist.songs)


    def call_timer_function(self):
        time_to_sleep_in_seconds = 0
        if self.timer_button_count == 0:
            self.timer_button.setToolTip("Pause after 30 minutes")
            self.timer_button.setStyleSheet("border: 3px solid #00ABB3;background-color: #EAEAEA;")
            self.timer_button.setText('30 minutes ')
            self.timer_button.setFixedSize(QSize(150,60))
            self.timer_button_count = 1
            time_to_sleep_in_seconds = HALF_HOUR_IN_MILISECONDS
            self.sleep_timer.start(time_to_sleep_in_seconds*1000)
            #self.toggleTimer()

        elif self.timer_button_count == 1:
            self.timer_button.setToolTip("Pause after 1 hour")
            self.timer_button.setStyleSheet("border: 3px solid #00ABB3;background-color: #EAEAEA;")            
            self.timer_button.setText('1 hour ')
            self.timer_button.setFixedSize(QSize(150,60))
            self.timer_button_count = 2
            time_to_sleep_in_seconds = ONE_HOUR_IN_MILISECONDS
            self.sleep_timer.start(time_to_sleep_in_seconds)
        
        elif self.timer_button_count == 2:
            self.timer_button.setToolTip("Pause after 1 hour")
            self.timer_button.setStyleSheet("border: 3px solid #00ABB3;background-color: #EAEAEA;")            
            self.timer_button.setText('15s (Demo) ')
            self.timer_button.setFixedSize(QSize(150,60))
            self.timer_button_count = 3
            time_to_sleep_in_seconds = 15
            self.sleep_timer.start(time_to_sleep_in_seconds*1000)

        elif self.timer_button_count == 3:
            self.timer_button.setToolTip("No timer set")
            self.timer_button.setStyleSheet("border: 1px solid #070707;background-color: #B2B2B2;")           
            self.timer_button.setText('No timer')
            self.timer_button.setFixedSize(QSize(150,60))
            self.timer_button_count = 0
        
        
        
    
    def closeEvent(self):
        self.playlist.songServiceObject.stop()
        self.close()


    def VolumeSliderMovement(self):
        slider_current_value = self.volume_slider.Value() # volume slider position

        # set volume relative to the position

    def next_button_pressed(self):
        self.tn.start(1000)

    def next_button_released(self):
        self.tn.stop()
        if self.next_time_check:
            self.next_time_check = False
        else:
            self.next_time_check = False
            try : 
                self.next_music()
            except Exception as e : 
                self.reset_controls_on_edge_songs()


    # If we reach at the end of the songs 
    def reset_controls_on_edge_songs(self):
        self.position_slider.setValue(0)
        self.timer.stop()
        # self.toggle_music()

    def prev_button_pressed(self):
        self.tp.start(1000)

    def prev_button_released(self):
        self.tp.stop()
        if self.prev_time_check:
            self.prev_time_check = False
        else:
            self.prev_time_check = False
            try : 
                self.prev_music()
            except Exception as e : 
                # Means we are at first or last song 
                self.reset_controls_on_edge_songs()







