#
# The driver for the car system (no pun intended).  This class
# instantiates and reads from the sensors, and localizes the robot
# based on sensor input.  Future versions will also invoke the
# path planning algorithms and issue commands to the control system.
#

from mapping.landmarkmap import LandmarkMap

from sensors.datasource import FileDataSource
from sensors.fusion     import Averager
from sensors.gps        import GPS
from sensors.laser      import RawLaserRangeFinder
from sensors.ultrasonic import RawUltrasonicRangeFinder

gps_ds         = FileDataSource('../perception-dummy/gpsdummydata.txt', \
                                    lambda one: map(float, one.split(' ')))
left_laser_ds  = FileDataSource('../perception-dummy/leftlaserdummydata.txt')
right_laser_ds = FileDataSource('../perception-dummy/rightlaserdummydata.txt')

gps         = GPS(gps_ds)
left_laser  = RawLaserRangeFinder(left_laser_ds,  5.0, 240)
right_laser = RawLaserRangeFinder(right_laser_ds, 5.0, 240)
left_sonar  = RawUltrasonicRangeFinder(left_laser_ds,  5.0, 240)
right_sonar = RawUltrasonicRangeFinder(right_laser_ds, 5.0, 240)

left_depth   = Averager(left_laser,  left_sonar)
right_depth  = Averager(right_laser, right_sonar)

while gps_ds.hasNext():
    lat, lng    = gps.sample()
#    depth_l_left  = left_laser.sample()
 #   depth_l_right = right_laser.sample()
  #  depth_s_left  = left_laser.sample()
   # depth_s_right = right_laser.sample()
    #print depth_l_left, depth_l_right
    #print depth_s_left, depth_s_right
    # Fuse the depth sensors together..simple average for now
    depth_left  = left_depth.sample()
    depth_right = right_depth.sample()
    print "GPS: {0}, {1}, Left Depth: {2}m, Right Depth: {3}m".format(lat, lng, depth_left, depth_right)
    raw_input("Press ENTER to sample")
