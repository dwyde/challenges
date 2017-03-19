""" scoreboard URL Configuration """
from django.conf.urls import url
from django.contrib import admin

from challenges import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^challenges/$', views.list_challenges),
    url(r'^challenges/(\d+)/$', views.show_challenge),
]
