#
# A generic base class for data sources. A data source provides an API
# into a piece of hardware or software (or storage) that provides sensor
# data.
#
#

from util import raiseNotDefined

class DataSource(object):
    
    def hasNext(self):
        raiseNotDefined()

    def readOne(self):
        raiseNotDefined()

#
# A file based data source.  This assumes readings in order, with a single
# integer per line.  If your data is in a different format, you can supply
# a transformation function to parse and return the data in the correct
# format.
#
class FileDataSource(DataSource):
    
    def __init__(self, filePath, transform=lambda one: int(one)):
        with open(filePath) as f:
            self.content = f.readlines()
        self.transform = transform
        self.index = 0
        self.maxIndex = len(self.content) - 1
    
    def hasNext(self):
        return self.index < self.maxIndex

    def readOne(self):
        one = self.content[self.index]
        self.index += 1

        return self.transform(one)
