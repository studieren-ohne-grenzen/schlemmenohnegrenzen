from django.db import models
from geopy.geocoders import Nominatim
import random

class Cluster(models.Model):
    clusterNum = models.IntegerField(default=0)

class Household(models.Model):
    name1 = models.CharField(max_length=200)
    handy1 = models.CharField(max_length=200)
    email1 = models.CharField(max_length=200)
    name2 = models.CharField(max_length=200)
    handy2 = models.CharField(max_length=200)
    email2 = models.CharField(max_length=200)
    newsletter1 = models.BooleanField(default=False)
    newsletter2 = models.BooleanField(default=False)
    plz = models.IntegerField(default=0)
    street = models.CharField(max_length=200)
    note = models.CharField(max_length=2000)
    found_coords = models.BooleanField(default=False)
    longitude = models.FloatField(default=0.0)
    latitude = models.FloatField(default=0.0)
    signup_date = models.DateTimeField()
    cluster = models.ForeignKey(Cluster, on_delete=models.SET_NULL, null=True)

    def lookup_coords(self):
        geocoder = Nominatim()
        address = self.street + ", " + str(self.plz) + " Karlsruhe"
        tmp = geocoder.geocode(address, timeout=10)
        if tmp == None:
            self.found_coords = False
        else:
            self.found_coords = True
            self.longitude = tmp.longitude
            self.latitude = tmp.latitude
