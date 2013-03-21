
import math

METERS_PER_DEGREE_LAT = 111000
METERS_PER_DEGREE_LNG = 111000

def round_to_n(x, n):
    format = "%." + str(n-1) + "e"
    as_string = format % x
    return float(as_string)

class PointResolver(object):
    
    def __init__(self):
        self.lat = None
        self.lng = None
        self.lastlat = None
        self.lastlng = None
        self.heading = None

    def update(self, lat, lng):
        self.lat = lat
        self.lng = lng
        self.updateHeading()
    
    def updateHeading(self):
        if self.lastlat != None:
            # compute heading...this is required to make sense of the range finder data
            self.heading = 180 * math.atan2((self.lat - self.lastlat), (self.lng - self.lastlng)) / math.pi
            if self.heading < 0:
                self.heading = 360 + self.heading
                #print lastlat, lastlng, lat, lng, lat - lastlat, lng - lastlng, heading
        self.lastlat = self.lat
        self.lastlng = self.lng
        
    def resolve(self, relAngle, depth):
        angle = self.heading + relAngle
        if angle < 0:
            angle = 360 + angle
        angle = 2 * math.pi * angle / 360
        print math.sin(angle), math.cos(angle), angle
        # kind of a hack..we lose precision when writing to a file
        return (round_to_n(self.lat + (depth * math.sin(angle)) / METERS_PER_DEGREE_LAT, 12), \
                round_to_n(self.lng + (depth * math.cos(angle)) / METERS_PER_DEGREE_LNG, 12))