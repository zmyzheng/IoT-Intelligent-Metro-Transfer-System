from collections import OrderedDict
import re
import ast

class Synthesis:
    def __init__(self):
        self.tripId = None
        self.routeId = None
        self.startDate = None
        self.direction = None
        self.currentStopId = None
        self.currentStopStatus = None
        self.vehicleTimeStamp = None
        self.futureStops = OrderedDict()  # Format {stopId : [arrivalTime,departureTime]}
        self.timeStamp = None

    def constructFromDyDict(self, d):
        self.tripId = d[u'tripId']
        self.routeId = d[u'routeId']
        self.startDate = d[u'startDate']
        self.direction = d[u'direction']
        self.currentStopId = d[u'currentStopId']
        self.currentStopStatus = d[u'currentStopStatus']
        self.vehicleTimeStamp = d[u'vehicleTimeStamp']

        m = re.match(r'^OrderedDict\((.+)\)$', d[u'futureStops'])
        if m:
            self.futureStops = OrderedDict(ast.literal_eval(m.group(1)))
        self.timeStamp = d[u'timestamp']
