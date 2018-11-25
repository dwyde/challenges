""" scoreboard URL Configuration """
from django.conf.urls import url

from challenges import error_views
from challenges import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^challenges/$', views.list_challenges),
    url(r'^challenges/([-a-z]+)/$', views.show_challenge),
    url(r'^error/page-not-found/$', error_views.handler404),
    url(r'^error/server-error/$', error_views.handler500)
]
