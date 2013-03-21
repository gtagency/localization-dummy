#
# Sensor classes for single point (1D) Laser Range Finders.
# This module supports raw and calibrated laser range
# finders.
#
# It does not yet support 2D sweeping range finders.
#
#

from rangefinder import CalibratedRangeFinder
from rangefinder import RawRangeFinder

class CalibratedLaserRangeFinder(CalibratedRangeFinder):
    def __init__(self, datasource):
        Sensor.__init__(self, datasource)


    
class RawLaserRangeFinder(RawRangeFinder):
    
    def __init__(self, datasource, rangeInMeters, maxVal):
        RawRangeFinder.__init__(self, datasource, rangeInMeters, maxVal)
