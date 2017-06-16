from django.conf.urls import url

from . import views

app_name = 'frontend'
urlpatterns = [
    url(r'^danke', views.signup_successful, name='signup_successful'),
    url(r'^regenerate_clusters', views.regenerate_clusters, name='regenerate_clusters'),
    url(r'^regenerate_visiting_groups', views.regenerate_visiting_groups, name='regenerate_visiting_groups'),
    url(r'^regenerate_gps', views.regenerate_gps, name='regenerate_gps'),
    url(r'^cluster', views.cluster, name='cluster'),
    url(r'^confirmation', views.confirmation, name='confirmation'),
    url(r'^faq', views.faq, name='faq'),
    url(r'^bedingungen', views.bedingungen, name='bedingungen'),
    url(r'^hilfe', views.hilfe, name='hilfe'),
    url(r'^.*$', views.index, name='index')
]
