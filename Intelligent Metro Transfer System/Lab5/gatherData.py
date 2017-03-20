import time, csv, sys
from pytz import timezone
from datetime import datetime, date

sys.path.append('../utils')
import mtaUpdates

# This script should be run seperately before we start using the application
# Purpose of this script is to gather enough data to build a training model for Amazon machine learning
# Each time you run the script it gathers data from the feed and writes to a file
# You can specify how many iterations you want the code to run. Default is 50
# This program only collects data. Sometimes you get multiple entries for the same tripId. we can timestamp the 
# entry so that when we clean up data we use the latest entry

# Change DAY to the day given in the feed
DAY = datetime.today().strftime("%A")
TIMEZONE = timezone('America/New_York')

global ITERATIONS

# Default number of iterations
ITERATIONS = 50

#################################################################
####### Note you MAY add more datafields if you see fit #########
#################################################################

# column headers for the csv file
columns = ['timestamp', 'tripId', 'route', 'day', 'timeToReachExpressStation', 'timeToReachDestination']

def main(filename):
    newmat = mtaUpdates.mtaUpdates('49366f59360e776881a0172d90ed32ee')
    tripUpdates = newmat.getTripUpdates()
    print len(tripUpdates)

    data = []
    for tripUpdate in tripUpdates:
        if '120S' in tripUpdate.futureStops and '127S' in tripUpdate.futureStops:
            data.append([
                str(int((datetime.fromtimestamp(tripUpdate.timeStamp)
                            - datetime(date.today().year, date.today().month, date.today().day, 0, 0)
                            ).total_seconds() // 60) - 300),
                tripUpdate.tripId.encode('utf-8'),
                tripUpdate.routeId.encode('utf-8'),
                datetime.now().strftime("%A"),
                str(tripUpdate.futureStops['120S'][0]),
                str(tripUpdate.futureStops['127S'][0]),
            ])

    with open('rawdata/'+'raw'+filename+'.csv' ,'a') as file:
        for d in data:
            line = ','.join(d)
            file.write(line)
            file.write('\n')





if __name__ == '__main__':
    fileName = 'Sunday'
    with open('rawdata/'+'raw'+fileName+'.csv' ,'w') as file:
        file.write(','.join(columns))
        file.write('\n')
    while True:
        main(fileName)
        time.sleep(10)

