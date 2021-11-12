from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QMainWindow, QWidget, QPushButton, QApplication,
                             QLabel, QFileDialog, QStyle, QVBoxLayout, QDesktopWidget, QFrame)
import sys


class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Video Player")
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.frame = QFrame(self)
        self.setCentralWidget(self.frame)
        self.frame.setFrameShape(QFrame.NoFrame)


        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget(self.frame)
        videoWidget.setGeometry(0, 0, 1080, 3840)
        self.openFile()
        self.play()

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.move(0, 0)

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                                                  QDir.homePath())

        if fileName != '':
            self.mediaPlayer.setMedia(
                QMediaContent(QUrl.fromLocalFile(fileName)))
            print('set')

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            print('paused')
        else:
            self.mediaPlayer.play()
            print('playing')


app = QApplication(sys.argv)
videoplayer = VideoPlayer()
videoplayer.setFixedSize(1080, 3840)
videoplayer.show()
sys.exit(app.exec_())
