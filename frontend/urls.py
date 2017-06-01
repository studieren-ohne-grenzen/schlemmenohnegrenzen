from django.conf.urls import url

from . import views

app_name = 'frontend'
urlpatterns = [
    url(r'^danke', views.signup_successful, name='signup_successful'),
    url(r'^regenerate_clusters', views.regenerate_clusters, name='regenerate_clusters'),
    url(r'^regenerate_visiting_groups', views.regenerate_visiting_groups, name='regenerate_visiting_groups'),
    url(r'^cluster', views.cluster, name='cluster'),
    url(r'^confirmation', views.confirmation, name='confirmation'),
    url(r'^.*$', views.index, name='index')
]