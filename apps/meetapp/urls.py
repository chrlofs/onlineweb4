from django.conf.urls import url
from apps.meetapp import views

urlpatterns = [
    url(r'^$', views.index, name='meetapp'),
]
