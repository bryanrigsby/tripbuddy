from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.login_page),
    url(r'^register_def$', views.register),
    url(r'^register_page$', views.register_page),
    url(r'^login_def$', views.login),
    url(r'^login_page$', views.login_page),
    url(r'^success$', views.success),
    url(r'^main$', views.main),
    url(r'^new$', views.new),
    url(r'^add_trip$', views.add_trip),
    url(r'^trip/(?P<id>[0-9]+)$', views.trips),
    url(r'^trip/edit/(?P<id>[0-9]+)$', views.edit_page),
    url(r'^update$', views.update),
    url(r'^delete$', views.delete),
    url(r'^clear$', views.clear),
]