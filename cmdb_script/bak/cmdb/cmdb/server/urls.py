from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from . import views
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from cmdb import models
app_name = 'server'

urlpatterns = [
    path('serverList/', views.serverList),
    path('descServer/', views.descServer),

    path('applyIp/', views.applyIps),
    path('applyIpConfirm/', views.applyIpConfirm),
    path('applydIps/', views.applydIps),
    path('deleteIp/', views.deleteIp),

    path('login/', views.signIn),
    path('', views.index),
    path('logout/', views.signOut),

]