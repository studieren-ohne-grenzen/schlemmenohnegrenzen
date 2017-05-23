from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from frontend.models import Household, Cluster, VisitingGroup
from frontend.forms import HouseholdForm
from django.utils import timezone
from .clustering import initial_clusters, balance_clusters
import json
from operator import itemgetter
import cProfile, pstats, io

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
                note=form.cleaned_data['note'],
                signup_date=timezone.now())
            house.lookup_coords()
            house.save()
            return HttpResponseRedirect(reverse('frontend:signup_successful'))
    else:
        form = HouseholdForm()
    return render(request, 'frontend/index.html', {'form': form})

def signup_successful(request):
    return render(request, 'frontend/signup_successful.html')

def regenerate_clusters(request):
    # TODO: Authentication
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

def visitingCollision(h1, h2, h3):
    # TODO: PLZ
    if h1['street'] == h2['street'] or h1['street'] == h3['street'] or h2['street'] == h3['street']:
        return True
    else:
        return False

def get_score(households, elems):
    score = 0
    h1 = households[elems[0]]
    h2 = households[elems[1]]
    h3 = households[elems[2]]
    h4 = households[elems[3]]
    h5 = households[elems[4]]
    h6 = households[elems[5]]
    h7 = households[elems[6]]
    h8 = households[elems[7]]
    h9 = households[elems[8]]
    if visitingCollision(h1, h2, h3) or visitingCollision(h4, h5, h6) or visitingCollision(h7, h8, h9):
        score += 1
    if visitingCollision(h1, h4, h7) or visitingCollision(h2, h5, h8) or visitingCollision(h3, h6, h9):
        score += 1
    if visitingCollision(h1, h5, h9) or visitingCollision(h2, h6, h7) or visitingCollision(h3, h4, h8):
        score += 1
    return score

def recur(households, curr_elems, scores, pr):
    for i in range(9):
        #if len(curr_elems) == 3:
            #print(curr_elems, i)
        #    if curr_elems == [0, 1, 2] and i == 0:
        #        pr.enable()
        #        print("start")
        #    if curr_elems == [0, 1, 3] and i == 0:
        #        pr.disable()
        #        print("stop")
        #        s = io.StringIO()
        #        ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
        #        ps.print_stats()
        #        print(s.getvalue())
        if i not in curr_elems:
            new_elems = curr_elems[:]
            new_elems.append(i)
            if len(new_elems) < 9:
                recur(households, new_elems, scores, pr)
            else:
                score = get_score(households, new_elems)
                scores.append((score, new_elems))

def regenerate_visiting_groups(request):
    # TODO: Authentication

    # delete all current visiting groups
    VisitingGroup.objects.all().delete()

    clusters = Cluster.objects.all()

    curr_v_num = 0

    for cluster in clusters:
        scores = []
        households = []
        household_a = cluster.household_set.all()
        for h in household_a:
            households.append({'street': h.street, 'plz': h.plz})
        pr = cProfile.Profile()
        recur(households, [], scores, pr)
        scores.sort(key=itemgetter(0))
        score = scores[0][1]
        h1 = household_a[score[0]]
        h2 = household_a[score[1]]
        h3 = household_a[score[2]]
        h4 = household_a[score[3]]
        h5 = household_a[score[4]]
        h6 = household_a[score[5]]
        h7 = household_a[score[6]]
        h8 = household_a[score[7]]
        h9 = household_a[score[8]]
        v1 = VisitingGroup()
        v1.visiting_group_num = curr_v_num
        v1.save()
        curr_v_num += 1
        v2 = VisitingGroup()
        v2.visiting_group_num = curr_v_num
        v2.save()
        curr_v_num += 1
        v3 = VisitingGroup()
        v3.visiting_group_num = curr_v_num
        v3.save()
        curr_v_num += 1
        v4 = VisitingGroup()
        v4.visiting_group_num = curr_v_num
        v4.save()
        curr_v_num += 1
        v5 = VisitingGroup()
        v5.visiting_group_num = curr_v_num
        v5.save()
        curr_v_num += 1
        v6 = VisitingGroup()
        v6.visiting_group_num = curr_v_num
        v6.save()
        curr_v_num += 1
        v7 = VisitingGroup()
        v7.visiting_group_num = curr_v_num
        v7.save()
        curr_v_num += 1
        v8 = VisitingGroup()
        v8.visiting_group_num = curr_v_num
        v8.save()
        curr_v_num += 1
        v9 = VisitingGroup()
        v9.visiting_group_num = curr_v_num
        v9.save()
        curr_v_num += 1
        h1.first_visit = v1
        h2.first_visit = v1
        h3.first_visit = v1
        h4.first_visit = v2
        h5.first_visit = v2
        h6.first_visit = v2
        h7.first_visit = v3
        h8.first_visit = v3
        h9.first_visit = v3

        h1.second_visit = v4
        h4.second_visit = v4
        h7.second_visit = v4
        h2.second_visit = v5
        h5.second_visit = v5
        h8.second_visit = v5
        h3.second_visit = v6
        h6.second_visit = v6
        h7.second_visit = v6

        h1.third_visit = v7
        h5.third_visit = v7
        h9.third_visit = v7
        h2.third_visit = v8
        h6.third_visit = v8
        h7.third_visit = v8
        h3.third_visit = v9
        h4.third_visit = v9
        h8.third_visit = v9

        v1.save()
        v2.save()
        v3.save()
        v4.save()
        v5.save()
        v6.save()
        v7.save()
        v8.save()
        v9.save()

        h1.save()
        h2.save()
        h3.save()
        h4.save()
        h5.save()
        h6.save()
        h7.save()
        h8.save()
        h9.save()
    return HttpResponseRedirect(reverse('frontend:cluster'))

def cluster(request):
    # TODO: Authentication
    all_objects = Household.objects.all().filter(found_coords__exact=True).filter(cluster__isnull=False)

    jsonlst = []
    for obj in all_objects:
        jsonlst.append({"longitude": obj.longitude, "latitude": obj.latitude, "cluster": obj.cluster.clusterNum})

    jsonstr = json.dumps(jsonlst)

    wrong_entries = Household.objects.all().filter(found_coords__exact=False)

    return render(request, 'frontend/cluster.html', {"jsonstr": jsonstr, "wrong_entries": wrong_entries})
