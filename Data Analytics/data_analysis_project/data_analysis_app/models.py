# Create your models here.
# predictor/models.py
from django.db import models

class HistoricalData(models.Model):
    year = models.IntegerField()
    population = models.FloatField()
    co2 = models.FloatField()

    def __str__(self):
        return str(self.year)
