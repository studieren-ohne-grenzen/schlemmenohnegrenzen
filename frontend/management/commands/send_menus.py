from django.core.management.base import BaseCommand, CommandError
from frontend.models import Cluster, Household, VisitingGroup
from django.template.loader import get_template

class Command(BaseCommand):
    help = 'Send all mails with the menus'

    def handle(self, *args, **options):
        all_objects = Household.objects.all().filter(first_visit__isnull=False)
        
        for household in all_objects:
            einleitung = payment_txt_content = get_template("mail/menu/einleitung.txt").render({'household': household})
            
            puzzle = "puzzle"
            
            print(einleitung)

