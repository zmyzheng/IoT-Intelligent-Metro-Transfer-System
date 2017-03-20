from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils import timezone

from django.utils.encoding import python_2_unicode_compatible

# Create your models here.



@python_2_unicode_compatible# only if you need to support Python 2
class Temperature(models.Model):
    timestamp = models.FloatField()
    temperature = models.FloatField()
    
    def __str__(self):
        return str(self.temperature)
