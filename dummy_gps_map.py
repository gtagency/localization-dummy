#
#
#
#

RESOLUTION_M=1
METERS_PER_DEGREE_LAT = 111000
METERS_PER_DEGREE_LNG = 111000
SCALE = 1.0/10.0

from sensors.datasource import FileDataSource
from sensors.gps import GPS

class DummyGPSMap:
    def __init__(self):
        
        # Open and read the GPS data
        self.lats, self.longs = self.open_and_read_GPS_file('../perception-dummy/gpsdummydata.txt')

        self.compute_bounds()
        self.build_gps_pts()
        self.build_maze_data()
        self.build_center_line()
        
    def open_and_read_GPS_file(self, fname):
        ds  = FileDataSource(fname, lambda one: map(float, one.split(' ')))
        gps = GPS(ds)

        lats =[]
        longs=[]

        while ds.hasNext():
            pt = gps.sample();
            lats.append(pt[0])
            longs.append(pt[1])

        return lats, longs
        
    def compute_bounds(self):
        self.max_lat = max(self.lats)
        self.min_lat = min(self.lats)
        self.max_lng = max(self.longs)
        self.min_lng = min(self.longs)
        lat_rng = abs(self.max_lat - self.min_lat) * METERS_PER_DEGREE_LAT
        lng_rng = abs(self.max_lng - self.min_lng) * METERS_PER_DEGREE_LNG

        # round to the nearest 100 (quantize)
        self.lat_rng_q = int(round(lat_rng / 100) * (100 * SCALE))
        self.lng_rng_q = int(round(lng_rng / 100) * (100 * SCALE))

        print "Lat min/max/range(m) ", (self.min_lat, self.max_lat, self.lat_rng_q), \
              ", Long min/max/range(m)", (self.min_lng, self.max_lng, self.lng_rng_q)
        
    def get_maze_data(self):
        return self.maze_data
        
    def get_center_line(self):
        return self.center_line

    def build_gps_pts(self):
        self.gps_pts = []
        
        for lat, lng in zip(self.lats, self.longs):
            lat_i = int((abs(lat - self.min_lat) * METERS_PER_DEGREE_LAT - 1) * SCALE)
            lng_i = int((abs(lng - self.min_lng) * METERS_PER_DEGREE_LNG - 1) * SCALE)
            print lng_i, lat_i
            self.gps_pts.append((lng_i, lat_i));
        
    # Build a center line based on the path created in build_maze_data
    def build_center_line(self):
        self.center_line = []
        last_avg = None
        for j in range(0, self.lng_rng_q):
            path_start = None
            for i in range(0, self.lat_rng_q):
                print j, i
                if path_start == None and self.maze_data[i][j] == 0:
                    path_start = i
                if path_start != None and self.maze_data[i][j] != 0:
                    print "Found point", path_start, i
                    avg_x = (i - path_start) / 2
                    print "Appending point ", j, path_start + avg_x
                    self.center_line.append((j, path_start + avg_x))
                    path_start = None
            if path_start != None:
                print "Found point", path_start, self.lat_rng_q
                avg_x = (self.lat_rng_q - path_start) / 2
                print "Appending point ", j, path_start + avg_x
                self.center_line.append((j, path_start + avg_x))
                path_start = None
#        for pt in self.gps_pts:
 #           if last_avg == None:
  #              self.center_line.append(pt)
   #             last_avg = pt
    #            continue
     #       avg = ((pt[0] + last_avg[0]) / 2, (pt[1] + last_avg[1]) / 2)
      #      self.center_line.append(avg)
       #     last_avg = avg
        
        
    def build_maze_data(self):
        # Init the map to all unpassable blocks
        self.maze_data = []
        for i in range(0, self.lat_rng_q):
            self.maze_data.append([])
            for j in range(0, self.lng_rng_q):
                self.maze_data[i].append(1)

        print len(self.maze_data)
        # Clear a path as identified by the lat/long positions from the file
        for lng_i, lat_i in self.gps_pts:
            self.maze_data[lat_i][lng_i] = 0
            # Clear a square to the north, south, east, and west of the position
            if lat_i > 0:
                self.maze_data[lat_i - 1][lng_i] = 0
            if lat_i < (self.lat_rng_q - 1):
                self.maze_data[lat_i + 1][lng_i] = 0
            if lng_i > 0:
                self.maze_data[lat_i][lng_i - 1] = 0
            if lng_i < (self.lng_rng_q - 1):
                self.maze_data[lat_i][lng_i + 1] = 0

        for i in range(0, self.lat_rng_q - 1):
            self.maze_data[i] = tuple(self.maze_data[i])
        self.maze_data = tuple(self.maze_data)
