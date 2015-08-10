import kivy
kivy.require('1.9.0') # replace with your current kivy version !

__version__ = "0.1"

from kivy.lang import Builder
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListView
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty

from blueberry_client import BlueberryClient
import time
import threading
import json


# debug print
def cprint(s):
    """Print in red"""
    print '\033[31m' + s + '\033[0m'


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


class SongList(ListView):
        def __init__(self):
            superr(MainView, self).__init__()
            
        def update(self, l):
            item_strings = l
            

class PiblasterApp(App):
    cmd_send_list = ['MUSIC_DB_VERSION', 'MUSIC_DB',
                     'PLAYLIST', 'CURRENT_SONG', 'STATE',
                     'APPEND_SONG', 'APPEND_ALBUM', 'APPEND_ARTIST', 
                     'PLAY_SONG', 'PLAY_ALBUM', 'PLAY_ARTIST', 
                     'PREPEND_SONG', 'PREPEND_ALBUM', 'PREPEND_ARTIST']

         
    snd = ObjectProperty(None)
    def __init__(self):
        super(PiblasterApp, self).__init__()

        # debug
        cprint("START!")
        
        self.music_db_version = -1
        self.music_db_size = 0 # number of chunks to be transmitted
        self.music_db_chunks = {}
        self.blueberry = BlueberryClient()
        self.cmd_recv_list = {'ACK': None,
                              'MUSIC_DB_CHUNK': self.recv_music_db_chunk, 'DB_SIZE': self.recv_music_db_size,
                              'DB_PACKET_COUNT': None, 'MUSIC_DB_VERSION': self.recv_music_db_version,
                              'PLAYLIST_CHANGED': None, 'CURRENT_SONG': None, 'STATE': None,
                              'MUSIC_DB_SEND_COMPLETE': self.music_db_send_complete}
            
    def connect(self, obj):
        if self.blueberry.get_socket_stream('piblaster3000-0'):
            cprint("Successfully connected!")
            self.receive(daemon=True)

            
    def ask_music_db_version(self, *args):
        self.send('MUSIC_DB_VERSION')

        
    def recv_music_db_version(self, v):
        cprint('Version: {}'.format(v))
        if v != self.music_db_version:
            self.music_db_version = v
            self.music_db_chunks = {}
            self.send('MUSIC_DB')

            
    def recv_music_db_size(self, s):
        cprint('recv_music_db_size: {}'.format(s))
        self.music_db_size = int(s)


    def recv_music_db_chunk(self, s):
        n, c = s.split(',', 1)  # n: chunk number, c: chunk
        self.music_db_chunks[n] = c

        
    def music_db_send_complete(self, s):
        if len(self.music_db_chunks) == self.music_db_size:
            music_db_json = ""
            for i in sorted(self.music_db_chunks.iterkeys()):
                music_db_json += self.music_db_chunks[i]

            print music_db_json
            # TODO: recreate ListView
        else:
            missing = list(set(range(self.music_db_size)) - set(self.music_db_chunks.keys()))
            self.send('MUSIC_DB', json.dumps(missing))
                            
            
    def send(self, cmd, payload=""):
        """
        Sends cmd and payload via bluetooth.
        """
        if self.blueberry.connected and cmd in self.cmd_send_list:
            self.blueberry.send("{},{}".format(cmd, payload))
            return True
        else:
            return False


    def send_button(self, obj):
        self.ask_music_db_version()
 
        
    def receive(self, daemon=False):
        """
        Checks bt queue for new messages.
        Packets are split into command and payload.
        Corresponding function is called with payload as parameter.
        
        """
        if daemon:
            cprint('Start receive daemon')
            t = threading.Thread(target=self.receive)
            t.daemon = True
            t.start()
        else:
            while True:
                if not self.blueberry.messages.empty():
                    # received a new messages
                    m = self.blueberry.messages.get()
                    cmd, payload = m.split(',', 1)
                    if cmd in self.cmd_recv_list:
                        self.cmd_recv_list[cmd](payload)
        
        
    def build(self):
        self.piblaster = Piblaster()
        b = Button(text="Sent")
        b.bind(on_release=self.send_button)
        c = Button(text="Connect")
        c.bind(on_release=self.connect)

        l = BoxLayout()
        l.add_widget(self.piblaster)
        l.add_widget(b)
        l.add_widget(c)
        return l

    
    
if __name__ == "__main__":
    PiblasterApp().run()


