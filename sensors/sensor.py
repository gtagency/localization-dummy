#
# A generic base class for sensors.  A sensor class is used
# to model a specific type of sensor, and provide an easy
# API for consumer code.
#
#

class Sensor(object):
    UNKNOWN = -1
    
    def __init__(self, datasource):
        self.datasource = datasource
    
    #
    # Sample the sensor by reading one value
    # from the datasource.
    #
    def sample(self):
        return self.datasource.readOne()