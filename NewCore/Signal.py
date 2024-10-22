
class SignalProperties:
    def __init__(self, signalName, signalPath, dataPoints, channel):
        self.name = signalName
        self.location = signalPath
        self.data = dataPoints
        self.lineWidth = 20
        self.color = "color"
        self.speed = "speed"
        self.isLive = False
        self.isOnChannel1 = False
        self.isOnChannel2 = False

        self.update_channel(channel)

        self.colorinChannel1 = "#EFEFEF"
        self.colorinChannel2 = "#EFEFEF"
        self.isShown =True

    # Method to update channel
    def update_channel(self, channel):
        if channel == 1:
            self.isOnChannel1 = True
            self.isOnChannel2 = False
        elif channel == 2:
            self.isOnChannel1 = False
            self.isOnChannel2 = True
        else:
            print("Invalid channel! Use 1 or 2.")

    # color
    def setColor(self, color):
        self.color = color
    
    def getColor(self):
        return self.color
    
    # speed
    def setSpeed(self, speed):
        self.speed = speed
    
    def getSpeed(self):
        return self.speed
    
    # width
    def setWidth(self, width):
        self.lineWidth = width
    
    def getWidth(self):
        return self.lineWidth