#
# Classes for fusing data from multuple sensors
#

class LandmarkMap(object):
    
    def __init__(self):
        self.landmarks = []
    
    def addLandmark(self, pt):
        self.landmarks.append(pt)

    def isLandmark(self, pt):
        return pt in self.landmarks

    def load(self, mapFile):
        with open(mapFile) as f:
            content = f.readlines()
        
        for ptStr in content:
            self.landmarks.append(tuple(map(float, ptStr.split(','))))
        
    def save(self, mapFile):
        with open(mapFile, 'w') as f:
            for pt in self.landmarks:
                f.write("{0},{1}\n".format(*pt))
    