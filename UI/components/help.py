from PyQt5.QtWidgets import QWidget , QLabel, QVBoxLayout

class Help(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Shortcut Keys")
        self.label = QLabel()
        self.label.setObjectName('Help_label')
        layout = QVBoxLayout()
        self.label.setText("Play or Pause \t-  Space bar \n\nReduce Volume \t-  Ctrl + Left key \n\nAdd Volume \t-  Ctrl + Right key \n\nRewind \t\t-  A or Left Key \n\nFast forward \t-  D or Right key \n\nPlay previous song \t-  W or Up key \n\nPlay next song \t-  S or Down key")
        layout.addWidget(self.label)
        self.setLayout(layout)
