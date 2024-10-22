
class SignalProperties:
    def __init__(self, signalName, signalPath, dataPoints):
        self.name = signalName
        self.location = signalPath
        # self.time = dataPoints[0]
        # self.amplitude = dataPoints[1]
        self.data = dataPoints
        self.lineWidth = 20
        self.color = "color"
        self.speed = "speed"
        self.isLive = False
        self.isOnChannel1 = True
        self.isOnChannel2 = False

        self.colorinChannel1 = "#EFEFEF"
        self.colorinChannel2 = "#EFEFEF"
        self.isShown =True

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