from django.conf.urls import url

from . import views

app_name = 'frontend'
urlpatterns = [
    url(r'^danke$', views.signup_successful, name='signup_successful'),
    url(r'^.*$', views.index, name='index')
]