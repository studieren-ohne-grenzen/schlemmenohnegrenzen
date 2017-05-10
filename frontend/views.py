from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from frontend.models import Household
from frontend.forms import HouseholdForm

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
                note=form.cleaned_data['note'])
            house.lookup_coords()
            house.save()
            return HttpResponseRedirect(reverse('frontend:signup_successful'))
    else:
        form = HouseholdForm()
    return render(request, 'frontend/index.html', {'form': form})

def signup_successful(request):
    return render(request, 'frontend/signup_successful.html')

def cluster(request):
    #TODO: Authentication
    all_objects = Household.objects.all()
    #TODO: Clustering
    return render(request, 'frontend/cluster.html')
