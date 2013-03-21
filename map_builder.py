#
# A map builder that uses file based sensor data to extract landmarks
# and build a static map.
#

from mapping.landmarkmap import LandmarkMap
from sensors.datasource  import FileDataSource
from sensors.fusion      import Averager
from sensors.gps         import GPS
from sensors.laser       import RawLaserRangeFinder
from sensors.ultrasonic  import RawUltrasonicRangeFinder

import math

METERS_PER_DEGREE_LAT = 111000
METERS_PER_DEGREE_LNG = 111000

gps_ds         = FileDataSource('../perception-dummy/gpsdummydata.txt', \
                                    lambda one: map(float, one.split(' ')))
left_laser_ds  = FileDataSource('../perception-dummy/leftlaserdummydata.txt')
right_laser_ds = FileDataSource('../perception-dummy/rightlaserdummydata.txt')
left_sonar_ds  = FileDataSource('../perception-dummy/leftultrasonicdummydata.txt')
right_sonar_ds = FileDataSource('../perception-dummy/rightultrasonicdummydata.txt')

gps         = GPS(gps_ds)
left_laser  = RawLaserRangeFinder(left_laser_ds,  5.0, 240)
right_laser = RawLaserRangeFinder(right_laser_ds, 5.0, 240)
left_sonar  = RawUltrasonicRangeFinder(left_sonar_ds,  5.0, 240)
right_sonar = RawUltrasonicRangeFinder(right_sonar_ds, 5.0, 240)

left_depth   = Averager(left_laser,  left_sonar)
right_depth  = Averager(right_laser, right_sonar)

theMap = LandmarkMap()

lastlat = None
lastlng = None
while gps_ds.hasNext():
    lat, lng = gps.sample()
    if lastlat == None:
        lastlat = lat
        lastlng = lng
        # burn one depth sample
        right_depth.sample()
        continue
    # compute heading...this is required to make sense of the range finder data
    heading = 180 * math.atan2((lat - lastlat), (lng - lastlng)) / math.pi
    if heading < 0:
        heading = 360 + heading
    #print lastlat, lastlng, lat, lng, lat - lastlat, lng - lastlng, heading
    lastlat = lat
    lastlng = lng

    # take a sample from the right laser range finder, and determine it's lat/long
    # based on the GPS position
    d_right = right_depth.sample()
    if d_right != RawLaserRangeFinder.UNKNOWN and d_right < 2.4:
        angle = heading - 90
        if angle < 0:
            angle = 360 + angle
        angle = 2 * math.pi * angle / 360
        print math.sin(angle), math.cos(angle), angle
        landlat = lat + d_right * math.sin(angle)
        landlng = lng + d_right * math.cos(angle)
        
        print "Landmark!", lat, lng, landlat, landlng, heading, d_right
        theMap.addLandmark((lat, lng))

theMap.save('landmarks.map')
        