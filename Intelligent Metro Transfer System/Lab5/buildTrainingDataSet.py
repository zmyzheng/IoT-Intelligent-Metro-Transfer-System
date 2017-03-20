## This program is used to clean out the data from the csv that you collected.
## It aims at removing duplicate entries and extracting any further insights 
## that the author(s) of the code may see fit

## Usage (for file as is currently): python buildTrainingDataSet.py <filename of file from part 1>

import sys

# Pandas is a python library used for data analysis
import pandas
import numpy
from pandas import read_csv
from pytz import timezone
from datetime import datetime
from os import listdir
from os.path import isfile, join

TIMEZONE = timezone('America/New_York')


def main(mypath):

    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    finalAns = []
    for file in onlyfiles:
        if file == ".DS_Store":
            continue
        rawData = read_csv(join(mypath, file),  encoding="utf-8")
        grouped =  rawData.groupby('timestamp')

        weekdayOrNot = 1
        if rawData.day[0] == 'Saturday':
            weekdayOrNot = 0

        for groupIdx in grouped.groups:
            local = []
            express = []

            for idx in grouped.groups[groupIdx]:
                if rawData.route[idx] == 1:
                    local.append(idx)
                elif rawData.route[idx] == 2 or rawData.route[idx] == 3:
                    express.append(idx)

            minLocalIdx = local[0]
            minLocalToExTime = rawData.timeToReachExpressStation[minLocalIdx]
            for idx in local:
                if rawData.timeToReachExpressStation[idx] <rawData.timeToReachExpressStation[minLocalIdx]:
                    minLocalIdx = idx
                    minLocalToExTime = rawData.timeToReachExpressStation[idx]

            possible = []
            for idx in express:
                if rawData.timeToReachExpressStation[idx] > minLocalToExTime:
                    possible.append(idx)


            minExAfterMinLocalIdx = possible[0]
            minExToExtime = None
            for idx in possible:
                if rawData.timeToReachExpressStation[idx] < rawData.timeToReachExpressStation[minExAfterMinLocalIdx]:
                    minExAfterMinLocalIdx = idx
                    minExToExtime = rawData.timeToReachExpressStation[idx]

            switch = 0
            if rawData.timeToReachDestination[minLocalIdx] > rawData.timeToReachDestination[minExAfterMinLocalIdx]:
                switch = 1
            finalAns.append([int(rawData.timestamp[minLocalIdx]), weekdayOrNot,
                             rawData.timeToReachExpressStation[minLocalIdx],
                             rawData.timeToReachExpressStation[minExAfterMinLocalIdx],
                             switch
                             ])

    with open('finalData.csv','w') as file:
        for l in finalAns:
            line = ','.join([str(x) for x in l])
            file.write(line)
            file.write('\n')



if __name__ == "__main__":
    # print listdir('rawdata')
    main('rawdata/')
