from django.contrib import admin

from frontend.models import Household, Cluster, VisitingGroup

admin.site.register(Cluster)
admin.site.register(VisitingGroup)

class HouseholdAdmin(admin.ModelAdmin):
    list_display = ('name1', 'name2', 'signup_date')

admin.site.register(Household, HouseholdAdmin)
