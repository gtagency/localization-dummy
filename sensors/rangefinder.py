#
# A set of generic classes for range finders.  These can be used
# as is, or extended for specific types of range finders.
#
# Range finders can be grouped into two different types:
#   Calibrated range finders expect the datasource to report
#   real distances.  This may require calibration on the hardware.
#
#   Raw range finders expect the data source to report a raw
#   reading, which will be scaled based on the range of the
#   device.  Raw range finders can also threshold the data
#   and report UNKNOWN results if the data is outside a certain
#   range of values
#

from sensor import Sensor

class CalibratedRangeFinder(Sensor):
    def __init__(self, datasource):
        Sensor.__init(self, datasource)

class RawRangeFinder(Sensor):
    
    def __init__(self, datasource, rangeInMeters, maxVal):
        Sensor.__init__(self, datasource)
        self.rangeInMeters = rangeInMeters
        self.maxVal        = maxVal
        
    # 
    # Sample from the underlying sensor, and scale
    # the datapoint based on the sensor range.
    #
    def sample(self):
        s = Sensor.sample(self)
        # Exceeded the max value...probably out of range.
        if s > self.maxVal:
            ret = Sensor.UNKNOWN
        else:
            ret = s * self.rangeInMeters / self.maxVal
        
        return ret
