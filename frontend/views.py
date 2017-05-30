from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from frontend.models import Household, Cluster, VisitingGroup
from frontend.forms import HouseholdForm
from django.utils import timezone
from .clustering import initial_clusters, balance_clusters, generate_visiting_groups
from django.contrib.auth.decorators import login_required
import json

def index(request):
    if request.method == 'POST':
        form = HouseholdForm(request.POST)
        if form.is_valid():
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
                kontoinhaber=form.cleaned_data['kontoinhaber'],
                iban=form.cleaned_data['iban'],
                bic=form.cleaned_data['bic'],
                signup_date=timezone.now(),
                personal_payment=form.cleaned_data['personal_payment'])
            house.lookup_coords()
            house.save()
            return HttpResponseRedirect(reverse('frontend:signup_successful'))
    else:
        form = HouseholdForm()
    return render(request, 'frontend/index.html', {'form': form})

def signup_successful(request):
    return render(request, 'frontend/signup_successful.html')

def confirmation(request):
    return render(request, 'frontend/confirmation.html')

@login_required
def regenerate_clusters(request):
    # delete all current clusters
    Cluster.objects.all().delete()
    households = Household.objects.all().filter(found_coords__exact=True)
    householdsPerCluster = 9
    numOfClusters = len(households) // 9
    maxElems = numOfClusters * 9
    households = households[0:maxElems]
    clusters = []
    for i in range(0, numOfClusters):
        clst = Cluster()
        clst.clusterNum = i
        clst.save()
        clusters.append(clst)

    initial_clusters(households, clusters)
    balance_clusters(households, clusters)

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

    return render(request, 'frontend/cluster.html', {"jsonstr": jsonstr, "wrong_entries": wrong_entries, "personal_payers": personal_payers})
