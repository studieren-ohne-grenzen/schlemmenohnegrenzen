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

            mail = EmailMessage('Eure Schlemmen Ohne Grenzen Speisekarte',
                txtContent,
                'hallo@schlemmen-ohne-grenzen.de',
                [household.email1, household.email2],
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
            otherGuests = list(filter(lambda x: x == host or x == householdMe, guests))[0]
            return get_template("mail/menu/guest.txt").render({'host': host, 'otherGuests': otherGuests})

    def attachBasic(self, mail):
        fd = self.getPuzzleFd('basic/einladung.pdf')
        mail.attach('Einladung von Richard Schoenborn.pdf', fd.read(), 'application/pdf')

    def attachPuzzles(self, mail, puzzleGroup):
        #TODO: zusatzinfos Z0: 1, Z1: 3C, Z2: A
        hintLists = {
            91: '1GA1N1',
            92: '11BGN1',
            93: '12CGN1',
            94: '21AGN2',
            95: '2GB1N2',
            96: '22C1NG',
            97: '3GA2N2',
            98: '31B2NG',
            99: '32C2NG',
            1201: '1GA1N1',
            1202: '11BGN1',
            1203: '12BGN1',
            1204: '21AGN2',
            1205: '2GB1N2',
            1206: '22C1NG',
            1207: '3GB2N2',
            1208: '31B2NG',
            1209: '32C2NG',
            1210: '2GA2N1Z0',
            1211: '21B1NGZ1',
            1212: '22CGN2Z2'
        }
        hints = hintLists[puzzleGroup]
        for i in list(filter(lambda x: x%2 == 0, range(0, len(hints)))):
            self.attachPuzzleFiles(mail, hints[i], hints[i + 1])

    def attachPuzzleFiles(self, mail, puzzle, guestIdentifier):
        try:
            method_to_call = getattr(self, 'attachPuzzleFiles' + puzzle)
            method_to_call(mail, guestIdentifier)
        except AttributeError as e:
            self.attachPuzzlesDefault(mail, puzzle, guestIdentifier)

    def attachPuzzlesDefault(self, mail, puzzle, guestIdentifier):
        puzzleCourses = {
            '1': 'vorspeise',
            '2': 'vorspeise',
            '3': 'vorspeise',
            'A': 'hauptspeise',
            'B': 'hauptspeise',
            'C': 'hauptspeise',
            'N': 'nachspeise',
            'Z': 'zusatzinfos'
        }

        course = puzzleCourses[puzzle]
        if guestIdentifier == 'G':
            #host
            self.attachToMail(mail, course + '/' + puzzle + '/text.pdf', 'Text ' + course.capitalize() + '.pdf', 'application/pdf')
        self.attachToMail(mail, course + '/' + puzzle + '/' + guestIdentifier + '.jpg', 'Hinweis ' + course.capitalize() + '.jpg', 'image/jpeg')

    def attachPuzzleFilesZ(self, mail, guestIdentifier):
            self.attachToMail(mail, '/zusatzinfos/' + guestIdentifier + '.pdf', 'Zusatzinfo Nachspeise.pdf', 'application/pdf')

    def attachPuzzleFilesN(self, mail, guestIdentifier):
        if guestIdentifier == 'G':
            #host
            self.attachToMail(mail, 'nachspeise/text.pdf', 'Text Nachspeise.pdf', 'application/pdf')
        else:
            self.attachToMail(mail, 'nachspeise/url.jpg', 'Hinweis Nachspeise.jpg', 'image/jpg')

    def attachPuzzleFilesC(self, mail, guestIdentifier):
        if guestIdentifier == 'G':
            #host
            self.attachToMail(mail, 'hauptspeise/C/Ga.jpg', 'Hinweis 1 Hauptspeise.jpg', 'image/jpg')
            self.attachToMail(mail, 'hauptspeise/C/Gb.jpg', 'Hinweis 2 Hauptspeise.jpg', 'image/jpg')
        else:
            self.attachPuzzlesDefault(mail, 'C', guestIdentifier)

    def attachPuzzleFilesB(self, mail, guestIdentifier):
        if guestIdentifier == 'G':
            #host
            self.attachToMail(mail, 'hauptspeise/B/text.pdf', 'Text Hauptspeise.pdf', 'application/pdf')
            self.attachToMail(mail, 'hauptspeise/B/1.png', 'Karte 1 Hauptspeise.png', 'image/png')
            self.attachToMail(mail, 'hauptspeise/B/6.png', 'Karte 2 Hauptspeise.png', 'image/png')
            self.attachToMail(mail, 'hauptspeise/B/9.png', 'Karte 3 Hauptspeise.png', 'image/png')
            self.attachToMail(mail, 'hauptspeise/B/12.png', 'Karte 4 Hauptspeise.png', 'image/png')
        elif guestIdentifier == '1':
            #guest 1
            self.attachToMail(mail, 'hauptspeise/B/2.png', 'Karte 1 Hauptspeise.png', 'image/png')
            self.attachToMail(mail, 'hauptspeise/B/3.png', 'Karte 2 Hauptspeise.png', 'image/png')
            self.attachToMail(mail, 'hauptspeise/B/8.png', 'Karte 3 Hauptspeise.png', 'image/png')
            self.attachToMail(mail, 'hauptspeise/B/10.png', 'Karte 4 Hauptspeise.png', 'image/png')
        elif guestIdentifier == '2':
            #guest 2
            self.attachToMail(mail, 'hauptspeise/B/hinweis.jpg', 'Hinweis Hauptspeise.png', 'image/jpeg')
            self.attachToMail(mail, 'hauptspeise/B/5.png', 'Karte 1 Hauptspeise.png', 'image/png')
            self.attachToMail(mail, 'hauptspeise/B/7.png', 'Karte 2 Hauptspeise.png', 'image/png')
            self.attachToMail(mail, 'hauptspeise/B/4.png', 'Karte 3 Hauptspeise.png', 'image/png')
            self.attachToMail(mail, 'hauptspeise/B/11.png', 'Karte 4 Hauptspeise.png', 'image/png')

    def getPuzzleFd(self, loc):
        return open(settings.BASE_DIR + '/frontend/static/frontend/puzzles/' + loc, 'rb')

    def attachToMail(self, mail, path, name, mime):
        fd = self.getPuzzleFd(path)
        mail.attach(name, fd.read(), mime)
        fd.close()
