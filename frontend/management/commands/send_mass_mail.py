from django.core.management.base import BaseCommand, CommandError
from frontend.models import Cluster, Household, VisitingGroup
from django.template.loader import get_template
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
import os.path

class Command(BaseCommand):
    help = 'Send a mass mail'

    def handle(self, *args, **options):
        all_objects = Household.objects.all().filter(first_visit__isnull=False)
        i = 1
        total = len(all_objects)
        for household in all_objects:
            text = get_template("mail/mass_mail.txt").render({'household': household})

            mail = EmailMessage('Schlemmen Ohne Grenzen: Danke an euch alle | The Black Pretzels',
                text,
                'hallo@schlemmen-ohne-grenzen.de',
                [household.email1, household.email2],
                #html_message=html_content
                )

            mail.send(fail_silently=False)

            print(str(i) + '/' + str(total))
            i += 1
