""" scoreboard URL Configuration """
from django.conf.urls import url

from challenges import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^challenges/$', views.list_challenges),
    url(r'^challenges/([-a-z]+)/$', views.show_challenge),
]
