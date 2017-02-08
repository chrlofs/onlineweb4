# -*- coding: utf-8 -*-
from django.conf.urls import url
from apps.meetapp import views

urlpatterns = [
    url(r'^$', views.index, name='meetapp_index'),
    url(r'^(?P<active_tab>\w+)/$', views.index, name='meetapp_active'),
    url(r'meeting/', views.create_meeting, name="meeting_creation"),
]
