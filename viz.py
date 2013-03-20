

from draw import Maze
from dummy_gps_map import DummyGPSMap
import time

"""
# Smaller maze

maze_data = ( ( 2, 0, 1, 0, 0 ),
              ( 0, 0, 0, 0, 1 ),
              ( 1, 1, 1, 0, 0 ),
              ( 1, 0, 0, 0, 0 ),
              ( 0, 0, 2, 0, 1 ))
"""

# 0 - empty square
# 1 - occupied square
# 2 - occupied square with a beacon at each corner, detectable by the robot

maze_data = ( ( 1, 1, 0, 0, 2, 0, 0, 0, 0, 1 ),
              ( 1, 2, 0, 0, 1, 1, 0, 0, 0, 0 ),
              ( 0, 1, 1, 0, 0, 0, 0, 1, 0, 1 ),
              ( 0, 0, 0, 0, 1, 0, 0, 1, 1, 2 ),
              ( 1, 1, 0, 1, 1, 2, 0, 0, 1, 0 ),
              ( 1, 1, 1, 0, 1, 1, 1, 0, 2, 0 ),
              ( 2, 0, 0, 0, 0, 0, 0, 0, 0, 0 ),
              ( 1, 2, 0, 1, 1, 1, 1, 0, 0, 0 ),
              ( 0, 0, 0, 0, 1, 0, 0, 0, 1, 0 ),
              ( 0, 0, 1, 0, 0, 2, 1, 1, 1, 0 ))


print 'Creating world map'
world_map = DummyGPSMap()

print 'Creating world'
world = Maze(world_map.get_maze_data())

print 'Drawing world'
world.draw()

print 'Showing the GPS path'
world.show_path(world_map.get_gps_line())

#print 'Reading sensor information'

#print 'Showing laser bounds'


raw_input("Press ENTER to exit")

    
