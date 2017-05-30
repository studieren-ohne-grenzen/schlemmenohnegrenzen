from django.db import models
from geopy.geocoders import Nominatim
from .choices import plz_choices
import random

class Cluster(models.Model):
    clusterNum = models.IntegerField(default=0)

class VisitingGroup(models.Model):
    visiting_group_num = models.IntegerField(default=0)

class Household(models.Model):
    name1 = models.CharField(max_length=200)
    handy1 = models.CharField(max_length=200)
    email1 = models.CharField(max_length=200)
    name2 = models.CharField(max_length=200)
    handy2 = models.CharField(max_length=200)
    email2 = models.CharField(max_length=200)
    newsletter1 = models.BooleanField(default=False)
    newsletter2 = models.BooleanField(default=False)
    plz = models.IntegerField(default=76133, choices=plz_choices)
    street = models.CharField(max_length=200)
    gpsstreet = models.CharField(max_length=200)
    note = models.CharField(max_length=2000)
    found_coords = models.BooleanField(default=False)
    longitude = models.FloatField(default=0.0)
    latitude = models.FloatField(default=0.0)
    signup_date = models.DateTimeField()
    cluster = models.ForeignKey(Cluster, on_delete=models.SET_NULL, null=True)
    first_visit = models.ForeignKey(VisitingGroup, on_delete=models.SET_NULL, null=True, related_name='household1')
    second_visit = models.ForeignKey(VisitingGroup, on_delete=models.SET_NULL, null=True, related_name='household2')
    third_visit = models.ForeignKey(VisitingGroup, on_delete=models.SET_NULL, null=True, related_name='household3')
    iban = models.CharField(max_length=200)
    bic = models.CharField(max_length=200)
    kontoinhaber = models.CharField(max_length=200)
    personal_payment = models.BooleanField(default=False)

    def lookup_coords(self):
        geocoder = Nominatim()
        address = self.gpsstreet + ", " + str(self.plz) + " Karlsruhe"
        tmp = geocoder.geocode(address, timeout=10)
        if tmp == None:
            self.found_coords = False
        else:
            self.found_coords = True
            self.longitude = tmp.longitude
            self.latitude = tmp.latitude
