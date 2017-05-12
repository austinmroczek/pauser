class Pauser:
    
    """Pauser class"""

# this class controls all playback devices



    def __init__(self):
        import log
        self.myLog = log.Log('device.log')

        self.paused = False  # current system pause status
        self.devices = []
        self.address = "127.0.0.1"
        self.get_ip_address()
        self.findDevices()

# from https://stackoverflow.com/questions/24196932/how-can-i-get-the-ip-address-of-eth0-in-python
    def get_ip_address(self):
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.address = s.getsockname()[0]
        self.myLog.add("Pauser is using IP address " + self.address)

    def findDevices(self):
        #TODO: find all devices and set them up properly

        #HACK
        import pauserDeviceRoku3
        tempDevice = pauserDeviceRoku3.PauserDeviceRoku3('Roku3test1')
        tempDevice.setDeviceAddress('192.168.2.14')
        self.devices.append(tempDevice)
        tempDevice = pauserDeviceRoku3.PauserDeviceRoku3('Roku3test2')
        tempDevice.setDeviceAddress('192.168.2.62')
        self.devices.append(tempDevice)
        tempDevice = pauserDeviceRoku3.PauserDeviceRoku3('Roku3test3')
        tempDevice.setDeviceAddress('192.168.2.88')
        self.devices.append(tempDevice)

        
        #.62 .88

    def pause(self):
        for x in self.devices:
            x.pause()
        self.paused = True

    def play(self):
        for x in self.devices:
            x.play()
        self.paused = False

    def backup(self):
        for x in self.devices:
            x.backup()
        self.paused = False

    def isPaused(self):
        # return if we are paused or not
        return self.paused
