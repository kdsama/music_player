
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PyQt5.QtWidgets import QGridLayout, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QSize

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()

        #  Initialize all widgets
        self.setWindowTitle("Music Player")
        self.Image = QLabel('Image')
        self.MusicTitle = QLabel("Music Title")
        self.PlayStopButton = QPushButton("Play")
        self.ForwardButton = QPushButton("Forward")
        self.BackwardButton = QPushButton("Backword")
        layout = QGridLayout()

        #sets the minsize of the mainwindow
        self.setMinimumSize(QSize(400, 300))

        
        
        # Adding Widgets to gridlayout
        #Image.setPixmap(QPixmap())
        layout.addWidget(self.Image, 0, 1)
        layout.addWidget(self.MusicTitle, 1, 0)
        layout.addWidget(self.BackwardButton, 2, 0)
        layout.addWidget(self.PlayStopButton, 2, 1)
        layout.addWidget(self.ForwardButton, 2, 3)
        

        
        #dummy widget to the layout
        widget = QWidget()
        widget.setLayout(layout)

        #fitting the widget to the mainwindow
        self.setCentralWidget(widget)

        #connects button to corresponding function
        self.PlayStopButton.clicked.connect(self.PlayMusic)
        self.ForwardButton.clicked.connect(self.GoForward)
        self.BackwardButton.clicked.connect(self.GoBackward)

    # function for when Play/Stop button is clicked
    def PlayMusic(self):
        t = self.PlayStopButton.text()
        if t == "Play" :
            self.PlayStopButton.setText("Stop")
        else :
            self.PlayStopButton.setText("Play")

    # function for when Forward button is clicked
    def GoForward(self):
        pass

    # function for when Backward button is clicked
    def GoBackward(self):
        pass


app = QApplication([])

window = MainWindow()
window.show()

app.exec_()