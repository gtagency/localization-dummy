#
# A sensor class for ultrasonic range finders (sonar).  These sensors
# are raw sensors with similar characteristics to other range finders.
#
#

from rangefinder import RawRangeFinder

class RawUltrasonicRangeFinder(RawRangeFinder):
    
    def __init__(self, datasource, rangeInMeters, maxVal):
        RawRangeFinder.__init__(self, datasource, rangeInMeters, maxVal)
