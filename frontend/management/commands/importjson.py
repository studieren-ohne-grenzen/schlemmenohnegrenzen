from django.core.management.base import BaseCommand, CommandError
from frontend.models import Cluster, Household
import json
from django.utils import timezone

class Command(BaseCommand):
    help = 'Imports a JSON file to the database'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+', type=str)

    def handle(self, *args, **options):
        for filename in options['filename']:
            f = open(filename)
            jsonlist = json.load(f)
            for elem in jsonlist:
                household = Household(name1='a', name2='b', handy1='1', handy2='2', email1='asd', email2='asd', newsletter1=False, newsletter2=False, street=elem['address']['street'], plz=76131, note='asd', signup_date=timezone.now())
                household.lookup_coords()
                household.save()
