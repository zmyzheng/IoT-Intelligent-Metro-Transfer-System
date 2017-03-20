import urllib2,contextlib
from datetime import datetime
from collections import OrderedDict
import Synthesis
from pytz import timezone
import gtfs_realtime_pb2
import google.protobuf

import vehicle, alert, tripupdate

class mtaUpdates(object):

    # Do not change Timezone
    TIMEZONE = timezone('America/New_York')
    
    # feed url depends on the routes to which you want updates
    # here we are using feed 1 , which has lines 1,2,3,4,5,6,S
    # While initializing we can read the API Key and add it to the url
    feedurl = 'http://datamine.mta.info/mta_esi.php?feed_id=1&key='
    
    VCS = {0:"INCOMING_AT", 1:"STOPPED_AT", 2:"IN_TRANSIT_TO"}
    tripUpdates = []

    updates = []
    alerts = []
    vehicles = []

    def __init__(self,apikey):
        self.feedurl = self.feedurl + apikey
        self.tripUpdates = []

        self.updates = []
        self.alerts = []
        self.vehicles = []

    # Method to get trip updates from mta real time feed
    def getTripUpdates(self):
        feed = gtfs_realtime_pb2.FeedMessage()
        try:
            with contextlib.closing(urllib2.urlopen(self.feedurl)) as response:
                d = feed.ParseFromString(response.read())
        except (urllib2.URLError, google.protobuf.message.DecodeError) as e:
            print "Error while connecting to mta server " +str(e)

        timestamp = feed.header.timestamp
        nytime = datetime.fromtimestamp(timestamp, self.TIMEZONE)
        print nytime

        for entity in feed.entity:
            # Trip update represents a change in timetable
            if entity.trip_update and entity.trip_update.trip.trip_id:
                update = tripupdate.tripupdate()
                # trip id
                update.tripId = entity.trip_update.trip.trip_id
                # routeId
                update.routeId = entity.trip_update.trip.route_id
                # startDate
                update.startDate = entity.trip_update.trip.start_date
                # direction
                if '..' in update.tripId:
                    update.direction = entity.trip_update.trip.trip_id.split('..')[1][0]
                elif '.' in update.tripId:
                    update.direction = entity.trip_update.trip.trip_id.split('.')[1][0]
                else:
                    pass
                # futureStopData
                # {stopId : [arrivalTime,departureTime]}
                for stop in entity.trip_update.stop_time_update :
                    update.futureStops[stop.stop_id] = [stop.arrival.time, stop.departure.time]
                self.updates.append(update)

            if entity.vehicle and entity.vehicle.trip.trip_id:
                v = vehicle.vehicle()
                # trip id
                v.trip_id = entity.vehicle.trip.trip_id
                # currentStopNumber
                v.currentStopId = entity.vehicle.current_stop_sequence
                # stop id
                v.currentStopId = entity.vehicle.stop_id
                # time stamp
                v.timestamp = entity.vehicle.timestamp
                # currentStopStatus
                v.currentStopStatus = entity.vehicle.current_status

                self.vehicles.append(v)

            if entity.alert.header_text.translation:
                a = alert.alert()
                # alert msg
                for msg in entity.alert.header_text.translation:
                    if a.alertMessage is None:
                        a.alertMessage = msg.text
                    else:
                        a.alertMessage += msg.text
                # route_id and trip id
                for informed_one in entity.alert.informed_entity:
                    a.tripId.append(informed_one.trip.trip_id)
                    a.routeId[informed_one.trip.trip_id] = informed_one.trip.route_id
                self.alerts.append(a)

        for update in self.updates:
            syn = Synthesis.Synthesis()
            syn.tripId = update.tripId
            syn.routeId = update.routeId
            syn.startDate = update.startDate
            syn.direction = update.direction
            syn.futureStops = update.futureStops
            syn.timeStamp = timestamp
            # join two list
            for v in self.vehicles:
                if syn.tripId == v.trip_id:
                    syn.currentStopId = v.currentStopId
                    syn.currentStopStatus = v.currentStopStatus
                    syn.vehicleTimeStamp = v.timestamp
            self.tripUpdates.append(syn)

        return self.tripUpdates
# END OF getTripUpdates method


if __name__ == '__main__':
    mu = mtaUpdates("49366f59360e776881a0172d90ed32ee")
    x = mu.getTripUpdates()
    print len(x)