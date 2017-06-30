from django.contrib import admin

from frontend.models import Household, Cluster, VisitingGroup, Post, Vote

admin.site.register(Cluster)
admin.site.register(VisitingGroup)
admin.site.register(Post)
admin.site.register(Vote)

class HouseholdAdmin(admin.ModelAdmin):
    list_display = ('name1', 'name2', 'street', 'signup_date')

admin.site.register(Household, HouseholdAdmin)
