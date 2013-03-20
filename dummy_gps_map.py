#
#
#
#

RESOLUTION_M=1
METERS_PER_DEGREE_LAT = 111000
METERS_PER_DEGREE_LNG = 111000

class DummyGPSMap:
    def __init__(self):
        
        # Open and read the GPS data
        self.lats, self.longs = self.open_and_read_GPS_file('../perception-dummy/gpsdummydata.txt')

        self.compute_bounds()
        self.build_gps_line()
        self.build_maze_data()
        
    def open_and_read_GPS_file(self, fname):
        with open(fname) as f:
            content = f.readlines()

        # pop off the header row (LATITUDE, LONGITUDE)
        if "TUDE" in content[0]:
            content.pop(0);

        lats =[]
        longs=[]

        for coord in content:
            parts = coord.split(' ');
            lats.append(float(parts[0]))
            longs.append(float(parts[1]))

        return lats, longs
        
    def compute_bounds(self):
        self.max_lat = max(self.lats)
        self.min_lat = min(self.lats)
        self.max_lng = max(self.longs)
        self.min_lng = min(self.longs)
        lat_rng = abs(self.max_lat - self.min_lat) * METERS_PER_DEGREE_LAT
        lng_rng = abs(self.max_lng - self.min_lng) * METERS_PER_DEGREE_LNG

        # round to the nearest 100 (quantize)
        self.lat_rng_q = int(round(lat_rng / 100) * 10)
        self.lng_rng_q = int(round(lng_rng / 100) * 10)

        print "Lat min/max/range(m) ", (self.min_lat, self.max_lat, self.lat_rng_q), \
              ", Long min/max/range(m)", (self.min_lng, self.max_lng, self.lng_rng_q)
        
    def get_maze_data(self):
        return self.maze_data
        
    def get_gps_line(self):
        return self.gps_line

    def build_gps_line(self):
        self.gps_line = []
        for lat, lng in zip(self.lats, self.longs):
            lat_i = int((abs(lat - self.min_lat) * METERS_PER_DEGREE_LAT - 1) / 10)
            lng_i = int((abs(lng - self.min_lng) * METERS_PER_DEGREE_LNG - 1) / 10)
            print lng_i, lat_i
            self.gps_line.append((lng_i, lat_i));
        

    def build_maze_data(self):
        # Init the map to all unpassable blocks
        self.maze_data = []
        for i in range(0, self.lat_rng_q):
            self.maze_data.append([])
            for j in range(0, self.lng_rng_q):
                self.maze_data[i].append(1)

        print len(self.maze_data)
        # Clear a path as identified by the lat/long positions from the file
        for lng_i, lat_i in self.gps_line:
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
