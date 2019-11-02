from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from . import views
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from cmdb import models
app_name = 'colletData'

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    # url(r'', include(router.urls)),
    path('serverDataAPI', views.server),  ##服务器信息的上传与获取
    path('getIpsAPI', views.getIps), ##获取ip列表
]
