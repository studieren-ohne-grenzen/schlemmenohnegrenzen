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
            einleitung = get_template("mail/menu/einleitung.txt").render({'household': household})
            firstCourse = get_template("mail/menu/first_course.txt").render()
            firstCourse += self.renderDinner(household.first_visit.gastgeber, household.first_visit.household1.all(), household)

            secondCourse = get_template("mail/menu/second_course.txt").render()
            secondCourse += self.renderDinner(household.second_visit.gastgeber, household.second_visit.household2.all(), household)

            thirdCourse = get_template("mail/menu/third_course.txt").render()
            thirdCourse += self.renderDinner(household.third_visit.gastgeber, household.third_visit.household3.all(), household)

            end = get_template("mail/menu/ende.txt").render()

            txtContent = einleitung + firstCourse + secondCourse + thirdCourse + end

            #TODO send attachments with mails

            mail = EmailMessage('Eure Schlemmen Ohne Grenzen Speisekarte',
                txtContent,
                'hallo@schlemmen-ohne-grenzen.de',
                ['privat@denniskeck.de'],
                #html_message=html_content
                )
            
            self.attachBasic(mail)
            self.attachPuzzles(mail, household.puzzle)
            mail.send(fail_silently=False)

            send_mail('[Archiv] Speisekarte von '+household.name1+' und '+household.name2,
                txtContent,
                'hallo@schlemmen-ohne-grenzen.de',
                ['hallo@schlemmen-ohne-grenzen.de'],
                #html_message=html_content,
                fail_silently=False)

            print(str(i) + '/' + str(total))
            i += 1

    def renderDinner(self, host, guests, householdMe):
        if (host == householdMe):
            return get_template("mail/menu/host.txt").render({'host': host, 'guest1': guests[1], 'guest2': guests[2]})
        else:
            if (guests[1] == householdMe):
                otherGuests = guests[2]
            else:
                otherGuests = guests[1]
            return get_template("mail/menu/guest.txt").render({'host': host, 'otherGuests': otherGuests})
    
    def attachBasic(self, mail):
        fd = self.getPuzzleFd('basic/einladung.pdf')
        mail.attach('Einladung von Richard Schoenborn.pdf', fd.read(), 'application/pdf')
            
    def attachPuzzles(self, mail, puzzle):
        if puzzle == 91:
            self.attachToMail(mail, 'vorspeise/1/G.jpg', 'Hinweis Vorspeise.jpg', 'image/jpeg')
        elif puzzle == 92:
            #(92, "9.2 Vorspeise 1.1, Hauptspeise B.G, Nachspeise N.1"),
            self.attachToMail(mail, 'vorspeise/1/1.jpg', 'Hinweis Vorspeise.jpg', 'image/jpeg')
        elif puzzle == 93:
            self.attachToMail(mail, 'vorspeise/1/2.jpg', 'Hinweis Vorspeise.jpg', 'image/jpeg')
        
    def attachPuzzlesMainCourseB(self, mail, guestIdentifier):
        if guestIdentifier == 'G':
            #host
            self.attachToMail(mail, 'hauptgang/B/hint.jpg', 'Hinweis Hauptspeise.jpg', 'image/jpeg')
            self.attachToMail(mail, 'hauptgang/B/1.png', 'Karte 1 Hauptspeise.jpg', 'image/png')
            self.attachToMail(mail, 'hauptgang/B/6.png', 'Karte 2 Hauptspeise.jpg', 'image/png')
            self.attachToMail(mail, 'hauptgang/B/9.png', 'Karte 3 Hauptspeise.jpg', 'image/png')
            self.attachToMail(mail, 'hauptgang/B/12.png', 'Karte 4 Hauptspeise.jpg', 'image/png')
        elif guestIdentifier == '1':
            #guest 1
            self.attachToMail(mail, 'hauptgang/B/hint.jpg', 'Hinweis Hauptspeise.jpg', 'image/jpeg')
            self.attachToMail(mail, 'hauptgang/B/2.png', 'Karte 1 Hauptspeise.jpg', 'image/png')
            self.attachToMail(mail, 'hauptgang/B/3.png', 'Karte 2 Hauptspeise.jpg', 'image/png')
            self.attachToMail(mail, 'hauptgang/B/8.png', 'Karte 3 Hauptspeise.jpg', 'image/png')
            self.attachToMail(mail, 'hauptgang/B/10.png', 'Karte 4 Hauptspeise.jpg', 'image/png')    
        elif guestIdentifier == '1':
            #guest 2
            self.attachToMail(mail, 'hauptgang/B/hint.jpg', 'Hinweis Hauptspeise.jpg', 'image/jpeg')
            self.attachToMail(mail, 'hauptgang/B/5.png', 'Karte 1 Hauptspeise.jpg', 'image/png')
            self.attachToMail(mail, 'hauptgang/B/7.png', 'Karte 2 Hauptspeise.jpg', 'image/png')
            self.attachToMail(mail, 'hauptgang/B/4.png', 'Karte 3 Hauptspeise.jpg', 'image/png')
            self.attachToMail(mail, 'hauptgang/B/11.png', 'Karte 4 Hauptspeise.jpg', 'image/png')    
        
    def getPuzzleFd(self, loc):
        return open(settings.BASE_DIR + '/frontend/static/frontend/puzzles/' + loc, 'rb')
        
    def attachToMail(self, mail, path, name, mime):
        fd = self.getPuzzleFd(path)
        mail.attach(name, fd.read(), mime)
        fd.close()