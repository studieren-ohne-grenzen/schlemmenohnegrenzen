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
        i = 1
        total = len(all_objects)
        for household in all_objects:
            einleitung = get_template("mail/menu/einleitung_correction.txt").render({'household': household})
            firstCourse = get_template("mail/menu/first_course.txt").render()
            firstCourse += self.renderDinner(household.first_visit.gastgeber, household.first_visit.household1.all(), household)

            secondCourse = get_template("mail/menu/second_course.txt").render()
            secondCourse += self.renderDinner(household.second_visit.gastgeber, household.second_visit.household2.all(), household)

            thirdCourse = get_template("mail/menu/third_course.txt").render()
            thirdCourse += self.renderDinner(household.third_visit.gastgeber, household.third_visit.household3.all(), household)

            end = get_template("mail/menu/ende.txt").render()

            txtContent = einleitung + firstCourse + secondCourse + thirdCourse + end

            mail = EmailMessage('Schlemmen Ohne Grenzen - da hat was gefehlt',
                txtContent,
                'hallo@schlemmen-ohne-grenzen.de',
                [household.email1, household.email2],
                #html_message=html_content
                )

            mail.send(fail_silently=False)

            send_mail('[Archiv] Korrektur Speisekarte von '+household.name1+' und '+household.name2,
                txtContent,
                'hallo@schlemmen-ohne-grenzen.de',
                ['hallo@schlemmen-ohne-grenzen.de'],
                #html_message=html_content,
                fail_silently=False)

            print(str(i) + '/' + str(total))
            i += 1

    def renderDinner(self, host, guests, householdMe):
        if (host == householdMe):
            otherGuests = list(filter(lambda x: x != host, guests))
            return get_template("mail/menu/host.txt").render({'host': host, 'guest1': otherGuests[0], 'guest2': otherGuests[1]})
        else:
            otherGuests = list(filter(lambda x: x != host and x != householdMe, guests))[0]
            return get_template("mail/menu/guest.txt").render({'host': host, 'otherGuests': otherGuests})
