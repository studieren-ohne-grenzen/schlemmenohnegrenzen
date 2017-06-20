from django.core.management.base import BaseCommand, CommandError
from frontend.models import Cluster, Household, VisitingGroup
from django.template.loader import get_template
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
import os.path

class Command(BaseCommand):
    help = 'Send all mails with the menus'

    def handle(self, *args, **options):
        all_objects = Household.objects.all().filter(first_visit__isnull=False)
        self.extractBankData(all_objects)
        self.extractGuestList(all_objects)

    def extractBankData(self, objects):
        f = open('bankdaten.csv','w')
        f.write("Kontoinhaber,Mandatsreferenz,IBAN,BIC,Betrag,Verwendungszweck")
        f.write('\n')
        for household in objects:
            f.write(household.kontoinhaber + ',' + household.mandatsreferenz + ',' + household.iban + ',' + household.bic + ',' + "8" + "Schlemmen ohne Grenzen")
            f.write('\n')

    def extractGuestList(self, objects):
        all_objects = Household.objects.all().filter(first_visit__isnull=False)
        f = open('gaesteliste.csv','w')
        f.write("Name,Telefonnummer")
        f.write('\n')
        guestlist = []
        for household in objects:
            guestlist += [[household.name1]]
            guestlist += [[household.name2]]

        guestlist.sort()
        for people in guestlist:
            f.write(people[0])
            f.write('\n')
