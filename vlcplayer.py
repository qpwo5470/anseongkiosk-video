# importing vlc module
from tkinter import filedialog
import time
import vlc
import wx
from pynput import keyboard



from os import walk
from os.path import join

playlist = []
for (dirpath, dirnames, filenames) in walk('/home/linaro/videos'):
    playlist.extend([join(dirpath,filename) for filename in filenames])
    break
print(playlist)


from vlc import Instance


class testVLC(wx.Frame):

    def __init__(self, playlist):
        wx.Frame.__init__(self, None, -1, "Video Frame WxPython", size=(500, 400))
        self.panel = wx.Panel(self, id=-1, pos=(10, 10), size=(470, 300))
        self.panel.SetBackgroundColour(wx.BLACK)
        self.Show()
        self.list1 = playlist
        vlc_options = '--no-xlib --quiet --mouse-hide-timeout=0'
        self.Player = Instance(vlc_options)
        self.addPlaylist()
        self.playPlaylist()
        with keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()

    def on_press(self, key):
        if key == keyboard.Key.space:
            self.nextPlay()

    def on_release(self, key):
        if key == keyboard.Key.esc:  # esc 키가 입력되면 종료
            print('EXIT')

    def addPlaylist(self):
        self.mediaList = self.Player.media_list_new()
        for music in self.list1:
            self.mediaList.add_media(self.Player.media_new(music))
        self.listPlayer = self.Player.media_list_player_new()
        xid = self.panel.GetHandle()
        self.listPlayer.get_media_player().set_xwindow(xid)
        self.listPlayer.set_media_list(self.mediaList)
        self.listPlayer.set_playback_mode(vlc.PlaybackMode.loop)

    def playPlaylist(self):
        self.listPlayer.play()

    def nextPlay(self):
        self.listPlayer.next()

app = wx.App()
frame = testVLC(playlist)
app.MainLoop()