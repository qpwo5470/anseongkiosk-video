# importing vlc module
from tkinter import filedialog
import time
import vlc
from pynput import keyboard



from os import walk
from os.path import join

playlist = []
for (dirpath, dirnames, filenames) in walk('videos'):
    playlist.extend([join(dirpath,filename) for filename in filenames])
    break
print(playlist)


from vlc import Instance


class testVLC:

    def __init__(self, playlist):
        self.list1 = playlist
        self.Player = Instance('--no-video-title-show', '--fullscreen', '--mouse-hide-timeout=0')
        self.addPlaylist()
        self.playPlaylist()
        with keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()

    def on_press(self, key):
        if key == keyboard.Key.space:
            self.nextPlay()
        print('Key %s pressed' % key)

    def on_release(self, key):
        print('Key %s released' % key)
        if key == keyboard.Key.esc:  # esc 키가 입력되면 종료
            print('EXIT')

    def addPlaylist(self):
        self.mediaList = self.Player.media_list_new()
        for music in self.list1:
            self.mediaList.add_media(self.Player.media_new(music))
        self.listPlayer = self.Player.media_list_player_new()
        self.listPlayer.set_media_list(self.mediaList)
        self.listPlayer.set_playback_mode(vlc.PlaybackMode.loop)

    def playPlaylist(self):
        self.listPlayer.play()

    def nextPlay(self):
        self.listPlayer.next()

player = testVLC(playlist)