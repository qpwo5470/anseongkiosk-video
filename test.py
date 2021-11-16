import sys
from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
import vlc
import os.path


class MainWindow(qtw.QMainWindow):
  def __init__(self, parent=None):

      super().__init__(parent)
      ##Main framwork
      # creating a basic vlc instance
      self.instance = vlc.Instance()
      # creating an empty vlc media player
      self.mediaplayer = self.instance.media_player_new()

      self.createUI()
      self.isPaused = False

  def createUI(self):

      base_widget = qtw.QWidget()
      base_widget.setLayout(qtw.QHBoxLayout())
      notebook = qtw.QVBoxLayout()
      base_widget.layout().addLayout(notebook)
      self.setCentralWidget(base_widget)

      #VideoFrame Loading
      self.videoframe = qtw.QFrame()
      self.videoframe.setMinimumWidth(950)
      self.videoframe.setMinimumHeight(525)
      self.palette = self.videoframe.palette()
      self.palette.setColor (qtg.QPalette.Window,
                             qtg.QColor(0,0,0))
      self.videoframe.setPalette(self.palette)
      self.videoframe.setAutoFillBackground(True)

      #Position Slider
      self.positionslider = qtw.QSlider(qtc.Qt.Horizontal, self)
      self.positionslider.setToolTip("Position")
      self.positionslider.setMaximum(100000.0)
      self.positionslider.setTickPosition(qtw.QSlider.TicksBelow)
      self.positionslider.setTickInterval(2000)
      self.positionslider.sliderMoved.connect(self.setPosition)

      self.hbuttonbox = qtw.QHBoxLayout()
      self.playbutton = qtw.QPushButton("Play")
      self.hbuttonbox.addWidget(self.playbutton)
      self.playbutton.clicked.connect(self.PlayPause)

      #Button Box
      self.stopbutton = qtw.QPushButton("Stop")
      self.hbuttonbox.addWidget(self.stopbutton)
      self.stopbutton.clicked.connect(self.Stop)

      #Volume slider
      self.hbuttonbox.addStretch(1)
      self.volumeslider = qtw.QSlider(qtc.Qt.Horizontal, self)
      self.volumeslider.setMaximum(100)
      self.volumeslider.setValue(self.mediaplayer.audio_get_volume())
      self.volumeslider.setToolTip("Volume")
      self.hbuttonbox.addWidget(self.volumeslider)
      self.volumeslider.valueChanged.connect(self.setVolume)

      notebook.addWidget(self.videoframe)
      notebook.addWidget(self.positionslider)
      notebook.addLayout(self.hbuttonbox)

      #Actions Code
      open1 = qtw.QAction("&Open", self)
      open1.triggered.connect(self.OpenFile)

      exit = qtw.QAction("&Exit", self)
      exit.triggered.connect(sys.exit)


      menubar = self.menuBar()
      filemenu = menubar.addMenu("&File")
      filemenu.addAction(open1)
      filemenu.addSeparator()
      filemenu.addAction(exit)

      self.timer = qtc.QTimer(self)
      self.timer.setInterval(200)
      self.timer.timeout.connect(self.updateUI)

  def PlayPause(self):
      """Toggle play/pause status
      """
      if self.mediaplayer.is_playing():
          self.mediaplayer.pause()
          self.playbutton.setText("Play")
          self.isPaused = True
      else:
          if self.mediaplayer.play() == -1:
              self.OpenFile()
              return
          self.mediaplayer.play()
          self.playbutton.setText("Pause")
          self.timer.start()
          self.isPaused = False

  def PausePlay(self):

      if self.mediaplayer.is_playing():
          self.mediaplayer.pause()
          self.playbutton.setText("Play")
          self.isPaused = True



  def Stop(self):
      """Stop player
      """
      self.mediaplayer.stop()
      self.playbutton.setText("Play")


  def OpenFile(self, filename=None):

      """Open a media file in a MediaPlayer
      """
      if filename is None or filename is False:
          print("Attempt to open up OpenFile")
          filenameraw = qtw.QFileDialog.getOpenFileName(self, "Open File", os.path.expanduser('~'))
          filename = filenameraw[0]
      if not filename:
          return
      # create the media
      if sys.version < '3':
          filename = unicode(filename)

      self.media = self.instance.media_new(filename)
      # put the media in the media player
      self.mediaplayer.set_media(self.media)

      # parse the metadata of the file
      self.media.parse()
      # set the title of the track as window title
      self.setWindowTitle(self.media.get_meta(0))
      # print(vlc.libvlc_media_get_meta(self.media, 6))
      # print(vlc.libvlc_media_get_duration(self.media))
      # the media player has to be 'connected' to the QFrame
      # (otherwise a video would be displayed in it's own window)
      # this is platform specific!
      # you have to give the id of the QFrame (or similar object) to
      # vlc, different platforms have different functions for this
      if sys.platform.startswith('linux'):  # for Linux using the X Server
          self.mediaplayer.set_xwindow(self.videoframe.winId())
      elif sys.platform == "win32":  # for Windows
          self.mediaplayer.set_hwnd(self.videoframe.winId())
      elif sys.platform == "darwin":  # for MacOS
          self.mediaplayer.set_nsobject(int(self.videoframe.winId()))
      self.PlayPause()

  def setVolume(self, Volume):
      """Set the volume  """
      self.mediaplayer.audio_set_volume(Volume)


  def setPosition(self, position):
      """Set the position
      """
      # setting the position to where the slider was dragged
      self.mediaplayer.set_position(position / 100000.0)
      # the vlc MediaPlayer needs a float value between 0 and 1, Qt
      # uses integer variables, so you need a factor; the higher the
      # factor, the more precise are the results
      # (1000 should be enough)

  def updateUI(self):
      """updates the user interface"""
      # setting the slider to the desired position
      self.positionslider.setValue(self.mediaplayer.get_position() * 100000.0)

      if not self.mediaplayer.is_playing():
          # no need to call this function if nothing is played
          self.timer.stop()
          if not self.isPaused:
              # after the video finished, the play button stills shows
              # "Pause", not the desired behavior of a media player
              # this will fix it
              self.Stop()


if __name__ == '__main__':
  app = qtw.QApplication(sys.argv) #it's required to save a referance to MainWindow
  mw = MainWindow()
  mw.show()
  if sys.argv[1:]:
      mw.OpenFile(sys.argv[1])
  sys.exit(app.exec_())
  #if it goes out of scope ,it will be destroyed
