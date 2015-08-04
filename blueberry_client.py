from jnius import autoclass

from Queue import Queue
import threading

class BlueberryClient(object):

    def __init__(self): 
        self.BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
        self.BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
        self.BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
        self.UUID = autoclass('java.util.UUID')

        self.recv_stream = None
        self.send_stream = None
        self.connected = False

        self.cur_msg = ""
        self.messages = Queue()
    
        
    def get_socket_stream(self, name):
        """Connect to name. If successful, self.recv_stream and self.send_stream are set."""
        self.cprint( '========================================================================================')
        self.cprint( name)
     
        paired_devices = self.BluetoothAdapter.getDefaultAdapter().getBondedDevices().toArray()
        self.cprint( '========================================================================================')
        socket = None
        for device in paired_devices:
            if device.getName() == name:

                self.cprint( 'Found ' + name)
                self.cprint( 'UUIDs')
                for u in device.getUuids():
                    self.cprint( u.getUuid().toString())
            
            
                socket = device.createRfcommSocketToServiceRecord(
                self.UUID.fromString("00001101-0000-1000-8000-00805F9B34FB"))

                self.cprint('socket {}'.format(socket))
                self.recv_stream = socket.getInputStream()
                self.send_stream = socket.getOutputStream()
                break


        rd = socket.getRemoteDevice()
        print rd.getName()
        print rd.getType()
        print rd.toString()
        print rd.getAddress()
        print rd.getBluetoothClass().toString()

        try:
            self.cprint('connect')
            socket.connect()
            self.cprint('connected')
            print self.recv_stream.available()
            print self.recv_stream.markSupported()
            self.connected = True
            self.receive(True)
        except Exception as e:
            self.cprint('connect failed')
            print(e)
            self.recv_stream = None
            self.send_stream = None
            self.connected = False
            
        return self.connected

    def cprint(self, s):
        """Print in red"""
        print '\033[31m' + s + '\033[0m'

                 
    def send(self, cmd):
        self.send_stream.write('{}'.format(cmd))
        self.send_stream.flush()


    def receive(self, daemon=False, eol='\n'):
        """Waits for message and saves it in self.messages"""
        if daemon:
            t = threading.Thread(target=self.receive)
            t.daemon = True
            t.start()
        else:
            while self.connected:
                try:
                    m = unichr(self.recv_stream.read())
                    if m == eol:
                        self.messages.put(msg)
                        msg = ""
                    else:
                        msg += m
                except Exception as e:
                    print e
        


