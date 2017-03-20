import mraa
import time

import math


import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()

from polls.models import Temperature





B=4275



print "Press Ctrl+C to escape..."
try:
    while (1):

        
        tempSensor = mraa.Aio(1)
        
        R = (1023.0/tempSensor.read()-1.0) * 100000 
        temperature=1.0/(math.log(R/100000.0)/B+1/298.15)-273.15
        
        newItem = Temperature(timestamp= time.time(), temperature= temperature)
        newItem.save()
        Temperature.objects.get(id = newItem.id-5).delete()


        time.sleep(5)
        

except KeyboardInterrupt:
    exit

