#
# Classes for fusing data from multuple sensors
#

from sensor import Sensor

class Averager(Sensor):
    
    def __init__(self, sensor1, sensor2):
        self.sensor1 = sensor1
        self.sensor2 = sensor2
        
    def sample(self):
        return (self.sensor1.sample() + self.sensor2.sample()) / 2