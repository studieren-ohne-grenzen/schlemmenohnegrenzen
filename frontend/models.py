from django.db import models
from geopy.geocoders import Nominatim
from .choices import plz_choices
import random

class MandatsreferenzCounter(models.Model):
    cnt = models.IntegerField(default=0)

class Cluster(models.Model):
    clusterNum = models.IntegerField(default=0)

class VisitingGroup(models.Model):
    visiting_group_num = models.IntegerField(default=0)
    dinner = models.IntegerField(default = 0)
    gastgeber = models.ForeignKey('Household', on_delete=models.SET_NULL, null=True, blank=True)

class Household(models.Model):
    name1 = models.CharField(max_length=200)
    handy1 = models.CharField(max_length=200)
    email1 = models.CharField(max_length=200)
    name2 = models.CharField(max_length=200)
    handy2 = models.CharField(max_length=200, blank=True)
    email2 = models.CharField(max_length=200)
    newsletter1 = models.BooleanField(default=False)
    newsletter2 = models.BooleanField(default=False)
    plz = models.IntegerField(default=76133, choices=plz_choices)
    street = models.CharField(max_length=200)
    gpsstreet = models.CharField(max_length=200)
    note = models.CharField(max_length=2000, blank=True)
    found_coords = models.BooleanField(default=False)
    longitude = models.FloatField(default=0.0)
    latitude = models.FloatField(default=0.0)
    signup_date = models.DateTimeField()
    cluster = models.ForeignKey(Cluster, on_delete=models.SET_NULL, null=True, blank=True)
    first_visit = models.ForeignKey(VisitingGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name='household1')
    second_visit = models.ForeignKey(VisitingGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name='household2')
    third_visit = models.ForeignKey(VisitingGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name='household3')
    iban = models.CharField(max_length=200, blank=True)
    bic = models.CharField(max_length=200, blank=True)
    kontoinhaber = models.CharField(max_length=200, blank=True)
    personal_payment = models.BooleanField(default=False)
    mandatsreferenz = models.CharField(max_length=35, blank=True)
    kontoinhaber_city = models.CharField(max_length=200, blank=True)
    kontoinhaber_street = models.CharField(max_length=200, blank=True)

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
