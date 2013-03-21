#
# A sensor class for a GPS.
#
#

from sensor import Sensor

class GPS(Sensor):
    
    def __init__(self, datasource):
        Sensor.__init__(self, datasource)

    