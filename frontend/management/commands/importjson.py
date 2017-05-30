from django.core.management.base import BaseCommand, CommandError
from frontend.models import Cluster, Household
import json
from django.utils import timezone
from .choices import plz_choices

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
                household = Household(name1='a', name2='b', handy1='1', handy2='2', email1='asd', email2='asd', newsletter1=False, newsletter2=False, street=elem['address']['street'], gpsstreet=elem['address']['street'], plz=plz, note='asd', signup_date=timezone.now(), iban="", bic="", kontoinhaber="" personal_payer=True)
                household.lookup_coords()
                household.save()

