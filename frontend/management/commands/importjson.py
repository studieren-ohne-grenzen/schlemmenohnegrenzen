from django.core.management.base import BaseCommand, CommandError
from frontend.models import Cluster, Household
import json
from django.utils import timezone
from ...choices import plz_choices

class Command(BaseCommand):
    help = 'Imports a JSON file to the database'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+', type=str)

    def handle(self, *args, **options):
        for filename in options['filename']:
            f = open(filename)
            jsonlist = json.load(f)
            for elem in jsonlist:
                plz = 76131
                try:
                    plz = int(elem['address']['zip'])
                except ValueError:
                    print("Error while converting zip code", elem['address']['zip'], "to integer")
                
                house = Household(name1="Name 1",
                    name2="Name 2",
                    email1="schlemmen1@s.denniskeck.de",
                    email2="schlemmen2@s.denniskeck.de",
                    handy1="handy1",
                    handy2="handy2",
                    newsletter1=False,
                    newsletter2=False,
                    plz=plz,
                    street=elem['address']['street'],
                    gpsstreet=elem['address']['street'],
                    note="Das ist die Notiz",
                    kontoinhaber="",
                    iban="",
                    bic="",
                    signup_date=timezone.now(),
                    personal_payment=True,
                    mandatsreferenz="")
                house.lookup_coords()
                house.save()

