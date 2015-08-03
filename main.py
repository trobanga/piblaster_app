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

    snd = ObjectProperty(None)
    def __init__(self):
        super(PiblasterApp, self).__init__()
        self.blueberry = BlueberryClient()

    def connect(self, obj):
        if self.blueberry.get_socket_stream('piblaster3000-0'):
            cprint("Successfully connected!")

        pass
        
    def send(self, obj):
        cprint("send, obj")
        print(obj.text)
        # l = Label(text='sent')
        
        self.blueberry.send('hello1')
        self.blueberry.send('hesdo2')
        self.blueberry.send('hello3')


        # self.receive(0)
        
        # t = self.blueberry.receive()
        # cprint("antowort")
        # print t
        # cprint("antowort")
        # l = Label(text=t)
        # self.piblaster.add_widget(l)


        
    def receive(self, obj):
        print time.clock()
        i = 0
        while True:
            i += 1
            t = self.blueberry.receive()
            l = Label(text=t)
            self.piblaster.add_widget(l)
        print time.clock()
        
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


