import kivy
kivy.require('1.9.0') # replace with your current kivy version !

__version__ = "0.1"

from kivy.lang import Builder
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty

from blueberry_client import BlueberryClient
import time
import threading

class Piblaster(Widget):
    pass


class SendButton(Button):

    def build(self):
    #     pass#super(SendButton, self).__init__()
        print 'hell'
        self.bind(on_release=self.send)
        return self

        
    def send(self, obj):
        cprint("send, obj")
        print(obj.text)
        # self.blueberry.send('Hello')
        

class PiblasterApp(App):
    cmd_send_list = ['MUSIC_DB_VERSION', 'MUSIC_DB',
                     'PLAYLIST', 'CURRENT_SONG', 'STATE',
                     'APPEND_SONG', 'APPEND_ALBUM', 'APPEND_ARTIST', 
                     'PLAY_SONG', 'PLAY_ALBUM', 'PLAY_ARTIST', 
                     'PREPEND_SONG', 'PREPEND_ALBUM', 'PREPEND_ARTIST']
    
    snd = ObjectProperty(None)
    def __init__(self):
        super(PiblasterApp, self).__init__()
        self.music_db_version = 0
        self.music_db_size = 0 # number of chunks to be transmitted
        self.blueberry = BlueberryClient()
        cmd_recv_list = {'ACK': None,
                        'MUSIC_DB_CHUNK': self.recv_music_db_chunk, 'DB_SIZE': self.recv_music_db_size,
                        'DB_PACKET_COUNT': None, 'MUSIC_DB_VERSION': self.recv_music_db_version,
                        'PLAYLIST_CHANGED': None, 'CURRENT_SONG': None, 'STATE': None}

            
    def connect(self, obj):
        if self.blueberry.get_socket_stream('piblaster3000-0'):
            cprint("Successfully connected!")

            
    def recv_music_db_version(self, v):
        if v != self.music_db_version:
            self.music_db_version = v
            self.send('MUSIC_DB')

            
    def recv_music_db_size(s)
        self.music_db_size = s

        
    def send(self, cmd, payload=""):
        pass 
                
        
    def receive(self, obj):
        """
        Checks bt queue for new messages.
        Packets are split into command and payload.
        Corresponding function is called with payload as parameter.
        
        """
        if not self.blueberry.messages.empty():
            # received a new messages
            m = self.blueberry.get()
            cmd, payload = m.split(',' 1)
            if cmd in self.cmd_recv_list:
                self.cmd_recv_list[cmd](payload)
        
        
    def build(self):
        self.piblaster = Piblaster()
        b = Button(text="Sent")
        b.bind(on_release=self.send)
        c = Button(text="Connect")
        c.bind(on_release=self.connect)

        l = BoxLayout()
        l.add_widget(self.piblaster)
        l.add_widget(b)
        l.add_widget(c)
        return l

    
def cprint(s):
    """Print in red"""
    print '\033[31m' + s + '\033[0m'

    
if __name__ == "__main__":
    PiblasterApp().run()


