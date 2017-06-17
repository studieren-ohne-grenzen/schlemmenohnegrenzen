from django.core.management.base import BaseCommand, CommandError
from frontend.models import Cluster, Household, VisitingGroup
from django.template.loader import get_template
from django.core.mail import send_mail

class Command(BaseCommand):
    help = 'Send all mails with the menus'

    def handle(self, *args, **options):
        all_objects = Household.objects.all().filter(first_visit__isnull=False)
        i = 1
        total = len(all_objects)
        for household in all_objects:
            einleitung = get_template("mail/menu/einleitung.txt").render({'household': household})
            firstCourse = get_template("mail/menu/first_course.txt").render()
            firstCourse += self.render_dinner(household.first_visit.gastgeber, household.first_visit.household1.all(), household)

            secondCourse = get_template("mail/menu/second_course.txt").render()
            secondCourse += self.render_dinner(household.second_visit.gastgeber, household.second_visit.household2.all(), household)

            thirdCourse = get_template("mail/menu/third_course.txt").render()
            thirdCourse += self.render_dinner(household.third_visit.gastgeber, household.third_visit.household3.all(), household)

            end = get_template("mail/menu/ende.txt").render()

            txt_content = einleitung + firstCourse + secondCourse + thirdCourse + end

            #TODO send attachments with mails

            send_mail('Eure Schlemmen Ohne Grenzen Speisekarte',
                txt_content,
                'hallo@schlemmen-ohne-grenzen.de',
                [household.email1, household.email2],
                #html_message=html_content,
                fail_silently=False)

            send_mail('[Archiv] Speisekarte von '+household.name1+' und '+household.name2,
                txt_content,
                'hallo@schlemmen-ohne-grenzen.de',
                ['hallo@schlemmen-ohne-grenzen.de'],
                #html_message=html_content,
                fail_silently=False)

            print(str(i) + '/' + str(total))
            i += 1

    def render_dinner(self, host, guests, householdMe):
        if (host == householdMe):
            return get_template("mail/menu/host.txt").render({'host': host, 'guest1': guests[1], 'guest2': guests[2]})
        else:
            if (guests[1] == householdMe):
                otherGuests = guests[2]
            else:
                otherGuests = guests[1]
            return get_template("mail/menu/guest.txt").render({'host': host, 'otherGuests': otherGuests})
