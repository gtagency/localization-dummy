#
# A map builder that uses file based sensor data to extract landmarks
# and build a static map.
#

from mapping.landmarkmap   import LandmarkMap
from mapping.pointresolver import PointResolver
from sensors.datasource    import FileDataSource
from sensors.fusion        import Averager
from sensors.gps           import GPS
from sensors.laser         import RawLaserRangeFinder
from sensors.ultrasonic    import RawUltrasonicRangeFinder

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

theMap   = LandmarkMap()
resolver = PointResolver()

while gps_ds.hasNext():
    lat, lng = gps.sample()
    
    resolver.update(lat, lng)
    
    if resolver.heading == None:
        # burn one depth sample
        right_depth.sample()
        continue
        
    
    # take a sample from the right laser range finder, and determine it's lat/long
    # based on the GPS position
    d_right = right_depth.sample()
    if d_right != RawLaserRangeFinder.UNKNOWN and d_right < 2.4:
        landlat, landlng = resolver.resolve(-90, d_right)
        
        print "Landmark!", lat, lng, landlat, landlng, resolver.heading, d_right
        theMap.addLandmark((landlat, landlng))

theMap.save('landmarks.map')
        