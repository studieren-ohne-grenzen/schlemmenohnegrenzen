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
        all_objects = Household.objects.all().filter()
        i = 1
        total = 2 * len(all_objects)
        for household in all_objects:
            text = get_template("mail/mass_mail.txt").render({'household': household})

            if (household.newsletter1):
                text = get_template("mail/advertisement.txt").render({'name': household.name1})
                mail = EmailMessage('Karlsruhe schlemmt wieder! - Schlemmen Ohne Grenzen #8 am 30. November!',
                    text,
                    'hallo@schlemmen-ohne-grenzen.de',
                    [household.email1]
                    )
                mail.send(fail_silently=False)
                i += 1
                print(str(i) + '/' + str(total))
            if (household.newsletter2):
                text = get_template("mail/advertisement.txt").render({'name': household.name2})
                mail = EmailMessage('Karlsruhe schlemmt wieder! - Schlemmen Ohne Grenzen #8 am 30. November!',
                    text,
                    'hallo@schlemmen-ohne-grenzen.de',
                    [household.email2]
                    )
                mail.send(fail_silently=False)
                i += 1
                print(str(i) + '/' + str(total))
