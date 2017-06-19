from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from frontend.models import Household, Cluster, VisitingGroup, MandatsreferenzCounter
from frontend.forms import HouseholdForm, LastschriftForm
from django.utils import timezone
from .clustering import initial_clusters, balance_clusters, generate_visiting_groups
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import json
from django.template.loader import get_template
from .hilfen import hilfen
from datetime import datetime
from django.db.models import F
from django.conf import settings

def email_senden(house):
    txt_content = get_template("mail/confirmation.txt").render({'house': house})
    #html_content = get_template("mail/confirmation.html").render(house)
    send_mail('Schlemmen Ohne Grenzen Bestätigung!',
        txt_content,
        'hallo@schlemmen-ohne-grenzen.de',
        [house.email1,house.email2],
        #html_message=html_content,
        fail_silently=False)

    if not house.personal_payment:
        iban_start = house.iban[:4]
        iban_end = house.iban[-3:]
        payment_txt_content = get_template("mail/sepa.txt").render({'house': house, 'iban_start': iban_start, 'iban_end': iban_end})
        #payment_html_content = get_template("mail/confirmation.html").render(house)
        send_mail('Schlemmen Ohne Grenzen SEPA-Lastschriftmandat',
        payment_txt_content,
        'hallo@schlemmen-ohne-grenzen.de',
        [house.email1],
        #html_message=payment_html_content,
        fail_silently=True)

    admin_content = get_template("mail/confirmation_admin.txt").render({'house': house})
    send_mail('[Info] Schlemmen Anmeldung',
    admin_content,
    'hallo@schlemmen-ohne-grenzen.de',
    ['hallo@schlemmen-ohne-grenzen.de'],
    fail_silently=True)

def faq(request):
    return render(request, 'frontend/faq.html')

def charaktere(request):
    return render(request, 'frontend/charaktere.html')

def portal(request):
    return render(request, 'frontend/portal.html')

def vorspeise(request):
    return render(request, 'frontend/vorspeise.html')

def nachspeise(request):
    return render(request, 'frontend/nachspeise.html')

def hilfe(request):
    newhilfen = []

    for hilfe in hilfen:
        if hilfe['datetime'] < datetime.now():
            newhilfen.append(hilfe)

    return render(request, 'frontend/hilfe.html', {'hilfen': newhilfen})

def index(request):
    if request.method == 'POST':
        form = HouseholdForm(request.POST)
        if form.is_valid():
            personal_payment=form.cleaned_data['personal_payment']
            if personal_payment:
                house = Household(name1=form.cleaned_data['name1'],
                    name2=form.cleaned_data['name2'],
                    email1=form.cleaned_data['email1'],
                    email2=form.cleaned_data['email2'],
                    handy1=form.cleaned_data['handy1'],
                    handy2=form.cleaned_data['handy2'],
                    newsletter1=form.cleaned_data['newsletter1'],
                    newsletter2=form.cleaned_data['newsletter2'],
                    plz=form.cleaned_data['plz'],
                    street=form.cleaned_data['street'],
                    gpsstreet=form.cleaned_data['street'],
                    note=form.cleaned_data['note'],
                    kontoinhaber="",
                    iban="",
                    bic="",
                    signup_date=timezone.now(),
                    personal_payment=True,
                    mandatsreferenz="")
                house.lookup_coords()
                house.save()
                email_senden(house)
                return HttpResponseRedirect(reverse('frontend:signup_successful'))
            else:
                request.session['name1'] = form.cleaned_data['name1']
                request.session['name2'] = form.cleaned_data['name2']
                request.session['email1'] = form.cleaned_data['email1']
                request.session['email2'] = form.cleaned_data['email2']
                request.session['handy1'] = form.cleaned_data['handy1']
                request.session['handy2'] = form.cleaned_data['handy2']
                request.session['newsletter1'] = form.cleaned_data['newsletter1']
                request.session['newsletter2'] = form.cleaned_data['newsletter2']
                request.session['plz'] = form.cleaned_data['plz']
                request.session['street'] = form.cleaned_data['street']
                request.session['note'] = form.cleaned_data['note']
                request.session['kontoinhaber'] = form.cleaned_data['kontoinhaber']
                request.session['kontoinhaber_city'] = form.cleaned_data['kontoinhaber_city']
                request.session['kontoinhaber_street'] = form.cleaned_data['kontoinhaber_street']
                request.session['iban'] = form.cleaned_data['iban']
                request.session['bic'] = form.cleaned_data['bic']
                return HttpResponseRedirect(reverse('frontend:confirmation'))
    else:
        form = HouseholdForm()
    return render(request, 'frontend/index.html', {'form': form, 'signupEnabled': settings.SIGNUP_ENABLED})

def signup_successful(request):
    return render(request, 'frontend/signup_successful.html')

def bedingungen(request):
    return render(request, 'frontend/bedingungen.html')

def generate_mandatsreferenz():
    cnt = -1
    if MandatsreferenzCounter.objects.count() == 0:
        mc = MandatsreferenzCounter()
        mc.cnt = 1
        mc.save()
        cnt = 1
    else:
        mc = MandatsreferenzCounter.objects.all()[0]
        mc.cnt += 1
        cnt = mc.cnt
        mc.save()
    return "SCHLEMMEN20170621KA{:05d}".format(cnt)


def confirmation(request):
    if request.method == 'POST':
        form = LastschriftForm(request.POST)
        if form.is_valid() and form.cleaned_data['mandat'] == True:
            # in db speichern
            house = Household(name1=request.session['name1'],
                name2=request.session['name2'],
                email1=request.session['email1'],
                email2=request.session['email2'],
                handy1=request.session['handy1'],
                handy2=request.session['handy2'],
                newsletter1=request.session['newsletter1'],
                newsletter2=request.session['newsletter2'],
                plz=request.session['plz'],
                street=request.session['street'],
                gpsstreet=request.session['street'],
                note=request.session['note'],
                kontoinhaber=request.session['kontoinhaber'],
                kontoinhaber_city=request.session['kontoinhaber_city'],
                kontoinhaber_street=request.session['kontoinhaber_street'],
                iban=request.session['iban'],
                bic=request.session['bic'],
                signup_date=timezone.now(),
                personal_payment=False,
                mandatsreferenz=request.session['mandatsreferenz'])
            house.lookup_coords()
            house.save()
            email_senden(house)
            request.session.flush()
            return HttpResponseRedirect(reverse('frontend:signup_successful'))
    else:
        form = LastschriftForm()
    if (not 'iban' in request.session) or (not 'bic' in request.session) or (not 'kontoinhaber' in request.session):
        return HttpResponseRedirect(reverse('frontend:index'))
    if not 'mandatsreferenz' in request.session:
        mandatsreferenz = generate_mandatsreferenz()
        request.session['mandatsreferenz'] = mandatsreferenz
    else:
        mandatsreferenz = request.session['mandatsreferenz']
    return render(request, 'frontend/confirmation.html', {
        'kontoinhaber': request.session['kontoinhaber'],
        'kontoinhaber_city': request.session['kontoinhaber_city'],
        'kontoinhaber_street': request.session['kontoinhaber_street'],
        'iban': request.session['iban'],
        'bic': request.session['bic'],
        'mandatsreferenz': mandatsreferenz,
        'form': form
    })

@login_required
def regenerate_clusters(request):
    # delete all current clusters
    Cluster.objects.all().delete()
    households = Household.objects.all().filter(found_coords__exact=True)

    remainder = len(households) % 9
    print(remainder)
    numOf12Clusters = 0
    if remainder >= 6:
        numOf12Clusters = 2
    elif remainder >= 3:
        numOf12Clusters = 1

    numOfClusters = len(households) // 9 # should also work with 12 because remainder is discarded
    maxElems = numOfClusters * 9 + numOf12Clusters * 3
    households = households[0:maxElems]
    clusters = []
    for i in range(0, numOfClusters):
        clst = Cluster()
        clst.clusterNum = i
        clst.save()
        clusters.append(clst)

    initial_clusters(households, clusters)
    balance_clusters(households, clusters, numOf12Clusters)

    return HttpResponseRedirect(reverse('frontend:cluster'))

@login_required
def regenerate_gps(request):
    houses = Household.objects.all()
    for house in houses:
        house.lookup_coords()
        house.save()
    return HttpResponseRedirect(reverse('frontend:cluster'))

@login_required
def regenerate_visiting_groups(request):
    # delete all current visiting groups
    VisitingGroup.objects.all().delete()

    clusters = Cluster.objects.all()
    generate_visiting_groups(clusters)

    return HttpResponseRedirect(reverse('frontend:cluster'))

@login_required
def cluster(request):
    all_objects = Household.objects.all().filter(found_coords__exact=True).filter(cluster__isnull=False)

    jsonlst = []
    for obj in all_objects:
        jsonlst.append({"longitude": obj.longitude, "latitude": obj.latitude, "cluster": obj.cluster.clusterNum, "name1": obj.name1, "name2": obj.name2, "street": obj.street})

    jsonstr = json.dumps(jsonlst)

    wrong_entries = Household.objects.all().filter(found_coords__exact=False)
    personal_payers = Household.objects.all().filter(personal_payment__exact=True)

    vs = VisitingGroup.objects.all().filter(dinner=0)
    vorspeise = []

    for v in vs:
        house = v.household1.all()
        vorspeise.append({'street': v.gastgeber.street, 'name1': v.gastgeber.name1 + ' & ' + v.gastgeber.name2, 'name2': house[0].name1 + ' & ' + house[0].name2 + ', ' + house[0].street, 'name3': house[1].name1 + ' & ' + house[1].name2 + ', ' + house[1].street, 'name4': house[2].name1 + ' & ' + house[2].name2 + ', ' + house[2].street})

    hs = VisitingGroup.objects.all().filter(dinner=1)
    hauptspeise = []

    for v in hs:
        house = v.household2.all()
        if len(house) == 3:
            hauptspeise.append({'street': v.gastgeber.street, 'name1': v.gastgeber.name1 + ' & ' + v.gastgeber.name2, 'name2': house[0].name1 + ' & ' + house[0].name2 + ', ' + house[0].street, 'name3': house[1].name1 + ' & ' + house[1].name2 + ', ' + house[1].street, 'name4': house[2].name1 + ' & ' + house[2].name2 + ', ' + house[2].street})
        else:
            print(len(house))

    ns = VisitingGroup.objects.all().filter(dinner=2)
    nachspeise = []

    for v in ns:
        house = v.household3.all()
        nachspeise.append({'street': v.gastgeber.street, 'name1': v.gastgeber.name1 + ' & ' + v.gastgeber.name2, 'name2': house[0].name1 + ' & ' + house[0].name2 + ', ' + house[0].street, 'name3': house[1].name1 + ' & ' + house[1].name2 + ', ' + house[1].street, 'name4': house[2].name1 + ' & ' + house[2].name2 + ', ' + house[2].street})

    return render(request, 'frontend/cluster.html', {"jsonstr": jsonstr, "wrong_entries": wrong_entries, "personal_payers": personal_payers, 'vorspeise': vorspeise, 'hauptspeise': hauptspeise, 'nachspeise': nachspeise, 'all_housholds': all_objects})
